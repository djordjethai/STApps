# Set the folder path where your .py files are located (including subfolders)
$folderPath = "."

# Get a list of all .py files in the folder (including subfolders)
$fileList = Get-ChildItem -Path $folderPath -File -Recurse -Filter *.py

# Define a function to remove the BOM from a file
function Remove-BOM {
    param (
        [string]$filePath
    )
    $content = Get-Content -Path $filePath -Raw
    $content = $content -replace '^\xEF\xBB\xBF', ''
    Set-Content -Path $filePath -Value $content -Encoding UTF8
}

# Iterate through each .py file and remove the BOM if present
foreach ($file in $fileList) {
    Write-Host "Processing .py file: $($file.FullName)"
    Remove-BOM -filePath $file.FullName
}

Write-Host "BOM removal process completed for all .py files."
