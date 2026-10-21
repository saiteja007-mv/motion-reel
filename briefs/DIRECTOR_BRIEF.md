# Director's brief: [FILM TITLE]

You are the director, animator, sound designer and render engineer for a [DURATION] film made in code,
in `films/[slug]/`. Follow the studio rules in `../../AGENTS.md` and the brand in `../../brand/BRAND.md`.
Treat this as a multi-step production with gates. Don't rush to a final render.

## The film in one line
[LOGLINE. What the viewer should feel or know at the end.]

## Spec
- Format: [1920x1080 | 1080x1920 | 1080x1080] @ [24 | 30 | 60] fps, [DURATION] s. Other ratios: [none | 9:16, 1:1]
- Look: [a look name from the brand file]
- Engine: [HyperFrames | cinetic (Remotion) | cinetic (HyperFrames) | video-shotcraft (Remotion)]
- Audio: [earshot kit preset calm | crisp | minimal] + [no music | supplied ./audio/track.wav | synthesized]
- Delivery: [MP4 master | transparent overlay .mov for an editor | both]

## References and inputs
- `./refs/`: [video / frames / image folder]. Take the grammar (pacing, type, transitions), never the content.
- Footage / screenshots: [paths]. Real UI only.
- Tools available: skills `/hyperframes`, `/cinetic`, `/video-shotcraft`, `/earshot`, `/colorfigures`;
  NullMotion templates; [your video editor]. Images: [your configured image generator].
- Budget: [tokens / time / paid API spend]. Be economical.

## Look
[3-5 lines: palette, type, texture, camera language. Anything banned beyond the studio list.]

## Beat sheet
0:00-0:02  hook: [the single most striking image]
0:02-0:[..] [act 1]
...         a new visual payoff every 3-5 s
[END]       [lockup / CTA / the last frame sets up the first for a loop]

## Text on screen
[Every line of copy, split into fragments, with when it appears. Word count total: N.]

## Workflow, with gates
1. Write `docs/style_guide.md` (from refs) and `docs/shotlist.md` (every shot: frames, camera, text, SFX cue).
   Show the user the shot list before building.
2. Stills for every shot, then a contact sheet, then critique.
3. Animatic at 960x540 with placeholder sound. Fix pacing before polish.
4. Full animation, polish pass, sound pass (earshot cues on measured frames), final render.
5. For long films: write `docs/ANIMATION_GUIDE.md` first, then split chapters across subagents.

## Critique loop (every gate, at least 2 rounds)
Use `prompts/critique-pass.txt`. Log scores and the 3 biggest problems in `docs/review_log.md`. Fix. Repeat until all 8+.

## Deliverables
`out/final.mp4` · `out/poster.png` · `out/qa/contact.png` · [`out/overlay.mov`] · [`out/final_9x16.mp4`] ·
`README.md` with how to re-render and what to improve next.
