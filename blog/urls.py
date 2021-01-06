from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('article-view-set', views.ArticleViewSet)

urlpatterns = [
    path('article/', views.get_article),
    path('article/all/', views.get_all_articles),
    path('article/search/', views.get_all_articles),
    path('article/submit/', views.submit_article),
    path('article/update/<int:pk>', views.update_article),
    path('article/delete/<int:pk>', views.delete_article),
]

urlpatterns += router.urls
