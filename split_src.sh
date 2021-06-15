ffmpeg -i "$1" -c copy -map 0 -segment_time 00:10:00 -f segment -reset_timestamps 1 "${1%.*}"-Part-%03d.mp4
