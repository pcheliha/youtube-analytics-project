import os
import isodate
from googleapiclient.discovery import build
import json
from src.channel import Channel
from datetime import timedelta
from src.video import Video

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


def printj(print_dict: dict) -> None:
    print(json.dumps(print_dict, indent=2, ensure_ascii=False))


class PlayList:
    def __init__(self, playlist_id: str) -> None:
        """
        Экземпляры класса инициализируются по id плейлиста
        """
        self.playlist_id = playlist_id
        self.title = self.name_pl()
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"

    def print_info(self) -> list:
        """
        Метод для получения информации в плейлисте.
        """
        playlist_id = self.playlist_id
        playlist_video = youtube.playlistItems().list(playlistId=playlist_id,
                                               part='contentDetails',
                                               maxResults=50, ).execute()

        return playlist_video

    def make_ch_id(self) -> str:
        """
        метод для получения id канала.
        """
        playlist_id = self.playlist_id
        ch_info = youtube.playlistItems().list(playlistId=playlist_id,
                                               part='contentDetails',
                                               maxResults=50,
                                               ).execute()

        ch_id = Channel(ch_info['items'][0]['snippet']['channelid'])
        return ch_id.channel_id

    def name_pl(self) -> str:
        """
        метод для получения названия канала.
        """
        channel_id = PlayList.make_ch_id(self)
        playlist = youtube.playlists().list(channelId=channel_id,
                                     part='contentDetails,snippet',
                                     maxResults=50,
                                     ).execute()
        for playlist in playlist['items']:
            if self.playlist_id in playlist['id']:
                return playlist['snippet']['title']


    @property
    def total_duration(self) -> timedelta:
        """
        метод для получения суммарной длительности плейлиста.
        """
        total_time = timedelta()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in PlayList.print_info(self)['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time += duration
        return total_time


    def show_best_video(self) -> str:
        """
        метод для получения ссылки на самое популярное видео по количеству лайков.
        """
        like_id = 0
        url_vid = ''
        for i in PlayList.print_info(self)['items']:
            vid = Video(i['contentDetails']['videoid'])
            if like_id < int(vid.like):
                like_id = int(vid.like)
        return url_vid
