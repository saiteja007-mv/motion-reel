# motion-reel

An agent skill and studio kit for **motion graphics rendered from code**: channel intros, launch films,
product and website promos, explainers, Shorts clips and transparent overlays for an editor.

You give a coding agent (Claude Code, Codex, Cursor, Gemini CLI, opencode...) a brief. It picks the
engine, builds the film as a pure function of time, scores it with synthesized sound, critiques its own
contact sheets until every score is 8+, and renders the master. Nothing is published or uploaded.

> **Agents:** start at [`AGENTS.md`](AGENTS.md) (house rules), then
> [`skills/motion-reel/SKILL.md`](skills/motion-reel/SKILL.md) (the pipeline). [`llms.txt`](llms.txt) is the short index.

## How a film gets made

```
brief ──> shot list ──> stills ──> animatic ──> animation ──> sound ──> critique loop ──> master
          (gate)                    (960x540)                (earshot)   (8+ on every score)
```

| Step | What the agent does | Uses |
|---|---|---|
| Intake | Asks at most 3 questions: message, duration, format, look, music, deliverable | `brand/BRAND.md` |
| Engine | HyperFrames for most films; cinetic for full launch films; video-shotcraft for real-site promos | see table below |
| Brief | Copies and fills the director's brief, writes the shot list on the beat grid | `briefs/DIRECTOR_BRIEF.md`, `scripts/beats.py` |
| Build | Stills first, then motion; deterministic, seek-safe, no network at render | the engine's own skill |
| Sound | Optional Phonon voiceover first (it sets shot timing), then earshot effects on measured onsets, mastered to -14 / -18 LUFS | `scripts/phonon_say.py`, `templates/score.py` |
| Critique | Contact sheet + phone-size sheet + strip around the fastest moment, scored 1-10 | `scripts/qa-sheets.*`, `prompts/critique-pass.txt` |
| Deliver | MP4 master, ProRes 4444 overlay, re-laid-out aspect ratios, poster | |

## Install

1. Clone the kit. This folder is your studio; films go in `films/<slug>/`.
   ```bash
   git clone https://github.com/saiteja007-mv/motion-reel.git ~/motion-studio
   ```
2. Make the skill visible to your agent (copy or link `skills/motion-reel`):
   ```bash
   cp -r ~/motion-studio/skills/motion-reel ~/.claude/skills/    # Claude Code
   cp -r ~/motion-studio/skills/motion-reel ~/.agents/skills/    # Codex and other agents that read ~/.agents/skills
   ```
3. Tell the skill where the studio is: `export MOTION_STUDIO=~/motion-studio` (or just open the agent in that folder).
4. Install the engines you want (below), then fill in your brand:
   ```bash
   cp brand/BRAND.template.md brand/BRAND.md
   ```
5. Ask the agent: *"/motion-reel a 20-second 16:9 intro for my channel"*.

## Dependencies

Install each from its own repo; this kit only orchestrates them.

| Tool | Role | Licence |
|---|---|---|
| [HyperFrames](https://github.com/heygen-com/hyperframes) | Default engine: HTML + GSAP compositions rendered to video (`npx hyperframes`) | Apache-2.0 |
| [cinetic](https://github.com/Leonxlnx/cinetic) | Full launch films with brand build, motion blur and a ship gate | MIT |
| [video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) | Remotion promos built from real page screenshots and 2.5D camera moves | Apache-2.0 (Remotion has its own licence terms) |
| [earshot](https://github.com/Leonxlnx/earshot) | Synthesized sound effects with measured onsets and peaks; set `EARSHOT_PYTHON` to its venv python | MIT |
| [Phonon](https://github.com/gradium-ai/xn-ptts) (`pip install ptts`) | Optional local voiceover on CPU; set `PHONON_PYTHON`, or use `uv run --with ptts` | MIT/Apache-2.0 code; 31M model Apache-2.0, 40M models CC BY-NC 4.0 |
| colorfigures | Isometric "how does X work" objects (optional skill) | MIT |
| [ffmpeg](https://ffmpeg.org) | QA sheets, encoding, loudness | |
| Python + [librosa](https://librosa.org) | `scripts/beats.py` | |
| Node 18+ | HyperFrames and Remotion | |

Optional references (prompt ideas, motion vocabulary): see [`references/README.md`](references/README.md).

## Repo map

| Path | What |
|---|---|
| [`AGENTS.md`](AGENTS.md) | House rules: render contract, look, sound, critique loop, never-do list. `CLAUDE.md` imports it. |
| [`skills/motion-reel/SKILL.md`](skills/motion-reel/SKILL.md) | The skill an agent loads: intake, engine choice, build, sound, critique, delivery |
| [`brand/BRAND.template.md`](brand/BRAND.template.md) | Fill-in brand: message, audience, looks (palette, type), assets, rules |
| [`briefs/DIRECTOR_BRIEF.md`](briefs/DIRECTOR_BRIEF.md) | Brief template with spec, beat sheet, text on screen and gated workflow |
| [`prompts/critique-pass.txt`](prompts/critique-pass.txt) | The harsh-director scoring prompt |
| [`scripts/beats.py`](scripts/beats.py) | `python scripts/beats.py track.wav > beats.json`: bpm, beats, downbeats, hits |
| [`scripts/qa-sheets.ps1`](scripts/qa-sheets.ps1) / [`.sh`](scripts/qa-sheets.sh) | Contact, phone and strip sheets plus a loop check, into `out/qa/` |
| [`scripts/phonon_say.py`](scripts/phonon_say.py) | Voiceover lines with Phonon; refuses the non-commercial 40M models by default |
| [`templates/score.py`](templates/score.py) | Places earshot takes and voiceover WAVs on cue times, writes `score.wav` |

## Rules worth knowing before you start

- **Deterministic or it doesn't ship:** no CSS transitions, timers or `requestAnimationFrame` driving motion; seeded noise only.
- **Real UI only:** product screens are captured, never generated.
- **Banned defaults:** centered title on a gradient, everything fading in, corner labels, glow on UI, particle bursts, sparkles meaning "AI".
- **Sound restraint:** one soft sound per text fragment, one clean hit on the lockup, no risers.
- **No publishing:** the agent hands you files. It never uploads or posts.

## Credits

Pipeline inspired by Movez's course *How to build a motion design studio with Opus 5.5* (Sep 2026); the
wording, rules and scripts here are this repo's own. Engines and references belong to their authors, linked above.

## Licence

[MIT](LICENSE) for this kit. Dependencies keep their own licences.
