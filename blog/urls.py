from django.urls import path
from . import views


urlpatterns = [
    path('article/all/', views.AllArticleAPIView.get_all_articles),
]
