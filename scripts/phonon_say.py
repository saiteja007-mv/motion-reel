#!/usr/bin/env python3
"""Local, offline text-to-speech with Phonon (gradium-ai/xn-ptts). Commercial-safe by default.

  & $env:PHONON_PYTHON phonon_say.py "Welcome back." -o vo.wav --voice Miles --seed 1
  & $env:PHONON_PYTHON phonon_say.py --file line.txt -o vo.wav --rate 48000     (48 kHz for video mixes)
  & $env:PHONON_PYTHON phonon_say.py --list-voices
Anywhere with uv:  uv run --with ptts python phonon_say.py ...

Licence guard: Phonon 31M and its voice catalog are Apache-2.0, fine for monetised video. The 40M models are
CC BY-NC 4.0, so any model other than Phonon 31M is refused unless --noncommercial is passed.
Every other flag (text, --voice, --seed, --temperature, --quant, --list-voices) passes through to ptts.
"""
import argparse
import os
import subprocess
import sys

import ptts

ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
ap.add_argument("-m", "--model", default=ptts.DEFAULT_MODEL)
ap.add_argument("-o", "--output", default="out.wav")
ap.add_argument("-l", "--lang", default="en")
ap.add_argument("--file", help="read the text from this UTF-8 file instead of the command line")
ap.add_argument("--rate", type=int, help="resample the WAV with ffmpeg, e.g. 48000 for a video mix (native: 24000)")
ap.add_argument("--noncommercial", action="store_true",
                help="allow a model other than Phonon 31M; the 40M models are CC BY-NC 4.0, never for monetised video")
a, rest = ap.parse_known_args()

if "phonon-31m" not in a.model and not a.noncommercial:
    sys.exit(f"phonon_say: refusing {a.model}: only Phonon 31M is cleared for monetised use (40M is CC BY-NC 4.0). "
             "Use the default model, or pass --noncommercial for private, unmonetised audio.")
if a.file:
    with open(a.file, encoding="utf-8") as f:
        rest += ["--", f.read().strip()]

raw = a.output + ".tmp.wav" if a.rate else a.output
code = subprocess.call([sys.executable, "-m", "ptts", "--model", a.model, "--lang", a.lang, "-o", raw, *rest])
if a.rate and os.path.exists(raw):
    if code == 0:
        code = subprocess.call(["ffmpeg", "-v", "error", "-y", "-i", raw, "-ar", str(a.rate), a.output])
    os.remove(raw)
sys.exit(code)
