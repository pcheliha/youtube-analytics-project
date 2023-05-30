import os
from googleapiclient.discovery import build
import json

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self._channel_id = channel_id
        self.title = Channel.print_info(self)['items'][0]['snippet']['title']
        self.description = Channel.print_info(self)['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{channel_id}"
        self.video_count = Channel.print_info(self)['items'][0]['statistics']['videoCount']
        self.views_count = Channel.print_info(self)['items'][0]['statistics']['viewCount']
        self.subscriber_count = Channel.print_info(self)['items'][0]['statistics']['subscriberCount']


    def __str__(self):
        return f'{self.title}, {self.url}'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        if int(self.subscriber_count) < int(other.subscriber_count):
            return True
        return False

    def __le__(self, other):
        if int(self.subscriber_count) <= int(other.subscriber_count):
            return True
        return False

    def __gt__(self, other):
        if int(self.subscriber_count) > int(other.subscriber_count):
            return True
        return False

    def __ge__(self, other):
        if int(self.subscriber_count) >= int(other.subscriber_count):
            return True
        return False

    def __eq__(self, other):
        if int(self.subscriber_count) == int(other.subscriber_count):
            return True
        return False

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return channel

    @property
    def channel_id(self):
        return self._channel_id

    @classmethod
    def get_service(cls):
        return Channel.channel_id

    def to_json(self, name_json) -> "json":
        data = {}
        data['channel_id'] = self.channel_id
        data['title'] = self.title
        data['description'] = self.description
        data['url'] = self.url
        data['videoCount'] = self.video_count
        data['viewsCount'] = self.views_count
        data['subscriberCount'] = self.subscriber_count
        with open(f'{name_json}', "w", encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)




