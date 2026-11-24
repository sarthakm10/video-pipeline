# Builds an explainer video from a spec: slides with step-by-step reveals, each step narrated by Kokoro (af_heart).
# Usage: py build.py c_sw          (reads specs/spec_c_sw.py, writes out/<FILE>)
#        py build.py c_sw slides   (preview: slide images only, in work/c_sw/)
# FFMPEG_DIR, BROWSER and VCODEC can be set in the environment (GitHub Actions does); the defaults are for this laptop.
import hashlib, importlib, os, subprocess, sys

import soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "specs"))
sys.path.insert(0, HERE)
FF = os.environ.get("FFMPEG_DIR", "C:/Users/sarth/AppData/Local/Programs/UiPath/Studio/ffmpeg")
EDGE = os.environ.get("BROWSER", "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
VCODEC = os.environ.get("VCODEC", "libopenh264")  # CI uses libx264
VOICE, SPEED = "af_heart", 1.0
TEMPLATE = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
_tts = None


def tts(text, path):
    global _tts
    if os.path.exists(path):
        return
    if _tts is None:
        _tts = Kokoro(os.path.join(HERE, "models", "kokoro-v1.0.onnx"), os.path.join(HERE, "models", "voices-v1.0.bin"))
    samples, sr = _tts.create(text, voice=VOICE, speed=SPEED, lang="en-us")
    sf.write(path, samples, sr)


def duration(path):
    out = subprocess.check_output([FF + "/ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out.strip())


def render(html, step, path, meta):
    page = (TEMPLATE.replace("{{BODY}}", html).replace("{{STEP}}", str(step))
            .replace("{{TAG}}", meta["tag"]).replace("{{TRACK}}", meta.get("track", "Java Fullstack · Frontend")).replace("{{PROGRESS}}", meta["progress"]))
    hp = path[:-4] + ".html"
    open(hp, "w", encoding="utf-8").write(page)
    subprocess.run([EDGE, "--headless=new", "--user-data-dir=" + os.path.join(HERE, "edge-profile-" + str(os.getpid())), "--disable-gpu",
                    "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=1920,1080",
                    "--screenshot=" + path, "file:///" + hp.replace("\\", "/")], check=True, capture_output=True)


def main(name, only=None):
    spec = importlib.import_module("spec_" + name)
    work = os.path.join(HERE, "work", name)
    os.makedirs(work, exist_ok=True)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    jobs = []
    for si, slide in enumerate(spec.SLIDES):
        for st, narr in enumerate(slide["steps"]):
            pause = 0
            if isinstance(narr, tuple):
                narr, pause = narr
            jobs.append((si, st, narr, pause, slide["html"]))
    total = len(spec.SLIDES)
    if only == "slides":  # preview: render every step's image, no audio or video
        for si, st, _, _, html in jobs:
            render(html, st, os.path.join(work, f"s{si:02d}_{st:02d}.png"), {"tag": spec.TAG, "track": getattr(spec, "TRACK", "Java Fullstack · Frontend"), "progress": f"{100*(si+1)/total:.1f}%"})
        print("slides rendered:", len(jobs))
        return
    segs = []
    for n, (si, st, narr, pause, html) in enumerate(jobs):
        audio = os.path.join(work, "a_" + hashlib.sha1(narr.encode()).hexdigest()[:12] + ".wav")
        tts(narr, audio)
        img = os.path.join(work, f"s{si:02d}_{st:02d}.png")
        render(html, st, img, {"tag": spec.TAG, "track": getattr(spec, "TRACK", "Java Fullstack · Frontend"), "progress": f"{100*(si+1)/total:.1f}%"})
        dur = duration(audio) + 0.35 + 0.5 + pause
        seg = os.path.join(work, f"seg{n:03d}.mp4")
        vf = "fade=in:st=0:d=0.35," if st == 0 else ""
        subprocess.run([FF + "/ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-i", img, "-i", audio,
                        "-t", f"{dur:.3f}", "-vf", vf + "format=yuv420p", "-af", "adelay=350:all=1,apad",
                        "-c:v", VCODEC, "-b:v", "2500k", "-r", "30",
                        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", seg], check=True)
        segs.append(seg)
        print(f"  step {n+1}/{len(jobs)}  slide {si+1}  {dur:.1f}s", flush=True)
    lst = os.path.join(work, "list.txt")
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    out = os.path.join(HERE, "out", spec.FILE)
    subprocess.run([FF + "/ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    "-movflags", "+faststart", out], check=True)
    print(f"DONE {spec.FILE}  {duration(out)/60:.1f} min  {os.path.getsize(out)/1048576:.1f} MB", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
