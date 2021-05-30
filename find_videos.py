import praw
from praw.models import MoreComments
import requests
from urllib import parse
import os
import youtube_dl
import subprocess
from datetime import date
import json
from better_profanity import profanity

reddit = praw.Reddit(
    client_id="9nXJxamasMcuOg",
    client_secret="OwVtC0jABwtnGz9RtlRGY1wo2MK6Nw",
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15 (made by user u/cyberclips)",
    # username="cyberclips",
    # password="Z2Eb0sC8"
)

# test_subreddits = {"nextfuckinglevel", "Unexpected", "aww"}
# test_subreddits = {"HighQualityGifs"}
# test_subreddits = ['Unexpected', 'funny', 'AbruptChaos', 'yesyesyesyesno', 'nonononoyes', 'WatchPeopleDieInside', 'KidsAreFuckingStupid', ]
# test_subreddits = ['AbruptChaos', 'WatchPeopleDieInside',]
test_subreddits = ['Unexpected', 'Whatcouldgowrong', ]
post_limit = 10

date_downloaded = date.today().strftime("%m-%d-%y")

post_dict = {}


class GetPosts:
    def __init__(self, subreddit_list, post_limit):
        self.subreddits_list = subreddit_list
        self.post_limit = post_limit

    def download_posts(self):
        count_downloads = 1
        for sub in self.subreddits_list:
            for submission in reddit.subreddit(sub).top("day",limit=self.post_limit):
                if submission.over_18 == False:
                    if submission.is_video == True:
                        GetPosts.get_videos(submission, sub)
                        GetPosts.write_to_json(submission, sub, count_downloads)
                        count_downloads += 1
                    elif submission.url.endswith('gif') == True:
                        GetPosts.get_gifs(submission, sub)
                        GetPosts.write_to_json(submission, sub, count_downloads)
                        count_downloads += 1
                    elif submission.url.endswith('gifv') == True:
                        GetPosts.get_videos(submission, sub)
                        GetPosts.write_to_json(submission, sub, count_downloads)
                        count_downloads += 1
        with open('shorts_post_info.json', 'w') as post_list:
            json.dump(post_dict, post_list, indent=4)
        print('posted dict to json')



    def get_videos(submission, sub):
        print("Title: " + submission.title)
        ydl_opts = {
            'outtmpl': f'Shorts/Downloaded/{date_downloaded}/{submission.name}.mp4'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([submission.url])

    def get_gifs(submission, sub):
        print(f"downloading {submission.name}")
        img_data = requests.get(submission.url).content
        with open(f'Shorts/Downloaded/{date_downloaded}/{submission.name}.mp4', 'wb') as handler:
            handler.write(img_data)

    def get_length(filename):
        cmd_list = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                    "default=noprint_wrappers=1:nokey=1", filename]
        print(f'Get Length: {" ".join(cmd_list)}')
        result = subprocess.run(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        if result.stdout.decode() == "N/A":
            return 0
        else:
            return float(result.stdout)


    def write_to_json(submission, sub, count_downloads):
        profanity.load_censor_words()
        submission.title = profanity.censor(submission.title)
        def top_comments(submission):
            comment_list = []
            submission.comment_sort = 'best'
            submission.comment_limit = 12

            for top_level_comment in submission.comments:
                if (hasattr(top_level_comment, 'stickied') == True) and (top_level_comment.stickied == True):
                    continue
                if isinstance(top_level_comment, MoreComments):
                    continue
                comment_list.append(profanity.censor(top_level_comment.body))
            return comment_list

        clip_length = GetPosts.get_length(f"Shorts/Downloaded/{date_downloaded}/{submission.name}.mp4")
        post_comments = top_comments(submission)

        post_data = {
            'date' : date_downloaded,
            'subreddit' : submission.subreddit_name_prefixed,
            'link' : submission.name, 
            'title' : submission.title, 
            'comments' : post_comments,
            'updoots' : submission.score, 
            'length' : clip_length, 
            'edited' : False,
            'published' : False,
            'delete' : False
            }
        post_dict[count_downloads] = post_data
        print('posted info to dictionary')





if __name__ == "__main__":
    GetPosts(test_subreddits, post_limit=post_limit).download_posts()
