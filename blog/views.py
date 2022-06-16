from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions  # 권한 설정
from rest_framework.response import Response

from blog.models import Article

# Create your views here.
class ArticleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user # 현재 로그인한 사용자

        articles = Article.objects.filter(author=user)

        title = []
        for article in articles:
            title.append(article.title)
        # print(title)

        # 위의 세줄을 이렇게 줄여 쓸 수 있다.
        title = [article.title for article in articles] 
        
        return Response({'article_list':title})