/**
 * @artifact src/core/hooks/useMemoryFeed.ts
 * Paginated memory_entries with live INSERT subscription.
 */

import { useState, useEffect, useCallback } from "react";
import { supabase } from "@/core/supabase";
import { useRealtime } from "./useRealtime";
import type { MemoryEntry } from "@/core/supabase";

interface MemoryFilters {
  domain?: string;
  state?: MemoryEntry["state"];
  layer?: number;
  search?: string;
}

interface UseMemoryFeedResult {
  memories: MemoryEntry[];
  total: number;
  isLoading: boolean;
  error: string | null;
  page: number;
  setPage: (page: number) => void;
  setFilters: (filters: MemoryFilters) => void;
  refetch: () => void;
  insert: (entry: { content: string; domain: string; memory_layer?: number }) => Promise<void>;
  updateState: (id: number, state: MemoryEntry["state"]) => Promise<void>;
  archive: (id: number) => Promise<void>;
  remove: (id: number) => Promise<void>;
  checkResonance: (entityId: string, content: string) => Promise<any>;
}

const PAGE_SIZE = 20;

export function useMemoryFeed(): UseMemoryFeedResult {
  const [memories, setMemories] = useState<MemoryEntry[]>([]);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [filters, setFilters] = useState<MemoryFilters>({});

  const fetch = useCallback(async () => {
    setIsLoading(true);
    let query = supabase
      .from("memory_entries")
      .select("*", { count: "exact" })
      .order("last_retrieved", { ascending: false })
      .range(page * PAGE_SIZE, (page + 1) * PAGE_SIZE - 1);

    if (filters.domain) query = query.eq("domain", filters.domain);
    if (filters.state)  query = query.eq("state", filters.state);
    if (filters.layer)  query = query.eq("memory_layer", filters.layer);
    if (filters.search) query = query.ilike("content", `%${filters.search}%`);

    const { data, error: err, count } = await query;
    if (err) setError(err.message);
    else {
      setMemories(data ?? []);
      setTotal(count ?? 0);
    }
    setIsLoading(false);
  }, [page, filters]);

  useEffect(() => { fetch(); }, [fetch]);

  // Flash new rows on INSERT
  useRealtime("memory_entries", "INSERT", (payload) => {
    const newEntry = payload.new as MemoryEntry;
    setMemories((prev) => [newEntry, ...prev.slice(0, PAGE_SIZE - 1)]);
    setTotal((t) => t + 1);
  });

  const insert = async (entry: { content: string; domain: string; memory_layer?: number }) => {
    const content_hash = await crypto.subtle
      .digest("SHA-256", new TextEncoder().encode(entry.content))
      .then((buf) => Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, "0")).join(""));

    const { error: err } = await supabase.from("memory_entries").insert({
      ...entry,
      content_hash,
      state: "Active",
    });
    if (err) setError(err.message);
  };

  const updateState = async (id: number, state: MemoryEntry["state"]) => {
    const { error: err } = await supabase
      .from("memory_entries")
      .update({ state })
      .eq("id", id);
    if (err) setError(err.message);
    else setMemories((prev) => prev.map((m) => m.id === id ? { ...m, state } : m));
  };

  const archive = async (id: number) => {
    await updateState(id, "Archived");
  };

  const remove = async (id: number) => {
    const { error: err } = await supabase.from("memory_entries").delete().eq("id", id);
    if (err) setError(err.message);
    else setMemories((prev) => prev.filter((m) => m.id !== id));
  };

  const checkResonance = async (entityId: string, content: string) => {
    const { data, error: err } = await supabase.functions.invoke("sentinel-dissonance-check", {
      body: { entity_id: entityId, content, generate_quest: true },
    });
    if (err) throw err;
    return data;
  };

  return { memories, total, isLoading, error, page, setPage, setFilters, refetch: fetch, insert, updateState, archive, remove, checkResonance };
}
