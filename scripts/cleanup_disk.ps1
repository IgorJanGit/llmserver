# Disk Cleanup Script for LLM Server
# Safely cleans temporary files and caches to free up space

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Disk Cleanup Utility" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

$totalFreed = 0

# Function to safely delete folder contents
function Clear-FolderSafe {
    param($Path, $Name)
    
    if (Test-Path $Path) {
        Write-Host "Cleaning $Name..." -ForegroundColor Yellow
        $sizeBefore = (Get-ChildItem $Path -Recurse -ErrorAction SilentlyContinue | 
                      Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        
        try {
            Get-ChildItem $Path -Recurse -ErrorAction SilentlyContinue | 
                Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
            
            $sizeAfter = (Get-ChildItem $Path -Recurse -ErrorAction SilentlyContinue | 
                         Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
            
            if ($null -eq $sizeAfter) { $sizeAfter = 0 }
            if ($null -eq $sizeBefore) { $sizeBefore = 0 }
            
            $freed = $sizeBefore - $sizeAfter
            $freedMB = [math]::Round($freed / 1MB, 2)
            
            Write-Host "  OK Freed: $freedMB MB" -ForegroundColor Green
            return $freed
        }
        catch {
            Write-Host "  WARNING: Some files could not be deleted (in use)" -ForegroundColor Yellow
            return 0
        }
    }
    else {
        Write-Host "  $Name not found, skipping" -ForegroundColor Gray
        return 0
    }
}

# Clean Windows Temp
$totalFreed += Clear-FolderSafe "$env:TEMP" "Windows Temp"

# Clean User Temp
$totalFreed += Clear-FolderSafe "$env:USERPROFILE\AppData\Local\Temp" "User Temp"

# Clean Internet Cache
$totalFreed += Clear-FolderSafe "$env:USERPROFILE\AppData\Local\Microsoft\Windows\INetCache" "Internet Cache"

# Clean pip cache
$totalFreed += Clear-FolderSafe "$env:USERPROFILE\AppData\Local\pip\cache" "Python pip cache"

# Clean npm cache (if exists)
$totalFreed += Clear-FolderSafe "$env:APPDATA\npm-cache" "npm cache"

# Clean general cache folder
$totalFreed += Clear-FolderSafe "$env:USERPROFILE\.cache" "General cache"

# Optional: List large files in Downloads (do not delete automatically)
Write-Host "`nLarge files in Downloads:" -ForegroundColor Cyan
if (Test-Path "$env:USERPROFILE\Downloads") {
    $largeFiles = Get-ChildItem "$env:USERPROFILE\Downloads" -File -Recurse -ErrorAction SilentlyContinue |
                  Where-Object { $_.Length -gt 100MB } |
                  Sort-Object Length -Descending |
                  Select-Object -First 10
    
    if ($largeFiles) {
        $largeFiles | ForEach-Object {
            $sizeMB = [math]::Round($_.Length / 1MB, 2)
            Write-Host "  - $($_.Name) - $sizeMB MB" -ForegroundColor Gray
        }
        Write-Host "`n  WARNING: Review and delete manually if not needed" -ForegroundColor Yellow
    }
    else {
        Write-Host "  No large files found" -ForegroundColor Green
    }
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
$totalFreedGB = [math]::Round($totalFreed / 1GB, 2)
Write-Host "  Total Space Freed: $totalFreedGB GB" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

# Show current disk space
Write-Host "Current disk space:" -ForegroundColor Cyan
Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Used -ne $null} | 
    Select-Object Name, 
        @{Name="Free(GB)";Expression={[math]::Round($_.Free/1GB,2)}},
        @{Name="Total(GB)";Expression={[math]::Round(($_.Used+$_.Free)/1GB,2)}},
        @{Name="Free%";Expression={[math]::Round($_.Free/($_.Used+$_.Free)*100,1)}} |
    Format-Table -AutoSize

Write-Host "`nCleanup complete!`n" -ForegroundColor Green
