from rest_framework import serializers
from .models import Post, Tag, Category, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'author']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'name', 'description', 'author', 'tags', 'category', "slug"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.query_params.get('include') == 'comments':
            comments = Comment.objects.filter(post=instance)
            representation['comments'] = CommentSerializer(comments, many=True).data
        return representation


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['name', 'description', 'category', 'tags']

