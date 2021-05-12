import json, os, random, ffmpeg
import moviepy.editor as mp
from moviepy.video.fx import all
from moviepy.config import change_settings
from numpy import short


class EditClip:
    def __init__(self):
        pass

    def shortify():
        with open("shorts_post_info.json", 'r') as clip_list:
            data = json.load(clip_list)
            for clip_number in data:
                clip_info = data[clip_number]
                clip_name = clip_info['link']
                clip_info['length']
                                    
                if (int(clip_info['length']) in range(5,59)) and (clip_info['edited'] == False):
                    EditClip.make_short(clip_info)
                    clip_info['edited'] = True
                else:
                    clip_info['delete'] = True

        with open('shorts_post_info.json', 'w') as clip_list:
            json.dump(data, clip_list, indent=4)

    def clip_has_sound(clip_info):
        probe_info = ffmpeg.probe(f"Shorts/Downloaded/{clip_info['date']}/{clip_info['link']}.mp4")
        level_down = probe_info['streams']
        clip_has_audio = False
        for x in level_down:
            if x['codec_type'] != 'audio':
                continue
            elif x['codec_type'] == 'audio':
                clip_has_audio = True
        return clip_has_audio

    def make_short(clip_info):
        background_clip = mp.VideoFileClip("Boilerplate/color.mp4")
        main_clip = mp.VideoFileClip(f"Shorts/Downloaded/{clip_info['date']}/{clip_info['link']}.mp4")
        if main_clip.w * 16 > main_clip.h * 9:
            main_clip = main_clip.resize(width=1080)
        else:
            main_clip = main_clip.resize(height=1920)

        main_clip = main_clip.set_position("center")
        composite_clip = mp.CompositeVideoClip([background_clip, main_clip])

        if EditClip.clip_has_sound(clip_info) == False:
            print('this clip has no audio')
            background_song = mp.AudioFileClip(f"Boilerplate/FunnyMusic/{random.choice(os.listdir('Boilerplate/FunnyMusic'))}")
            composite_clip = composite_clip.set_audio(background_song)

        final_clip = composite_clip.set_duration(int(clip_info['length']))

        if not os.path.exists(f"Shorts/Edited/{clip_info['date']}"):
            os.makedirs(f"Shorts/Edited/{clip_info['date']}")
        
        final_clip.write_videofile(f"Shorts/Edited/{clip_info['date']}/{clip_info['link']}.mp4")
    

        



if __name__ == '__main__':
    EditClip.shortify()