from rest_framework import serializers

from .models import Video, VideoTag
from django.contrib.auth.models import User


def get_url(link):
    return "https://localhost:8000/" + link

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class TagSerializer(serializers.ModelSerializer):
    label = serializers.CharField()

    class Meta:
        model = VideoTag
        fields = ['label']

class VideoSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_file_url')
    caption = serializers.CharField()
    tags = TagSerializer()

    class Meta:
        model = Video
        fields = ['url', 'caption', 'tags']


    @staticmethod
    def get_file_url(video: Video):
        return get_url(video.file.url)