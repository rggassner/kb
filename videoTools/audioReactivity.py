#!/usr/bin/python3
import numpy as np
import math,os,shutil
import moviepy.editor as mpy
from scipy.io import wavfile

imgs_path_in='inframes'
imgs_path_out="outframes"
path_to_audio="input.mp3"
vid_fps=30
speed_multiply = 1
#my_speed_map = [1,1,2,4,8,9,10,10,10,10]
my_speed_map  = [1,1,2,4,8,9,10,10,10,10]

def convert_audio():
    audio_clip = mpy.AudioFileClip(path_to_audio)
    audio_clip.write_audiofile('./temp_audio.wav', fps=44100, nbytes=2, codec='pcm_s16le')

def get_signal_rate():
    rate, signal = wavfile.read('./temp_audio.wav')
    signal = np.mean(signal, axis=1)
    signal = np.abs(signal)
    return signal,rate

def get_volume(signal,rate,audio_frames):
    samples_per_frame = signal.shape[0] / audio_frames
    volume = []
    for frame in range(audio_frames):
        start = int(round(frame * samples_per_frame))
        stop = int(round((frame + 1) * samples_per_frame))
        v = np.mean(signal[start:stop], axis=0)
        volume.append(v)
    volume_max = max(volume)
    for i in range(audio_frames):
        volume[i] = round(volume[i] / volume_max,3)
    return volume

def get_audio_frame_count(signal,rate):
    duration = signal.shape[0] / rate
    audio_frames = int(np.ceil(duration * vid_fps))
    return audio_frames

def get_speed_map():
    speed_map = []
    for i in my_speed_map:
        i = math.ceil(i * speed_multiply)
        speed_map.append(i)
    return speed_map

def get_input_video_frames():
    input_video_frames = [f for f in os.listdir(imgs_path_in) if os.path.isfile(os.path.join(imgs_path_in, f))]
    input_video_frames.sort()
    return input_video_frames

def get_out_frames(volume,input_video_frames,speed_map):
    out_frames = []
    frame_count = 0
    for i, v in enumerate(volume):
        if i > len(input_video_frames):
            break
        v = volume[i] # 0...1
        idx = v * len(speed_map)        
        idx = math.floor(idx)             
        idx = min(idx,len(speed_map)-1)  
        speed = speed_map[idx]             
        frame_count += speed
        if frame_count > len(input_video_frames):
            break
        out_frames.append(input_video_frames[frame_count-1])
    return out_frames

def copy_out_frames(out_frames):
    for i in out_frames:
        shutil.copyfile(imgs_path_in+"/"+i,imgs_path_out+"/"+i)
    
speed_map=get_speed_map()
convert_audio()
signal,rate=get_signal_rate()
audio_frames=get_audio_frame_count(signal,rate)
volume=get_volume(signal,rate,audio_frames)
input_video_frames=get_input_video_frames()
out_frames=get_out_frames(volume,input_video_frames,speed_map)
print("Output will have {} frames, based on audio length.".format(audio_frames))
if len(out_frames) < audio_frames:
    print("Not all video frames will be used. Video frames:{} Audio frames:{}.\nYou could decrease speed_multiply.".format(len(out_frames),audio_frames))
copy_out_frames(out_frames)
print('ffmpeg -y -framerate {} -pattern_type glob -i "{}/*.png" -c:v libx264 -r {} -pix_fmt yuv420p temp_video.mp4;ffmpeg -y -i temp_video.mp4 -i temp_audio.wav -map 0:v -map 1:a -c:v copy -shortest audio-reactive-video.mp4'.format(vid_fps,imgs_path_out,vid_fps))
