from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from blog.models import *
from . import serializers


@api_view()
def get_all_articles(self):
    try:
        all_articles = Article.objects.all().order_by('-created_at')[:10]
        data = []

        for article in all_articles:
            data.append({
                "title": article.title,
                "cover": article.cover.url if article.cover else None,
                "content": article.content,
                "created_at": article.created_at,
                "category": article.author.user.first_name + ' ' + article.author.user.last_name,
            })

        return Response({'data': data}, status=status.HTTP_200_OK)

    except:
        return Response({'status': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_article(request):
    try:
        article_title = request.data['article_title']
        article = Article.objects.filter(title__contains=article_title)
        serialized_date = serializers.SingleArticleSerializer(article, many=True)
        data = serialized_date.data
        return Response({'data': data}, status=status.HTTP_200_OK)
    except:
        return Response({'status': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_articles(request):
    try:
        from django.db.models import Q

        query = request.data['query']
        articles = Article.objects.filter(Q(content__icontains=query))
        serialized_data = serializers.SingleArticleSerializer(articles, many=True)
        data = serialized_data.data
        return Response({'data': data}, status=status.HTTP_200_OK)
    except:
        return Response({'status': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def submit_article(request):
    serializer = serializers.SubmitArticleSerializer(data=request.data)
    try:
        if serializer.is_valid():
            title = serializer.data.get('title')
            cover = request.FILES['cover']
            content = serializer.data.get('content')
            category_id = serializer.data.get('category_id')
            author_id = serializer.data.get('author_id')
        else:
            return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=author_id)
        author = UserProfiles.objects.get(user=user)
        category = Category.objects.get(id=category_id)

        article = Article()
        article.title = title
        article.cover = cover
        article.content = content
        article.category = category
        article.author = author
        article.save()
        return Response({'data': serializers.SingleArticleSerializer(article).data}, status=status.HTTP_201_CREATED)
    except:
        return Response({'status': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
