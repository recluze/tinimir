# Tinimir: Tiny Music Remover 

Author: recluze 

This little script uses [Spleeter](https://github.com/deezer/spleeter) and ffmpeg to remove music from any video. 

I use this script to download documentaries off of youtube (using youtube-dl), remove any music leaving voice narration in and put them in a local media server to be streamed during my kids' "video time". 

Limitaton: Spleeter has a default 10-minute limit. Any sound after that is essentially muted. A workaround is to split your original videos into 10-minute segments. 

To segment videos using ffmpeg, use the following: 

    ffmpeg -i "$1" -c copy -map 0 -segment_time 00:10:00 -f segment -reset_timestamps 1 "${1%.*}"-Part-%03d.mp4
