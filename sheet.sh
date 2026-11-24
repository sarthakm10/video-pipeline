#!/bin/bash
# Contact sheets of each slide's last step (2x3 per sheet) for quick checks: work/<m>/sheet_N.png
m=$1; d=work/$m; t=$d/_last; rm -rf $t; mkdir -p $t; i=0
for s in $(ls $d/s[0-9][0-9]_*.png | sed 's#.*/\(s[0-9]*\)_.*#\1#' | sort -u); do
  i=$((i+1)); cp $(ls $d/${s}_*.png | tail -1) $t/$(printf %03d $i).png
done
FF=${FFMPEG_DIR:-C:/Users/sarth/AppData/Local/Programs/UiPath/Studio/ffmpeg}/ffmpeg
rm -f $d/sheet_*.png
$FF -loglevel error -y -i $t/%03d.png -vf "scale=960:540,tile=2x3" $d/sheet_%d.png
ls $d/sheet_*.png
