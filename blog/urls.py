from django.urls import path
from . import views


urlpatterns = [
    path('article/', views.get_article),
    path('article/all/', views.get_all_articles),
    path('article/search/', views.get_all_articles),
    path('article/submit/', views.submit_article),
    path('article/update-cover/', views.submit_article),
]
