import json, shutil

class DeleteClips:
    def __init__(self):
        pass
    
    def delete():
        with open("shorts_post_info.json", 'r') as clip_list:
            data = json.load(clip_list)
            clip_info = data['1']

            print(clip_info)

            download_path = f"Shorts/Downloaded/{clip_info['date']}"
            edited_path = f"Shorts/Edited/{clip_info['date']}"
            print(download_path)
            try:
                shutil.rmtree(download_path)
                print(f"Deleted {download_path}")
            except OSError as e:
                print(f"Could not delete '{download_path}'. {e.strerror}")

            try:
                shutil.rmtree(edited_path)
                print(f"Deleted {edited_path}")
            except OSError as e:
                print(f"Could not delete '{edited_path}'. {e.strerror}")



if __name__ == '__main__':
    DeleteClips.delete()