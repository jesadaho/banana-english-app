#!/usr/bin/env python3
"""Deterministic achievement badge assembler and checkpoint gate.

This script DOES NOT invoke an image model. Render one isolated motif image per ID,
then ingest it; the pipeline will never turn a contact sheet into assets.
Requires Pillow: pip install pillow
"""
import argparse
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

CATALOG = {
 "getting_started": ["first_hello","first_lesson","first_mission","beginner"],
 "learning": ["study_time","bookworm","scholar","banana_graduate","clear_voice"],
 "speaking": ["say_hello","talkative","smooth_speaker","conversation_master"],
 "consistency": ["streak_3","streak_7","streak_14","streak_30"],
 "skill": ["crystal_clear","no_hint_hero","english_only","perfect_mission","perfect_drill"],
 "explorer": ["daily_life_explorer","travel_explorer","social_explorer","work_career_explorer","survival_explorer"],
}
IDS = [i for ids in CATALOG.values() for i in ids]
CATEGORY = {i: c for c, ids in CATALOG.items() for i in ids}
SIZE = 1024

def frame():
    """One shared, deterministic ivory rounded-square frame for all 27."""
    im = Image.new("RGBA", (SIZE, SIZE))
    d = ImageDraw.Draw(im)
    # 8% transparent outer margin, consistent silhouette.
    box = (82, 82, 942, 942)
    d.rounded_rectangle((78, 87, 946, 950), radius=225, fill=(116, 78, 27, 28))
    d.rounded_rectangle(box, radius=220, fill=(244, 216, 167, 255))
    d.rounded_rectangle((87, 87, 937, 936), radius=215, fill=(255, 250, 235, 255))
    d.rounded_rectangle((109, 109, 915, 914), radius=200, fill=(248, 229, 192, 255))
    d.rounded_rectangle((137, 140, 887, 886), radius=175, fill=(255, 241, 212, 255))
    return im

def state_path(root):
    return root / "state.json"

def load_state(root):
    p = state_path(root)
    if p.exists():
        s = json.loads(p.read_text())
        if s.get("catalog") != IDS:
            raise ValueError("Catalog changed: refuse to resume with incompatible state")
        return s
    return {"catalog": IDS, "completed": [], "files": {}}

def save_state(root, s):
    root.mkdir(parents=True, exist_ok=True)
    state_path(root).write_text(json.dumps(s, ensure_ascii=False, indent=2) + "\n")

def next_id(s):
    return next((i for i in IDS if i not in s["completed"]), None)

def ingest(root, id, source):
    s = load_state(root)
    expected = next_id(s)
    if id != expected:
        raise ValueError(f"Checkpoint blocked: next required ID is {expected}, got {id}")
    if not source.is_file():
        raise FileNotFoundError(source)
    with Image.open(source) as src:
        if src.format != "PNG" or src.width < 512 or src.height < 512:
            raise ValueError("Source must be an individual PNG >=512x512")
        rgba = src.convert("RGBA")
    if rgba.getpixel((0, 0))[3] > 8 or rgba.getpixel((rgba.width-1, 0))[3] > 8:
        raise ValueError("Motif source corners are opaque; provide a transparent isolated motif, not a sheet")
    alpha = rgba.getchannel("A")
    bbox = alpha.getbbox()
    if not bbox:
        raise ValueError("Empty motif")
    # Reject obvious multi-panel composites; semantic review still mandatory.
    w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    if w < 64 or h < 64:
        raise ValueError("Motif too small")
    motif = rgba.crop(bbox)
    motif.thumbnail((570, 570), Image.Resampling.LANCZOS)
    base = frame()
    pos = ((SIZE-motif.width)//2, (SIZE-motif.height)//2)
    base.alpha_composite(motif, pos)
    dest = root / CATEGORY[id] / (id + ".png")
    dest.parent.mkdir(parents=True, exist_ok=True)
    base.save(dest)
    verify(dest)
    s["completed"].append(id)
    s["files"][id] = str(dest.relative_to(root))
    save_state(root, s)
    return dest

def verify(path):
    with Image.open(path) as im:
        if im.size != (SIZE, SIZE) or im.mode != "RGBA":
            raise ValueError(f"Invalid dimensions/mode: {path}")
        a = im.getchannel("A")
        for p in [(0,0),(1023,0),(0,1023),(1023,1023)]:
            if a.getpixel(p) != 0:
                raise ValueError(f"Opaque canvas corner: {path}")
        bbox = a.getbbox()
        if not bbox or min(bbox[0],bbox[1],SIZE-bbox[2],SIZE-bbox[3]) < 65:
            raise ValueError(f"Badge outside safe bounds: {path}")
    return True

def main():
    p=argparse.ArgumentParser()
    p.add_argument("command", choices=["init","next","ingest","verify","status"])
    p.add_argument("--root", type=Path, default=Path("achievement-badges-v3"))
    p.add_argument("--id")
    p.add_argument("--source", type=Path)
    a=p.parse_args()
    s=load_state(a.root)
    if a.command=="init":
        save_state(a.root,s)
    elif a.command=="next":
        print(next_id(s) or "COMPLETE")
    elif a.command=="ingest":
        if not a.id or not a.source:
            p.error("ingest requires --id and --source")
        print(ingest(a.root,a.id,a.source))
    elif a.command=="verify":
        for id in s["completed"]:
            verify(a.root / s["files"][id])
        print(f"Verified {len(s['completed'])}/27 individual files")
    elif a.command=="status":
        print(json.dumps({"completed":len(s["completed"]),"total":len(IDS),"next":next_id(s),"remaining":len(IDS)-len(s["completed"])},indent=2))
    if a.command=="init":
        print(f"Initialized {len(IDS)} IDs; next: {next_id(s)}")

if __name__=="__main__":
    main()
