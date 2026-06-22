param([int]$Port = 4173, [string]$Root = ".")

$ErrorActionPreference = "Stop"
$Root = (Resolve-Path $Root).Path

$mime = @{
  ".html"="text/html; charset=utf-8"; ".htm"="text/html; charset=utf-8";
  ".css"="text/css; charset=utf-8"; ".js"="application/javascript; charset=utf-8";
  ".json"="application/json"; ".svg"="image/svg+xml"; ".png"="image/png";
  ".jpg"="image/jpeg"; ".jpeg"="image/jpeg"; ".gif"="image/gif";
  ".ico"="image/x-icon"; ".woff"="font/woff"; ".woff2"="font/woff2"; ".txt"="text/plain"
}

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$Port/")
$listener.Start()
Write-Host "Help My House static server running at http://localhost:$Port/  (root: $Root)"

while ($listener.IsListening) {
  try {
    $ctx = $listener.GetContext()
  } catch { break }
  $req = $ctx.Request
  $res = $ctx.Response
  try {
    $rel = [System.Uri]::UnescapeDataString($req.Url.AbsolutePath).TrimStart('/')
    if ([string]::IsNullOrWhiteSpace($rel)) { $rel = "index.html" }
    $path = Join-Path $Root $rel
    if ((Test-Path $path) -and ((Get-Item $path).PSIsContainer)) { $path = Join-Path $path "index.html" }

    if (Test-Path $path -PathType Leaf) {
      $bytes = [System.IO.File]::ReadAllBytes($path)
      $ext = [System.IO.Path]::GetExtension($path).ToLower()
      $res.ContentType = if ($mime.ContainsKey($ext)) { $mime[$ext] } else { "application/octet-stream" }
      $res.Headers.Add("Cache-Control", "no-cache")
      $res.StatusCode = 200
      $res.ContentLength64 = $bytes.Length
      $res.OutputStream.Write($bytes, 0, $bytes.Length)
    } else {
      $res.StatusCode = 404
      $msg = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found: $rel")
      $res.OutputStream.Write($msg, 0, $msg.Length)
    }
  } catch {
    try { $res.StatusCode = 500 } catch {}
  } finally {
    try { $res.OutputStream.Close() } catch {}
  }
}
