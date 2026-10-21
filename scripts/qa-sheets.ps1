# Build the critique sheets for a rendered film.
#   pwsh scripts/qa-sheets.ps1 -Video films/<slug>/out/final.mp4 [-At 4.2] [-Loop]
# Writes <video dir>/qa/contact.png (2 fps), strip.png (12 frames around -At), phone.png (360 px wide),
# and loop_check.mp4 with -Loop.
param(
    [Parameter(Mandatory)][string]$Video,
    [double]$At = -1,
    [switch]$Loop
)
$ErrorActionPreference = 'Stop'
$qa = Join-Path (Split-Path (Resolve-Path $Video)) 'qa'
New-Item -ItemType Directory $qa -Force | Out-Null

ffmpeg -v error -y -i $Video -vf "fps=2,scale=270:-1,tile=6x5" -frames:v 1 "$qa/contact.png"
ffmpeg -v error -y -i $Video -vf "fps=1,scale=360:-1,tile=5x3" -frames:v 1 "$qa/phone.png"
if ($At -ge 0) {
    ffmpeg -v error -y -ss ([Math]::Max(0, $At - 0.1)) -i $Video -vf "scale=320:-1,tile=12x1" -frames:v 1 "$qa/strip.png"
}
if ($Loop) {
    ffmpeg -v error -y -stream_loop 1 -i $Video -c copy "$qa/loop_check.mp4"
}
Get-ChildItem $qa | ForEach-Object { $_.FullName }
