import json
from datetime import datetime, date


class TestClass:
    def __init__(self):
        num_of_clips = 0
    
    def test_def():
        with open('shorts_post_info.json', 'r') as posts_file:
            data = json.load(posts_file)
            post_hour = 9
            for clip in data:
                TestClass.time(post_hour)
                post_hour += 1
                

    def time(post_hour):
        begin_time = str(date.today()) + f" {post_hour}:00"
        post_time = datetime.strptime(begin_time, '%Y-%m-%d %H:%M').replace(second=0, microsecond=0).isoformat()
        print(post_time)

    def testing():
        test_string = "WCGW If I Ride Across A Lake With A Motorcycle At High Speed Thinking I Can Hydroplane On The Surface"
        test_string = test_string[0:90]
        print(test_string)
                

if __name__ == '__main__':
    TestClass.testing()