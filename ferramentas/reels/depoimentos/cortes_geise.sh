#!/bin/bash
# Cortes do depoimento da Geise (sem cenas com marcas de terceiros).
# Uso: bash cortes_geise.sh video_original.mp4 pasta_saida
# Usa as artes de tmp/ geradas por montar_geise.py (ov.png, ovs.png, cta.png).
# Pausas da fala usadas como pontos de corte: 26.0, 46.05, 59.55; Sâny fala de 59.85 a 70.4.
# De 51.2 a 59.55 a Geise segue falando sobre cenas do evento com marcas de terceiros:
# a imagem é trocada pelo drone de Mariana (0 a 8.35 s).
set -e
SRC=$1; OUT=$2; T=$(cd "$(dirname "$0")" && pwd)/tmp; P=$T/partes; mkdir -p "$OUT" "$P"
V="crop=ih*9/16:ih,scale=1080:1920,setsar=1,fps=30,format=yuv420p"
VE="-c:v libx264 -crf 21 -preset veryfast"
AE="-c:a aac -b:a 160k -ar 48000 -ac 2"
# partes de vídeo (sem áudio), com a faixa do nome
vid() { ffmpeg -loglevel error -y -ss $1 -to $2 -i "$SRC" -i $T/$3 -filter_complex "[0:v]$V[v];[v][1:v]overlay=0:0" -an $VE $P/$4; }
vid 8.125 51.208 ov.png g1.mp4
vid 0 8.342 ov.png drone.mp4
vid 46.05 51.208 ov.png g3.mp4
vid 8.125 26.0 ov.png s1.mp4
vid 26.0 46.05 ov.png s2.mp4
vid 59.85 70.4 ovs.png sany.mp4
ffmpeg -loglevel error -y -loop 1 -t 4 -i $T/cta.png -vf "fps=30,format=yuv420p,fade=in:st=0:d=0.3" $VE $P/cta.mp4
aud() { ffmpeg -loglevel error -y -ss $1 -to $2 -i "$SRC" -vn -af "afade=out:st=$(echo "$2-$1-0.4"|bc):d=0.4" $AE $P/$3; }
juntar() { # saída, áudio, vídeos...
  local saida=$1 audio=$2; shift 2; : > $P/l.txt; for f in "$@"; do echo "file '$P/$f'" >> $P/l.txt; done
  ffmpeg -loglevel error -y -f concat -safe 0 -i $P/l.txt -c copy $P/v.mp4
  ffmpeg -loglevel error -y -i $P/v.mp4 -i $audio -af "apad,loudnorm=I=-14:TP=-1.5:LRA=9" -shortest -c:v copy $AE -movflags +faststart "$OUT/$saida"; }
# Reel curto: Geise (com drone sob a voz) + Sâny + card do diagnóstico
aud 8.125 59.55 ag.m4a; aud 59.85 70.4 as.m4a
ffmpeg -loglevel error -y -f lavfi -t 4 -i anullsrc=r=48000:cl=stereo $AE $P/ac.m4a
: > $P/la.txt; for f in ag.m4a as.m4a ac.m4a; do echo "file '$P/$f'" >> $P/la.txt; done
ffmpeg -loglevel error -y -f concat -safe 0 -i $P/la.txt -c copy $P/areel.m4a
juntar reel-depoimento-geise-curto.mp4 $P/areel.m4a g1.mp4 drone.mp4 sany.mp4 cta.mp4
# Stories
aud 8.125 26.0 a1.m4a; juntar story-geise-1.mp4 $P/a1.m4a s1.mp4
aud 26.0 46.05 a2.m4a; juntar story-geise-2.mp4 $P/a2.m4a s2.mp4
aud 46.05 59.55 a3.m4a; juntar story-geise-3.mp4 $P/a3.m4a g3.mp4 drone.mp4
# Trecho horizontal para a página do diagnóstico do site
ffmpeg -loglevel error -y -ss 8.125 -to 26.0 -i "$SRC" -vf "scale=1280:-2" -af "afade=out:st=17.5:d=0.4" -c:v libx264 -crf 26 -preset medium -pix_fmt yuv420p -c:a aac -b:a 112k -ac 2 -movflags +faststart "$OUT/geise-trecho-diagnostico.mp4"
for f in "$OUT"/*.mp4; do echo "$(basename $f) $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)s $(du -h $f | cut -f1)"; done
