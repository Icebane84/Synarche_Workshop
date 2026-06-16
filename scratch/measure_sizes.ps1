function Get-DirSize($path) {
    if (Test-Path $path) {
        $files = Get-ChildItem -Path $path -Recurse -File -ErrorAction SilentlyContinue
        $size = ($files | Measure-Object -Property Length -Sum).Sum
        if ($size -eq $null) { $size = 0 }
        return [Math]::Round($size / 1MB, 2)
    }
    return 0
}

Write-Output "--- Subdirectories in Freeplane/freeplane ---"
Get-ChildItem -Path "C:\Users\Chris\Freeplane\freeplane" -Directory | ForEach-Object {
    $size = Get-DirSize $_.FullName
    Write-Output "$($_.Name) : $size MB"
}
