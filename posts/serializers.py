from rest_framework.serializers import ModelSerializer

from posts.models import Post


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('data', )
