import sys 
import subprocess 
import shutil
import os

def run_command(cmd): 
    subprocess.call(['echo'] + cmd)
    subprocess.call(cmd)



def get_audio_video_filenames(video_src, tmp_dirname): 
    # original video filename (stripped off of path) 
    orig_vid_file = os.path.basename(video_src) 
    base_sans_ext = os.path.splitext(orig_vid_file)[0] 


    # take out the video file and save name 
    video_file = os.path.join(tmp_dirname, base_sans_ext + "-vid.mp4") 
    run_command(['ffmpeg', '-i', video_src, '-c:v', 'copy', '-an', video_file]) 

    # take out the audio file 
    audio_file = os.path.join(tmp_dirname, base_sans_ext + "-aud.wav") 
    run_command(['ffmpeg', '-i', video_src, '-c:v', 'copy', '-vn', audio_file]) 

    # create output_video filename 
    output_video = os.path.join(tmp_dirname, base_sans_ext + ".mkv")

    return (audio_file, video_file, output_video, orig_vid_file) 

def main(): 
    # change directory to working to keep main dir clean  
    tmp_dirname = "temp" 
    try: 
        os.mkdir(tmp_dirname)
    except FileExistsError: 
        pass 

    video_src = sys.argv[1]

    print("Splitting video ... ") 

    # find the filename of the newly retrieved m4a and mp4 (video only) 
    audio_file, video_file, output_video, orig_vid_file = get_audio_video_filenames(video_src, tmp_dirname) 

    print("Converting using spleeter ... ") 
    run_command(['spleeter', 'separate', '-p', 'spleeter:2stems', '-o', os.path.join(tmp_dirname, 'output'), '-f', "{instrument}.{codec}", audio_file]) 

    # find output auido filename 
    output_audio = os.path.join(tmp_dirname, 'output', 'vocals.wav')


    print("Merging audio and video ... ") 
    run_command(['ffmpeg', '-i', video_file, '-i', output_audio, '-c', 'copy', output_video]) 
   

    # housekeeping 
    shutil.move(output_video, "./") 
    os.remove(audio_file)
    os.remove(video_file)
    os.remove(video_src)
    shutil.rmtree(os.path.join(tmp_dirname, "output")) 

    print("-" * 20) 
    print("Ready:", output_video) 
    print("-" * 20) 




if __name__ == '__main__': 
    if len(sys.argv) == 1: 
        print("Please provide filename to convert.")
        sys.exit(1) 
    main() 
