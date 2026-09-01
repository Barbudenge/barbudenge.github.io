$ErrorActionPreference = 'Stop'

$siteRoot = Split-Path -Parent $PSScriptRoot
$baseUrl = 'https://barbudenge.github.io'
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)

function New-SitemapEntry {
  param(
    [Parameter(Mandatory)] [string] $Url,
    [Parameter(Mandatory)] [string] $LastModified
  )

  if ($LastModified -notmatch '^\d{4}-\d{2}-\d{2}$') {
    throw "Invalid lastmod '$LastModified' for $Url"
  }

  [pscustomobject]@{
    Url = $Url
    LastModified = $LastModified
  }
}

function Get-ArticleEntry {
  param([Parameter(Mandatory)] [System.IO.FileInfo] $File)

  $html = [System.IO.File]::ReadAllText($File.FullName)
  $canonicalMatch = [regex]::Match($html, '<link\s+rel="canonical"\s+href="([^"]+)"')
  $publishedMatch = [regex]::Match($html, '"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})"')
  $modifiedMatch = [regex]::Match($html, '"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})"')

  if (-not $canonicalMatch.Success) {
    throw "Missing canonical URL in $($File.FullName)"
  }
  if (-not $publishedMatch.Success) {
    throw "Missing datePublished in $($File.FullName)"
  }

  $lastModified = if ($modifiedMatch.Success) {
    $modifiedMatch.Groups[1].Value
  } else {
    $publishedMatch.Groups[1].Value
  }

  New-SitemapEntry -Url $canonicalMatch.Groups[1].Value -LastModified $lastModified
}

$articleFiles = @(
  Get-ChildItem (Join-Path $siteRoot 'artigos') -Filter '*.html' -File |
    Where-Object Name -ne 'index.html'
  Get-ChildItem (Join-Path $siteRoot 'pt-br/artigos') -Filter '*.html' -File |
    Where-Object Name -ne 'index.html'
)

$articleEntries = @($articleFiles | ForEach-Object { Get-ArticleEntry $_ } | Sort-Object Url)
$latestArticleDate = ($articleEntries.LastModified | Sort-Object -Descending | Select-Object -First 1)

$entries = @(
  New-SitemapEntry "$baseUrl/projects/" '2026-09-01'
  New-SitemapEntry "$baseUrl/projects/pt-br/" '2026-09-01'
  New-SitemapEntry "$baseUrl/" $latestArticleDate
  New-SitemapEntry "$baseUrl/pt-br/" $latestArticleDate
  New-SitemapEntry "$baseUrl/privacy.html" '2026-06-15'
  New-SitemapEntry "$baseUrl/pt-br/privacy.html" '2026-06-15'
  New-SitemapEntry "$baseUrl/sobre.html" '2026-06-15'
  New-SitemapEntry "$baseUrl/pt-br/sobre.html" '2026-06-15'
  New-SitemapEntry "$baseUrl/artigos/" $latestArticleDate
  New-SitemapEntry "$baseUrl/pt-br/artigos/" $latestArticleDate
  $articleEntries
  New-SitemapEntry "$baseUrl/engrenarium/" '2026-09-01'
  New-SitemapEntry "$baseUrl/engrenarium/pt-br/" '2026-09-01'
  New-SitemapEntry "$baseUrl/camforge/" '2026-08-28'
  New-SitemapEntry "$baseUrl/camforge/pt-br/" '2026-08-28'
)

$duplicates = $entries | Group-Object Url | Where-Object Count -gt 1
if ($duplicates) {
  throw "Duplicate sitemap URLs: $($duplicates.Name -join ', ')"
}

$urlSetLines = [System.Collections.Generic.List[string]]::new()
$urlSetLines.Add('<?xml version="1.0" encoding="UTF-8"?>')
$urlSetLines.Add('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
foreach ($entry in $entries) {
  $url = [System.Security.SecurityElement]::Escape($entry.Url)
  $urlSetLines.Add('  <url>')
  $urlSetLines.Add("    <loc>$url</loc>")
  $urlSetLines.Add("    <lastmod>$($entry.LastModified)</lastmod>")
  $urlSetLines.Add('  </url>')
}
$urlSetLines.Add('</urlset>')

$latestSitemapDate = ($entries.LastModified | Sort-Object -Descending | Select-Object -First 1)
$sitemapIndex = @(
  '<?xml version="1.0" encoding="UTF-8"?>'
  '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
  '  <sitemap>'
  "    <loc>$baseUrl/urls-sitemap.xml</loc>"
  "    <lastmod>$latestSitemapDate</lastmod>"
  '  </sitemap>'
  '</sitemapindex>'
)

[System.IO.File]::WriteAllText(
  (Join-Path $siteRoot 'urls-sitemap.xml'),
  ($urlSetLines -join "`n") + "`n",
  $utf8NoBom
)
[System.IO.File]::WriteAllText(
  (Join-Path $siteRoot 'sitemap.xml'),
  ($sitemapIndex -join "`n") + "`n",
  $utf8NoBom
)
[System.IO.File]::WriteAllText(
  (Join-Path $siteRoot 'sitemap.txt'),
  (($entries.Url) -join "`n") + "`n",
  $utf8NoBom
)

Write-Output "Generated $($entries.Count) canonical URLs; latest content date is $latestSitemapDate."
