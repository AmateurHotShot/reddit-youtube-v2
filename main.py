import find_videos
import edit_videos
import post_videos
import delete_videos

subs = ['Unexpected', 'Whatcouldgowrong', ]
post_limit = 10

find_videos.GetPosts(subs, post_limit=post_limit).download_posts()
edit_videos.EditClip.shortify()
post_videos.YouTubeUpload.upload()
delete_videos.DeleteClips.delete()