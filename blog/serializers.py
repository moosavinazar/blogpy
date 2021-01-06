from rest_framework import serializers
from django.utils import timezone
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SingleArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Article
        fields = '__all__'
        # depth = 2


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ("created_at",)


class SubmitArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ("created_at",)

    def validate_title(self, value):
        if value == 'python':
            raise serializers.ValidationError("Not Valid Title")
        else:
            return value

    def create(self, validated_data):
        article = super().create(validated_data)
        article.created_at = timezone.now()
        user = User.objects.get(id=article.author_id)
        author = UserProfiles.objects.get(user=user)
        category = Category.objects.get(id=article.category_id)
        article.category = category
        article.author = author
        article.save()
        return article

    def update(self, instance, validated_data):
        old_created_at = instance.created_at
        article = super(SubmitArticleSerializer, self).update(instance, validated_data)
        article.created_at = old_created_at
        user = User.objects.get(id=article.author_id)
        author = UserProfiles.objects.get(user=user)
        category = Category.objects.get(id=article.category_id)
        article.category = category
        article.author = author
        article.save()
        return article
