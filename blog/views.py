from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from blog.models import Article


class AllArticleAPIView:

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

