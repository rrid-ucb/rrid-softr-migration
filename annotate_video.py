#!/usr/bin/env python3
import json, re, sys
from pathlib import Path

def load_segments(p):
    data = json.loads(Path(p).read_text())
    # Try common Whisper JSON shapes
    if "segments" in data and isinstance(data["segments"], list):
        return [{"id": s.get("id"), "start": float(s["start"]), "end": float(s["end"]), "text": s.get("text","").strip()} for s in data["segments"]]
    if "transcription" in data:
        # whisper.cpp older shape can wrap segments inside transcription[0].segments
        t = data["transcription"]
        if isinstance(t, list) and t and isinstance(t[0], dict) and "segments" in t[0]:
            return [{"id": s.get("id"), "start": float(s["start"]), "end": float(s["end"]), "text": s.get("text","").strip()} for s in t[0]["segments"]]
    raise ValueError("Could not find segments in transcript JSON")

def parse_pts_times(log_path):
    # Collect pts_time in the order frames were written
    pts = []
    rgx = re.compile(r"pts_time:(\d+(?:\.\d+)?)")
    for line in Path(log_path).read_text().splitlines():
        m = rgx.search(line)
        if m:
            pts.append(float(m.group(1)))
    return pts

def hhmmss(t):
    m, s = divmod(int(round(t)), 60)
    h, m = divmod(m, 60)
    if h: return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

def main(video, transcript_json, frames_dir, frames_log, out_dir):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    segs = load_segments(transcript_json)
    frames = sorted(Path(frames_dir).glob("frame_*.jpg"))
    pts_times = parse_pts_times(frames_log)

    # Pair frames with pts times in order
    n = min(len(frames), len(pts_times))
    frames = frames[:n]
    pts_times = pts_times[:n]
    frame_entries = [{"path": str(f), "time": t} for f, t in zip(frames, pts_times)]

    def nearest_frame(t0, t1=None):
        # Prefer frames whose time falls in [t0, t1]; else nearest to t0
        if t1 is not None:
            in_win = [fe for fe in frame_entries if t0 <= fe["time"] <= t1]
            if in_win:
                # choose the earliest in window
                return sorted(in_win, key=lambda x: x["time"])[0]
        # fallback: nearest to start
        return min(frame_entries, key=lambda x: abs(x["time"] - t0)) if frame_entries else None

    annotated = []
    for s in segs:
        f = nearest_frame(s["start"], s["end"])
        annotated.append({
            "id": s["id"],
            "start": s["start"],
            "end": s["end"],
            "start_hms": hhmmss(s["start"]),
            "end_hms": hhmmss(s["end"]),
            "text": s["text"],
            "frame": f
        })

    Path(out / "annotated.json").write_text(json.dumps({
        "video": video,
        "transcript": transcript_json,
        "frames_dir": frames_dir,
        "items": annotated
    }, indent=2))

    # Markdown
    md = [f"# Annotated transcript — {Path(video).name}", ""]
    for item in annotated:
        ts = item["start_hms"]
        text = item["text"]
        md.append(f"## {ts}")
        if item["frame"]:
            rel = Path(item["frame"]["path"])
            md.append(f"![{ts}]({rel})")
            md.append(f"<sub>frame at ~{hhmmss(item['frame']['time'])}</sub>")
        md.append("")
        md.append(text)
        md.append("")
        md.append("---")
        md.append("")
    Path(out / "annotated.md").write_text("\n".join(md))

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: annotate_video.py <video.mp4> <transcript.json> <frames_dir> <frames.log> <out_dir>", file=sys.stderr)
        sys.exit(2)
    main(*sys.argv[1:6])
