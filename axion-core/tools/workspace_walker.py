#!/usr/bin/env python3
# Copyright Phoenix Protocol. All rights reserved.
# GVRN.Engine.WorkspaceWalker.PY
# Sliding-Window State Machine Crawler for Synarche Monorepo Traversal

import argparse
import hashlib
import json
import mmap
import os
import re
import struct
import sys
import yaml

# Standardize console encoding for Windows Cp1252 console safety
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

def compute_sha256(filepath):
    if not os.path.exists(filepath):
        return ""
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""

class MmapLedgerCache:
    """
    High-performance binary mmap cache for the ledger data.
    Accelerates startup time by reading directly from a page-aligned binary file.
    """
    HEADER_FMT = "<IIII32s"  # magic_id, version, dirty, state_size, state_hash
    MAGIC = 0x53594E43      # "SYNC" in hex

    def __init__(self, cache_path):
        self.cache_path = cache_path
        self.mm = None
        self.f = None

    def load_cache(self) -> dict:
        if not os.path.exists(self.cache_path):
            return {}
        try:
            self.f = open(self.cache_path, "r+b")
            self.mm = mmap.mmap(self.f.fileno(), 0)
            self.mm.seek(0)
            
            header_size = struct.calcsize(self.HEADER_FMT)
            header_bytes = self.mm.read(header_size)
            magic, version, dirty, state_size, state_hash = struct.unpack(self.HEADER_FMT, header_bytes)
            
            if magic != self.MAGIC or state_size == 0:
                self.close()
                return {}
                
            state_blob = self.mm.read(state_size)
            # Verify hash to guarantee structural integrity
            if hashlib.sha256(state_blob).digest() != state_hash:
                self.close()
                return {}
                
            return json.loads(state_blob.decode('utf-8'))
        except Exception:
            self.close()
            return {}

    def write_cache(self, data_dict) -> bool:
        try:
            state_blob = json.dumps(data_dict).encode('utf-8')
            state_size = len(state_blob)
            state_hash = hashlib.sha256(state_blob).digest()
            header_size = struct.calcsize(self.HEADER_FMT)
            total_size = header_size + state_size
            
            # Align to 4096-byte memory page boundaries
            aligned_size = ((total_size + 4095) // 4096) * 4096
            
            # Write padding block
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            with open(self.cache_path, "wb") as f:
                f.write(b"\x00" * aligned_size)
                
            self.f = open(self.cache_path, "r+b")
            self.mm = mmap.mmap(self.f.fileno(), 0)
            self.mm.seek(0)
            
            header = struct.pack(
                self.HEADER_FMT,
                self.MAGIC,
                1,  # version
                0,  # dirty
                state_size,
                state_hash
            )
            self.mm.write(header + state_blob)
            self.mm.flush()
            return True
        except Exception as e:
            print(f"Error writing binary mmap cache: {e}", file=sys.stderr)
            self.close()
            return False

    def close(self):
        if self.mm:
            try:
                self.mm.close()
            except Exception:
                pass
            self.mm = None
        if self.f:
            try:
                self.f.close()
            except Exception:
                pass
            self.f = None

class WorkspaceWalker:
    def __init__(self, workspace_root=None):
        if workspace_root is None:
            # Resolve relative to script path (three directories up from axion-core/tools/)
            workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.workspace_root = workspace_root
        
        self.registry_path = os.path.join(workspace_root, "_governance", "01_Registries", "GVRN.Master.Registry.yaml")
        self.ledger_path = os.path.join(workspace_root, "_governance", "50_Logs", "LOG.MECS.LEDGER.json")
        self.ledger_cache_path = os.path.join(workspace_root, "_governance", "50_Logs", "LOG.MECS.LEDGER.bin")
        
        self.registry = self._load_registry()
        self.ledger_records = self._load_ledger()
        
        self.history = []

    def _load_registry(self):
        if not os.path.exists(self.registry_path):
            print(f"Warning: Master registry not found at {self.registry_path}", file=sys.stderr)
            return {}
        with open(self.registry_path, "r", encoding="utf-8") as f:
            try:
                return yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Error parsing registry: {e}", file=sys.stderr)
                return {}

    def _load_ledger(self):
        # 1. Attempt to load from high-performance binary mmap cache
        # Check if the JSON ledger is newer than the binary cache
        json_mtime = os.path.getmtime(self.ledger_path) if os.path.exists(self.ledger_path) else 0
        bin_mtime = os.path.getmtime(self.ledger_cache_path) if os.path.exists(self.ledger_cache_path) else 0
        
        cache_handler = MmapLedgerCache(self.ledger_cache_path)
        if bin_mtime > json_mtime:
            cached_data = cache_handler.load_cache()
            if cached_data:
                cache_handler.close()
                return self._normalize_ledger_records(cached_data.get("records", []))
            
        # 2. Fall back to standard JSON ledger file
        if not os.path.exists(self.ledger_path):
            cache_handler.close()
            return {}
            
        with open(self.ledger_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                # Populate binary mmap cache for subsequent lightning-fast runs
                cache_handler.write_cache(data)
                cache_handler.close()
                return self._normalize_ledger_records(data.get("records", []))
            except Exception:
                cache_handler.close()
                return {}

    def _normalize_ledger_records(self, records):
        normalized = {}
        duplicates = []
        for r in records:
            raw_path = r.get("artifact_path")
            if not raw_path:
                continue
            key = raw_path.replace("\\", "/")
            if key in normalized:
                duplicates.append(key)
            normalized[key] = r
        if duplicates:
            print(
                f"Warning: ledger contains duplicate artifact_path entries "
                f"(last one wins): {duplicates}",
                file=sys.stderr,
            )
        return normalized



    def check_waning_seal(self, rel_path):
        # Normalize relative path separators
        normalized_path = rel_path.replace("\\", "/")
        full_path = os.path.join(self.workspace_root, normalized_path)
        
        if not os.path.exists(full_path):
            return "MISSING"
            
        record = self.ledger_records.get(normalized_path)
        if not record:
            return "UNVERIFIED"
            
        current_hash = compute_sha256(full_path)
        if current_hash == record.get("content_sha256"):
            return "STILL_VALID"
        else:
            return "STALE_VERIFICATION_VOID"

    def get_node_by_id_or_path(self, target):
        # 1. Exact match on registry key
        if target in self.registry:
            return target, self.registry[target]
            
        # 2. Match artifact_id
        for k, v in self.registry.items():
            if v.get("artifact_id") == target:
                return k, v
                
        # 3. Match path (suffix or full)
        target_norm = target.replace("\\", "/")
        for k, v in self.registry.items():
            path_val = v.get("path", "")
            if path_val and (path_val.endswith(target_norm) or target_norm in path_val):
                return k, v
                
        return None, None

    def render_sliding_context(self, node_key, view_code=False):
        node = self.registry.get(node_key)
        if not node:
            return f"Error: Registry node '{node_key}' not found."
            
        rel_path = node.get("path", "")
        seal_status = self.check_waning_seal(rel_path)
        full_path = os.path.join(self.workspace_root, rel_path)
        
        # Determine whether to print raw file content
        file_content = ""
        if seal_status == "MISSING":
            # Explicit branch: previously this fell through to the
            # "STILL_VALID" cached-content message below, which is a false
            # reassurance — the file is gone, not cached-and-fine.
            file_content = "[File missing on disk — cannot verify or display content]"
        elif view_code or seal_status == "STALE_VERIFICATION_VOID" or seal_status == "UNVERIFIED":
            if os.path.exists(full_path):
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                except Exception as e:
                    file_content = f"[Error reading file: {e}]"
            else:
                file_content = "[File missing on disk]"

        # Format relations list
        relations = node.get("parsed_relations", [])
        if not relations:
            # Fallback to plain relations string
            relations_str = node.get("relations", "None")
        else:
            relations_str = "\n".join(f"  - {r}" for r in relations)

        prompt = f"""=== SYSTEM COGNITIVE ANCHOR (SLIDING CONTEXT FRAME) ===
Node ID: {node_key}
Artifact ID: {node.get('artifact_id', 'UNKNOWN')}
Official Name: {node.get('official_name', 'UNKNOWN')}
Path: {rel_path}
Version: {node.get('version', 'UNKNOWN')}
Status: {node.get('status_(state)', 'UNKNOWN')}
Waning Seal Status: {seal_status}
------------------------------------------------------
Relations:
{relations_str}
------------------------------------------------------
Axiomatic Specs:
{yaml.dump(node.get('specs', {})) if node.get('specs') else 'None'}
------------------------------------------------------
"""
        if file_content:
            prompt += f"--- [FILE CONTENT] ---\n{file_content}\n"
        else:
            prompt += f"--- [FILE CONTENT CACHED] ---\n[Waning Seal is STILL_VALID. File contents cached to prevent context ceiling overflow.]\n"
            
        prompt += "======================================================"
        return prompt

    def get_relations_list(self, node_key):
        node = self.registry.get(node_key)
        if not node:
            return []
        
        relations_list = []
        parsed = node.get("parsed_relations", [])
        for rel in parsed:
            if isinstance(rel, dict):
                for rel_type, target_id in rel.items():
                    relations_list.append((rel_type, target_id))
            elif isinstance(rel, str) and ":" in rel:
                parts = rel.split(":", 1)
                relations_list.append((parts[0].strip(), parts[1].strip()))
        return relations_list

    def run_interactive(self, start_node=None):
        if not self.registry:
            print("Fatal: Registry is empty. Interactive mode aborted.", file=sys.stderr)
            return 1
            
        # Default start node
        if start_node is None:
            # Look for PromptDSL spec
            for k in self.registry:
                if "PROMPT_DSL_SPEC" in k or "PromptDSL" in k:
                    start_node = k
                    break
            if not start_node:
                start_node = list(self.registry.keys())[0]

        curr_key, curr_node = self.get_node_by_id_or_path(start_node)
        if not curr_key:
            print(f"Error: Node '{start_node}' not found. Starting with first registry node.")
            curr_key = list(self.registry.keys())[0]

        while True:
            print("\n" + "="*60 + "\n")
            context_str = self.render_sliding_context(curr_key)
            print(context_str)
            
            relations = self.get_relations_list(curr_key)
            print("\nAvailable Traversal Options:")
            for idx, (rel_type, target_id) in enumerate(relations, start=1):
                print(f"  [{idx}] {rel_type} -> {target_id}")
                
            print("\nNavigation commands:")
            print("  goto <num_or_id> : Traverse to index or specific node ID")
            print("  view             : View full raw code/file contents")
            print("  back             : Go back to previous node")
            print("  exit             : Quit")
            
            try:
                cmd = input("\nwalker> ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting.")
                break
                
            if not cmd:
                continue
                
            cmd_lower = cmd.lower()
            if cmd_lower == "exit":
                break
            elif cmd_lower == "back":
                if self.history:
                    curr_key = self.history.pop()
                else:
                    print("History stack is empty.")
            elif cmd_lower == "view":
                print("\n--- RAW FILE CONTENT ---")
                print(self.render_sliding_context(curr_key, view_code=True))
                input("\nPress Enter to return...")
            elif cmd_lower.startswith("goto "):
                target_str = cmd[5:].strip()
                next_key = None
                
                if target_str.isdigit():
                    val = int(target_str)
                    if 1 <= val <= len(relations):
                        target_id = relations[val-1][1]
                        next_key, _ = self.get_node_by_id_or_path(target_id)
                else:
                    next_key, _ = self.get_node_by_id_or_path(target_str)
                    
                if next_key:
                    self.history.append(curr_key)
                    curr_key = next_key
                else:
                    print(f"Error: Target '{target_str}' not found in registry or index.")
            else:
                next_key, _ = self.get_node_by_id_or_path(cmd)
                if next_key:
                    self.history.append(curr_key)
                    curr_key = next_key
                else:
                    print(f"Invalid command or target: '{cmd}'")
                    
        return 0

def main():
    parser = argparse.ArgumentParser(description="Navigate the Synarche Workspace Knowledge Graph.")
    parser.add_argument("--node", help="Specific node ID or path to output sliding context prompt for.")
    parser.add_argument("--view", action="store_true", help="Force display file contents in output.")
    parser.add_argument("--interactive", action="store_true", help="Start interactive navigation crawler loop.")
    
    args = parser.parse_args()
    
    walker = WorkspaceWalker()
    
    if args.interactive or (not args.node):
        sys.exit(walker.run_interactive(args.node))
    else:
        node_key, _ = walker.get_node_by_id_or_path(args.node)
        if not node_key:
            print(f"Error: Node/Path '{args.node}' not found in registry.", file=sys.stderr)
            sys.exit(1)
        print(walker.render_sliding_context(node_key, view_code=args.view))
        sys.exit(0)

if __name__ == "__main__":
    main()
