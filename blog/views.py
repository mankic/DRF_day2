from importlib.resources import contents
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions  # 권한 설정
from rest_framework.response import Response

from blog.models import Article
from user.models import User
from DRF_day2.permissions import RegistedMoreThanThreeDaysUser, IsAdminOrIsAuthenticatedReadOnly
from blog.serializers import UserArticleSerializer

from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.
class ArticleView(APIView):
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get(self, request):
        user = request.user # 현재 로그인한 사용자
        
        # articles = Article.objects.filter(author=user)
        #Field lookups
        # articles = Article.objects.filter(join_date__lte=today() - timedelta(day=3))
        # articles = Article.objects.filter(title__contains=user)
        articles = Article.objects.filter(start_view__lte=datetime.now(), end_view__gte=datetime.now())

        # user = UserModel.objects.create(**request.data)

        # password = request.data.pop("password")
        # user.set_password(password)
        # user.save()


        # title = []
        # for article in articles:
        #     title.append(article.title)
        # print(title)

        # 위의 세줄을 이렇게 줄여 쓸 수 있다.
        title = [article.title for article in articles] 
        
        return Response({'article_list':title})

    def post(self, request):
        user = request.user 
        title = request.data.get('title','')
        contents = request.data.get('contents','')
        categorys = request.data.get('categorys','')

        if len(title) <= 5:
            return Response({'message':'제목을 5자 이상 적어주세요'})
        if len(contents) <= 20:
            return Response({'message':'내용을 20자 이상 적어주세요'})
        if not categorys:
            return Response({'message':'카테고리를 선택하세요'})

        article = Article(
            author=user,
            title=title,
            content=contents
        )
        article.save()
        article.category.add(*categorys)
        return Response({'message':'성공!'})