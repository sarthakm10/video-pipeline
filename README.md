# video-pipeline

Turns a spec (`specs/spec_<name>.py`) into a narrated explainer video:
HTML slides → headless Edge screenshots → Kokoro TTS (af_heart) → ffmpeg.

## Render on GitHub Actions

Actions → **Render videos** → Run workflow → enter spec names, e.g. `c_gra,c_mta,c_spc`.
Each spec renders in its own job. The MP4 appears as a downloadable artifact on the run (kept 7 days).

Tick **upload** to also push it to the `videos` release of `sarthakm10/java_60_days`.
That needs a repo secret `RELEASE_TOKEN`: a fine-grained token with *Contents: read and write* on `java_60_days` only.

## Render locally

```
pip install -r requirements.txt
# put kokoro-v1.0.onnx and voices-v1.0.bin in models/
py build.py c_sw          # full video → out/
py build.py c_sw slides   # slide images only → work/c_sw/
```

`FFMPEG_DIR`, `BROWSER` and `VCODEC` override the laptop defaults in `build.py`.
