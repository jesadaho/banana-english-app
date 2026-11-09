---
name: render-achievement-badges
description: Produce Banana English achievement assets individually with a fixed master frame, never by cropping a sheet.
---

# Achievement Badge Renderer

## Mandatory: render ONE badge at a time
- Generate each achievement's motif as a SEPARATE image. Never ask an image model for a grid, collage, or contact sheet as the production source.
- NEVER crop a combined sheet to extract badges. Preview sheets may be made only AFTER individual PNGs are completed and validated.
- Use ONE deterministic, reusable rounded-square master frame (SVG/Pillow) for all achievements. AI-generated independent frames will not reliably match, so generate the motif independently and composite it into the master frame.
- If a motif is wrong or low quality, regenerate that ONE motif. Do not stretch, warp or crop a finished badge to conceal a bad frame.

## Approved visual design
- Follow approved Explorer v2 individual render style, not the old cropped concept sheet. Check actual references before claiming a visual match.
- Rounded square, soft 3D, thick ivory/cream beveled frame, warm cream gradient face, colorful clay-like centered motif; front-on view, consistent upper-left lighting, subtle shadow.
- Frame, padding, gradient, bevel, silhouette and light direction MUST match exactly across all 27.
- No text, labels, checkmarks, progress rings, locks, or metallic casino effects baked into assets.
- Export 1024x1024 transparent RGBA PNG; transparency OUTSIDE badge, no checkerboard pixels, 6-10% safe margin.

## Canonical catalog: 27 IDs, not 29
The following IDs come from the user's ACHIEVEMENT_CATALOG. Never invent other badges or substitute categories.

### getting_started
- `first_hello`
- `first_lesson`
- `first_mission`
- `beginner`

### learning
- `study_time`
- `bookworm`
- `scholar`
- `banana_graduate`
- `clear_voice`

### speaking
- `say_hello`
- `talkative`
- `smooth_speaker`
- `conversation_master`

### consistency
- `streak_3`
- `streak_7`
- `streak_14`
- `streak_30`

### skill
- `crystal_clear`
- `no_hint_hero`
- `english_only`
- `perfect_mission`
- `perfect_drill`

### explorer
- `daily_life_explorer`
- `travel_explorer`
- `social_explorer`
- `work_career_explorer`
- `survival_explorer`

## Per-file production process
1. Load approved Explorer v2 reference and a single deterministic master frame. If missing, request the reference rather than silently changing style.
2. For each ID, plan a unique motif appropriate to its actual achievement condition, then render that motif individually.
3. Remove unwanted background from the MOTIF only if necessary; never remove background from cropped badge sheets.
4. Composite each individual motif inside the fixed master frame using fixed safe bounds and preserving aspect ratio.
5. Export `achievement-badges/<category>/<id>.png` as true RGBA 1024x1024.
6. Automated QA for EACH file: exact dimensions, transparent corners, alpha bounding box centered, identical master frame geometry, no clipping or checkerboard leakage.
7. Inspect each at 80px and 100px on the Banana English cream profile background. Reject any mismatched motif, misaligned frame, or poor legibility.
8. Upload ONLY verified individual files into a NEW versioned Google Drive folder with category subfolders; do not overwrite previous assets.
9. A contact sheet is allowed for review only after individual assets pass QA; never use it to generate deliverables.
10. Report exact number of individual assets rendered, verified, and uploaded; do not claim completion without confirming all 27 files.

## Output
`achievement-badges/<category>/<achievement_id>.png` — 27 distinct 1024x1024 RGBA PNGs.
