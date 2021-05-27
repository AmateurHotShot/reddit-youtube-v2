# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.insert
# NOTES:
# 1. This sample code uploads a file and can't be executed via this interface.
#    To test this code, you must run it locally using your own API credentials.
#    See: https://developers.google.com/explorer-help/guides/code_samples#python
# 2. This example makes a simple upload request. We recommend that you consider
#    using resumable uploads instead, particularly if you are transferring large
#    files or there's a high likelihood of a network interruption or other
#    transmission failure. To learn more about resumable uploads, see:
#    https://developers.google.com/api-client-library/python/guide/media_upload

import os
import json
import pickle
from datetime import datetime, date

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from googleapiclient.http import MediaFileUpload

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

class YouTubeUpload:
    def __init__(self):
        pass

    def upload():
        with open('shorts_post_info.json', 'r') as posts_file:
            data = json.load(posts_file)
            post_hour = 9
            for vid_info in data:
                clip_info = data[vid_info]
                if (clip_info['delete'] == False) and (clip_info['edited'] == True) and (clip_info['published'] == False):
                    YouTubeUpload.post(clip_info, post_hour)
                    post_hour += 1

    def token():
        
        credentials = None

        if os.path.exists('token.pickle'):
            print('Loading Credentials From File...')
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)

        # If there are no valid credentials available, then either refresh the token or log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                print('Refreshing Access Token...')
                credentials.refresh(Request())
            else:
                print('Fetching New Tokens...')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json',
                    scopes=[
                        'https://www.googleapis.com/auth/youtube.upload'
                    ]
                )

                flow.run_local_server(port=8080, prompt='consent',
                                    authorization_prompt_message='')
                credentials = flow.credentials

                # Save the credentials for the next run
                with open('token.pickle', 'wb') as f:
                    print('Saving Credentials for Future Use...')
                    pickle.dump(credentials, f)

        return credentials

    def post(clip_info, post_hour):
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=YouTubeUpload.token())


        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                "categoryId": "23",
                "description": YouTubeUpload.find_and_replace(clip_info),
                "title": f"{clip_info['title'][0:90]} #Shorts",
                "tags": ["watch people die inside the best so far","reddit memes compilation","reddit videos are lazy","fresh memes to bless 2021","funny videos for babies","reddit videos that take a turn","kid memes clean","memes","try not to laugh","funny","best memes","dank memes","memes compilation","dank memes compilation","tik tok memes","funny videos","clean memes","funny vines","try not to laugh challenge","vine","try not to laugh or grin","tiktok","clean","meme","funny memes","fresh memes","try not to laugh kids"]
                },
                "status": {
                "privacyStatus": "private",
                "publishAt": YouTubeUpload.publish_time(post_hour)
                }
            },
            
            media_body=MediaFileUpload(f"Shorts/Edited/{clip_info['date']}/{clip_info['link']}.mp4")
        )
        
        response = request.execute()

        print(response)
    
    def find_and_replace(clip_info):

        with open('Boilerplate/YouTubePostData/description.txt', 'r') as file:
            comment_list = str('\n'.join(clip_info['comments']))
            descr_temp = file.read()
            descr_temp = descr_temp.replace('[title]', clip_info['title'])
            final_description = descr_temp.replace('[comments]', comment_list)
            return final_description

    def publish_time(post_hour):
        begin_time = str(date.today()) + f" {post_hour}:00"
        post_time = datetime.strptime(begin_time, '%Y-%m-%d %H:%M').replace(second=0, microsecond=0).isoformat()
        return post_time



if __name__ == "__main__":
    YouTubeUpload.upload()