$site = "C:\Users\THINKPAD\AppData\Local\Programs\Python\Python311\Lib\site-packages"
$dist = "dist\ShopeeAgent\_internal"

$packages = @(
    'camoufox', 'browserforge', 'apify_fingerprint_datapoints',
    'language_tags', 'crewai', 'click', 'playwright'
)

foreach ($pkg in $packages) {
    $srcDir = Join-Path $site $pkg
    if (-not (Test-Path $srcDir)) { continue }
    
    $count = 0
    Get-ChildItem $srcDir -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
        $ext = $_.Extension.ToLower()
        if ($ext -eq '.py' -or $ext -eq '.pyc') { return }
        
        $relPath = $_.FullName.Replace("$site\", "")
        $destFile = Join-Path $dist $relPath
        $destDir = Split-Path $destFile -Parent
        New-Item -ItemType Directory -Force -Path $destDir | Out-Null
        Copy-Item $_.FullName $destFile -Force
        $count++
    }
    Write-Host "OK: $pkg - $count data files copied"
}

# Copy icon to dist root
$iconSrc = Join-Path (Split-Path (Split-Path $dist)) "logoicon.png"
if (Test-Path $iconSrc) {
    $iconDest = Split-Path $dist
    Copy-Item $iconSrc "$iconDest\logoicon.png" -Force
    Write-Host "OK: logoicon.png copied to dist"
}

Write-Host ""
Write-Host "DONE! All data files copied."
