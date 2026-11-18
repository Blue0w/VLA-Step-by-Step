param(
    [Parameter(Position = 0)]
    [string]$Source
)

$ErrorActionPreference = 'Stop'
$picturesPath = Join-Path (Split-Path -Parent $PSScriptRoot) 'pictures'

if ($Source) {
    $sourceFile = Get-Item -LiteralPath $Source
    $extension = $sourceFile.Extension.ToLowerInvariant()
    if ($sourceFile.PSIsContainer -or $extension -notin @('.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.bmp', '.avif')) {
        throw 'Pass a supported image file.'
    }
    $bytes = [System.IO.File]::ReadAllBytes($sourceFile.FullName)
}
else {
    Add-Type -AssemblyName System.Windows.Forms, System.Drawing
    $clipboardImage = [System.Windows.Forms.Clipboard]::GetImage()
    if ($null -eq $clipboardImage) {
        throw 'No image found on the clipboard. Copy the image itself, or pass a file path.'
    }

    $extension = '.png'
    $buffer = [System.IO.MemoryStream]::new()
    try {
        $clipboardImage.Save($buffer, [System.Drawing.Imaging.ImageFormat]::Png)
        $bytes = $buffer.ToArray()
    }
    finally {
        $buffer.Dispose()
        $clipboardImage.Dispose()
    }
}

$lastNumber = -1
foreach ($picture in Get-ChildItem -LiteralPath $picturesPath -File) {
    if ($picture.BaseName -match '^\d+$') {
        $lastNumber = [Math]::Max($lastNumber, [int]$picture.BaseName)
    }
}

$fileName = '{0:D2}{1}' -f ($lastNumber + 1), $extension
$destination = Join-Path $picturesPath $fileName
$output = [System.IO.File]::Open($destination, [System.IO.FileMode]::CreateNew)
try {
    $output.Write($bytes, 0, $bytes.Length)
}
finally {
    $output.Dispose()
}

Write-Output "pictures/$fileName"
