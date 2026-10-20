---
name: render-level-badges
description: Render consistent Banana English proficiency hexagon badges for Seed, Seed+, A1, A1+, A2, A2+, and B1.
---

# Render Level Badges

## Mandatory background context
Before rendering, inspect the approved **My Growth Hero Card background** reference. The user-approved reference is a warm ivory/cream and soft banana-yellow abstract gradient with pale sweeping arcs, delicate thin white curved lines and very subtle light dots; strongest yellow is at lower right, central area remains bright and uncluttered. The source reference was supplied in the 2026-10-20 conversation as `image(20261020-054832).png`. If a copy is committed into the repository, read that asset rather than approximating from this description. **Do not claim to have read an asset that is not accessible.**

The badges are displayed ON TOP of this cream/yellow Hero Card. Every badge must contrast clearly against that background: use a defined darker inner colored face, ivory outer bevel, subtle shadow, and readable text. Do not render yellow-on-yellow. Never bake the Hero Card background into the badge PNG: transparent RGBA only. For visual QA, composite the badge over the approved background and check at 96px and 160px.

## Level manifest (never forget A1)
| id | label | color family | motif |
| --- | --- | --- | --- |
| seed | Seed | fresh green | tiny sprout |
| seed_plus | Seed+ | emerald green | stronger sprout + small gold plus |
| a1 | A1 | teal | leaf |
| a1_plus | A1+ | turquoise | two leaves |
| a2 | A2 | sky blue | rising leaf |
| a2_plus | A2+ | richer blue | rising leaf with small accent |
| b1 | B1 | violet | laurel |

The manifest is a proposed visual mapping, not a formal CEFR mapping for Seed. Confirm with the product owner before adding or renaming levels.

## Visual specification
- Premium playful EdTech, minimal premium soft-flat design; no embossed or extruded text, no casino/VIP metallic.
- One master rounded hexagon silhouette, identical perspective, border thickness, padding, bevel, light direction and text baseline across ALL ranks.
- Text-first: exact level label visually dominant (~60%), small symbolic motif (~40%). Plus signs must be clearly readable.
- 1024x1024 WebP with actual alpha transparency, centered and 8% safe margin. Preserve PNG only if explicitly requested.
- No checkerboard pixels, background scenery, extra text or watermarks.
- Keep special effects restrained. Plus variant may have a small premium accent but not a different base shape.

## Non-negotiable: never crop a composite preview
Previous exports failed because slicing a 7-badge composite produced misaligned, skewed outlines and leaked cream/yellow background. NEVER extract production badges by cropping a contact sheet, and NEVER use background removal on such crops.

Generate each level as its OWN complete square asset, not one group image. However, independent AI generations alone do NOT guarantee identical geometry: use one deterministic master hexagon path/mask with fixed white outer border, colored band, thin white inner border, gradient face and typography positions. Build the master frame with vector geometry and rasterize individually to transparent WebP. If AI is used, restrict it to optional inner motif artwork; clip that artwork to the master shape. Do not use AI-generated border geometry.

Use a flat text-first design with optional small flat motif above the large label, consistent with the user's approved pale-gradient, double-white-outline reference. Do not include a decorative motif when rendering a text-only variant. No faux 3D offset or misaligned white border.

Before packaging, run automated QA on EACH file: 1024x1024, RGBA transparency outside shape, centered alpha bounding box, matching hexagon silhouette and border geometry across all seven, no clipping, no cream BG leakage. Compare all alpha masks programmatically. Inspect at actual app sizes (96px and 160px). Any failure must be fixed before exporting the ZIP. Preview/contact sheet is generated ONLY AFTER individual assets pass QA.

## Production workflow
1. Load the master frame and approved My Growth BG reference. If the BG reference is missing, request/locate it; never silently substitute another background.
2. Generate consistent variants using the same geometry, adjusting only palette, motif and plus accents.
3. Prefer deterministic compositing for EXACT typography (SVG/Pillow) over relying on image model text. Use large, flat, bold sans-serif letters with high contrast and no extrusion.
4. Export each level as a separate transparent WebP: `seed.webp`, `seed_plus.webp`, `a1.webp`, `a1_plus.webp`, `a2.webp`, `a2_plus.webp`, `b1.webp`.
5. Create a contact sheet `preview.webp` including the badges over the approved BG at realistic UI size.
6. QA each file: expected text, plus sign, alpha, dimensions, safe bounds, consistent silhouette, and legibility on cream/yellow.
7. Never claim a batch or file exists without verifying its actual output.

## Output
`level-badges/{seed,seed_plus,a1,a1_plus,a2,a2_plus,b1,preview}.webp`
