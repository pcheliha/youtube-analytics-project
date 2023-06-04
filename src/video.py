import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id: str):
        self.video_id = video_id
        self.name: str = Video.print_info(self)['items'][0]['snippet']['title']
        self.url: str = f"https://youtu.be/gaoc9MPZ4bw/{video_id}"
        self.view: int = Video.print_info(self)['items'][0]['statistics']['viewCount']
        self.like: int = Video.print_info(self)['items'][0]['statistics']['likeCount']

    def __repr__(self):
        return f'id - {self.video_id}'

    def __str__(self):
        return f"{Video.print_info(self)['items'][0]['snippet']['title']}"

    def print_info(self):
        video_id = self.video_id
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        return video_response

class PLVideo(Video):
    def __init__(self, video_id: str, plvideo_id: str):
        super().__init__(video_id)
        self.plvideo_id = plvideo_id

