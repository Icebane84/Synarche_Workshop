import httpx
import json
import sys
from pathlib import Path

# Paths to files
workspace_root = Path("C:/Users/Chris/Synarche_Workspace")
pcp_path = workspace_root / "_governance/20_Architecture/UEB-PCP-001_UEB-PCP-001ThePhoenix-ClassPersona_v11.0.md"
codex_path = workspace_root / "_governance/00_CORE/CORE.CODEX.PhoenixSchema.md"

notebook_id = "notebook:uobs2otsdf34vtjwzqxe"
api_url = "http://localhost:5055/api/sources"

def upload_file(file_path: Path, title: str):
    print(f"Uploading {title} from {file_path}...")
    if not file_path.exists():
        print(f"Error: {file_path} does not exist!")
        sys.exit(1)
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Prepare form data
    data = {
        "type": "text",
        "title": title,
        "content": content,
        "notebooks": json.dumps([notebook_id]),
        "embed": "true",
        "async_processing": "true"
    }
    
    response = httpx.post(api_url, data=data, timeout=60.0)
    if response.status_code == 200:
        print(f"Successfully uploaded {title}!")
        print(response.json())
    else:
        print(f"Failed to upload {title}: {response.status_code}")
        print(response.text)
        sys.exit(1)

if __name__ == "__main__":
    upload_file(codex_path, "CORE.CODEX.PhoenixSchema.md")
    upload_file(pcp_path, "UEB-PCP-001_UEB-PCP-001ThePhoenix-ClassPersona_v11.0.md")
