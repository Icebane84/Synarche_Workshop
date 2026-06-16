# backup_submodules.ps1
# Preserves all modified/untracked files of submodules to avoid data loss during transfer

$submodules = @{
    "esperanto" = "axion-core\vendor\esperanto"
    "open-notebook" = "open-notebook"
    "documentation" = "_governance\60_Archives\Phoenix_Extraction\Documentation"
}

$recoveryRoot = "recovery\submodules"

# Ensure recovery root exists
if (!(Test-Path $recoveryRoot)) {
    New-Item -ItemType Directory -Path $recoveryRoot -Force | Out-Null
}

foreach ($name in $submodules.Keys) {
    $path = $submodules[$name]
    if (!(Test-Path $path)) {
        Write-Host "Submodule path not found: $path"
        continue
    }

    Write-Host "Processing submodule: $name ($path)"
    $destDir = Join-Path $recoveryRoot $name

    # Create destination directory
    if (!(Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }

    # Run git status --porcelain inside the submodule
    $gitStatus = git -C $path status --porcelain

    $deletedFiles = @()
    $copiedCount = 0

    foreach ($line in $gitStatus) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }

        $status = $line.Substring(0, 2).Trim()
        # The filename might be enclosed in quotes if it has special characters
        $file = $line.Substring(3).Trim()
        if ($file.StartsWith('"') -and $file.EndsWith('"')) {
            $file = $file.Substring(1, $file.Length - 2)
        }

        # Resolve paths
        $srcFile = Join-Path $path $file
        $destFile = Join-Path $destDir $file

        if ($status -eq "D") {
            # File is deleted
            $deletedFiles += $file
            Write-Host "  [DELETED] $file"
        }
        else {
            # File is modified, added, or untracked
            if (Test-Path $srcFile -PathType Leaf) {
                $parentDir = Split-Path $destFile
                if (!(Test-Path $parentDir)) {
                    New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
                }
                Copy-Item -Path $srcFile -Destination $destFile -Force
                Write-Host "  [COPIED] $file -> $destFile"
                $copiedCount++
            }
            elseif (Test-Path $srcFile -PathType Container) {
                # If it's a directory (untracked directory), copy recursively
                $parentDir = Split-Path $destFile
                if (!(Test-Path $parentDir)) {
                    New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
                }
                Copy-Item -Path $srcFile -Destination $destFile -Recurse -Force
                Write-Host "  [COPIED DIR] $file -> $destFile"
                $copiedCount++
            }
        }
    }

    # Write deleted files list
    if ($deletedFiles.Count -gt 0) {
        $deletedListPath = Join-Path $destDir "deleted_files.txt"
        $deletedFiles | Out-File -FilePath $deletedListPath -Encoding utf8
        Write-Host "  [LOGGED DELETIONS] -> $deletedListPath"
    }

    Write-Host "Submodule $name complete. Copied: $copiedCount, Deleted: $($deletedFiles.Count)"
}
