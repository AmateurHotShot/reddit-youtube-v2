from youtube_uploader_selenium import YouTubeUploader
import json



class PostClips:
    def __init__(self):
        pass

    def postify():
        with open("shorts_post_info.json", 'r') as clip_list:
                data = json.load(clip_list)
                for clip_number in data:
                    clip_info = data[clip_number]
                                        
                    if (clip_info['edited'] == True) and (clip_info['published'] == False) and (clip_info['delete'] == False):
                        PostClips.find_and_replace(clip_info)
                        video_path = f"Shorts/Edited/{clip_info['date']}/{clip_info['link']}.mp4"
                        metadata_path = 'youtube_post.json'
                        uploader = YouTubeUploader(video_path, metadata_path)
                        was_video_uploaded, video_id = uploader.upload()
                        assert was_video_uploaded
                        clip_info['published'] = True
                        clip_info['delete'] = True
                    else:
                        clip_info['delete'] = True
        

    def find_and_replace(clip_info):

        with open('youtube_post.json', 'r+') as file:
            data = json.load(file)
            data['title'] = f"{clip_info['title']} - CyberClips #shorts"
            data['description'] = PostClips.description_replace(clip_info)
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def description_replace(clip_info):
        with open('Boilerplate/YouTubePostData/description.txt', 'r') as file:
            comment_list = str('\n'.join(clip_info['comments']))
            descr_temp = file.read()
            descr_temp = descr_temp.replace('[title]', clip_info['title'])
            final_description = descr_temp.replace('[comments]', comment_list)
            return final_description


if __name__ == "__main__":
    PostClips.postify()