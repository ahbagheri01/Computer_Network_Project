from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers import VideoSerializer
from ..models import Video

class GetVideoData(APIView):
    http_method_names = ['get']

    def get(self, request, id):
        video = Video.objects.filter(pk=id).prefetch_related('user', 'video_tag')
        if video.is_banned:
            return Response(data={"message": "video is banned"}, status=403)
        return Response(data=VideoSerializer(video).data, status=200)