from rest_framework import serializers

from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel

from blog.models import Article as ArticleModel
from blog.models import Comment as CommentModel
from blog.models import Category as CategoryModel


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model =CategoryModel
#         fields = ['name']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self,obj):
        return obj.name.username

    class Meta:
        model = CommentModel
        fields = ['user',"content"]


class UserArticleSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, source='comment_set', read_only=True)   # read_only 생성,수정하지않고 읽기전용
    # comment_set = CommentSerializer(many=True)

    def get_category(self,obj):
        return [category.name for category in obj.category.all()]

    class Meta:
        model = ArticleModel
        fields = ["author","category","title","content","comments","start_view","end_view"]

        # SerializerMethodField 와 read_only 는 is_valid 안함.


