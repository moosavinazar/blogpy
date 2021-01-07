from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from blog.models import *
from . import serializers
from rest_framework import viewsets, permissions


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = serializers.SingleArticleSerializer
    http_method_names = ['get', 'post']

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return serializers.SingleArticleSerializer
        else:
            return serializers.ArticleSerializer

    search_fields = ('name',)
    ordering_fields = '__all__'

    def list(self, request, *args, **kwargs):
        article = super().list(request, *args, **kwargs)
        print("----------- LIST -----------")
        return article

    def create(self, request, *args, **kwargs):
        article = super().create(request, *args, **kwargs)
        print("----------- CREATE -----------")
        return article

    def update(self, request, *args, **kwargs):
        article = super().update(request, *args, **kwargs)
        instance = self.get_object()
        print("----------- UPDATE ----------- {}".format(instance.title))
        return article

    def retrieve(self, request, *args, **kwargs):
        article = super().retrieve(request, *args, **kwargs)
        instance = self.get_object()
        print("----------- RETRIEVE ----------- {}".format(instance.title))
        return article

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print("----------- DESTROY ----------- {}".format(instance.title))
        article = super().destroy(request, *args, **kwargs)
        return article


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
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'status': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_article(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except:
        return Response({'error': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)

    serializer = serializers.SubmitArticleSerializer(article, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'status': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_article(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except:
        return Response({'error': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)

    article.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
