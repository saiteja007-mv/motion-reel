"""Place earshot bank takes on a film's cue times and write audio/score.wav (48 kHz stereo, 24-bit).

Copy into films/<slug>/audio/, set DUR and CUES, then run it with earshot's venv:
    & $env:EARSHOT_PYTHON audio/score.py      (PowerShell)
    "$EARSHOT_PYTHON" audio/score.py          (bash)
Each cue puts the take's measured onset (or peak, for whooshes and stings) on its picture time.
Browse bank ids with `python -m earshot sfx list`. Master the result afterwards (see AGENTS.md, Sound).
"""
import os

import numpy as np
import soundfile as sf
from earshot.forge import bank

SR, DUR = 48000, 12.0  # DUR = film length in seconds
HERE = os.path.dirname(os.path.abspath(__file__))

# (time s, bank id, align on "onset" or "peak", gain dB, render kwargs). Example cues: replace with yours.
CUES = [
    (0.30, 'fit/land.light/finger_phone', 'onset', -6, {}),                # first text fragment lands
    (2.00, 'whoosh_fast/crisp', 'peak', -8, {'dur': 0.7, 'apex': 0.35}),   # scene handoff
    (3.85, 'hover_tick/detent', 'onset', -10, {}),                         # cards appear: same pitch, no climb
    (4.65, 'hover_tick/detent', 'onset', -10, {}),
    (9.85, 'logo_sting/soft_bloom', 'peak', -4, {}),                       # logo lockup: one clean hit
]

mix = np.zeros((int(SR * DUR), 2), dtype=np.float64)
for seed, (t, sid, align, gain, kw) in enumerate(CUES):
    y, meta = bank.render(sid, seed=seed + 1, **kw)
    sr = meta.get('sr', SR)
    if sr != SR:
        raise SystemExit(f'{sid}: sample rate {sr}, expected {SR}')
    y = np.asarray(y, dtype=np.float64)
    if y.ndim == 1:
        y = np.stack([y, y], axis=1)
    anchor = float(meta[f'{align}_s'])  # bank meta: onset_s / peak_s, measured on this take
    start = int(round((t - anchor) * SR))
    a, b = max(start, 0), min(start + len(y), len(mix))
    if b > a:
        mix[a:b] += y[a - start:b - start] * 10 ** (gain / 20)
    print(f'{t:5.2f}s {sid:32s} {align}={anchor:.3f}s')

peak = np.abs(mix).max()
if peak > 0.89:
    mix *= 0.89 / peak
sf.write(os.path.join(HERE, 'score.wav'), mix.astype(np.float32), SR, subtype='PCM_24')
print('wrote audio/score.wav')
