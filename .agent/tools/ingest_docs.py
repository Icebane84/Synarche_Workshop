import json
import os
from pathlib import Path

import requests

# Configuration
API_URL = "http://127.0.0.1:5055/api"
WORKSPACE_ROOT = r"C:\Users\Chris\Synarche_Workspace"
TARGET_FOLDERS = [
    r"_governance",
    r"_Desktop_Vault\Phoenix",  # Assuming this is mapped or copied? If not, we scan what we can.
    # We will verify paths exist before scanning
]

# We will create one Notebook for each top-level folder we scan
# e.g. "Synarche Governance" for _governance


def create_notebook(name, description):
    """Create a notebook and return its ID."""
    try:
        response = requests.post(
            f"{API_URL}/notebooks", json={"name": name, "description": description}
        )
        response.raise_for_status()
        return response.json()["id"]
    except Exception as e:
        print(f"Error creating notebook '{name}': {e}")
        return None


def upload_file(file_path, notebook_id):
    """Upload a file as a source linked to the notebook."""
    try:
        filename = os.path.basename(file_path)
        print(f"Uploading {filename}...")

        # We use the 'upload' type which mimics a file upload
        # The API expects multipart/form-data

        with open(file_path, "rb") as f:
            files = {"file": (filename, f, "text/markdown")}
            data = {
                "type": "upload",
                "title": Path(filename).stem,  # Use filename without extension as title
                "notebooks": json.dumps([notebook_id]),  # Link to notebook immediately
                "async_processing": "true",  # Use async to avoid timeouts on large batches
                # 'embed': 'true' # Optional: Auto-embed? Maybe let user decide or default to False to save $$$
            }

            response = requests.post(f"{API_URL}/sources", data=data, files=files)
            if response.status_code != 200:
                print(f"Failed to upload {filename}: {response.text}")
            else:
                print(f"Successfully queued {filename}")

    except Exception as e:
        print(f"Error uploading {file_path}: {e}")


def main():
    print("Checking API connection...")
    try:
        requests.get(f"{API_URL.replace('/api', '')}/health", timeout=2)
        print("API is online.")
    except:
        print(f"❌ Could not connect to {API_URL}")
        print("Please make sure the Open Notebook API server is running (Terminal 2).")
        return

    for folder_rel in TARGET_FOLDERS:
        folder_path = os.path.join(WORKSPACE_ROOT, folder_rel)

        # Handle absolute paths if user provided them, or distinct roots
        if not os.path.exists(folder_path):
            # Try checking if it's an absolute path that was passed
            if os.path.exists(folder_rel):
                folder_path = folder_rel
            else:
                print(f"Skipping missing folder: {folder_path}")
                continue

        folder_name = os.path.basename(folder_path)
        notebook_name = f"Synarche: {folder_name}"
        print(f"\nProcessing folder: {folder_path} -> Notebook: {notebook_name}")

        # Create Notebook
        notebook_id = create_notebook(
            notebook_name, f"Imported documentation from {folder_name}"
        )
        if not notebook_id:
            continue

        # Walk and Upload
        count = 0
        for root, _dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(".md"):
                    full_path = os.path.join(root, file)
                    upload_file(full_path, notebook_id)
                    count += 1

        print(f"Finished uploading {count} files to '{notebook_name}'.")


if __name__ == "__main__":
    main()
