import find_videos
import edit_videos
import post_videos
import delete_videos

subs = ['Unexpected', ]

find_videos.GetPosts(subs).download_posts()
edit_videos.EditClip.shortify()
post_videos.YouTubeUpload.upload()
delete_videos.DeleteClips.delete()