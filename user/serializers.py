from rest_framework import serializers

from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel

from blog.models import Article as ArticleModel
from blog.models import Comment as CommentModel

class HobbySerializer(serializers.ModelSerializer):
    same_hobby_users = serializers.SerializerMethodField()
    def get_same_hobby_users(self,obj):
        # obj : hobby model 의 object
        
        # user_list = []
        # for user_profile in obj.userprofile_set.all():
        #     user_list.append(user_profile.user.username)

        # return user_list

        # for 축약
        return [user_profile.user.username for user_profile in obj.userprofile_set.all()]

    class Meta:
        model = HobbyModel
        fields = ["name","same_hobby_users"]

class UserProfileSerializer(serializers.ModelSerializer):
    # 매니투매니 관계이므로 쿼리셋으로 return  # input data 쿼리셋이면 many=True
    hobby = HobbySerializer(many=True)   
    class Meta:
        model = UserProfileModel
        fields = ["age","birthday","hobby"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ["content"]

class UserArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleModel
        fields = ["category","title","content"]

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()   # 원투원관계의 경우 object로 return
    articles = UserArticleSerializer(many=True, source='article_set')
    comments = CommentSerializer(many=True, source='comment_set')
    class Meta:
        model = UserModel
        # fields = '__all__'  # 모든필드 가져온다
        fields = ["username","email","join_date","userprofile","articles","comments"]