from rest_framework import serializers

from .models import Bookmark, CustomUser, Tag


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = (
            'pk',
            'slug',
        )


class BookmarkSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        
        bookmark = Bookmark.objects.create(**validated_data)
        
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            bookmark.tags.add(tag)
        
        return bookmark

    class Meta:
        model = Bookmark
        fields = (
            'pk',
            'title',
            'url',
            'comments',
            'tags',
            'created_at',
            'modified_at',
        )
    
