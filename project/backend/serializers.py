from rest_framework import serializers

from .models import Bookmark, CustomUser, Tag


class TagSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        tag, created = Tag.objects.get_or_create(**validated_data)
        if not created:
            raise serializers.ValidationError('Tag already exists', code=400)
        return tag

    
    class Meta:
        model = Tag
        
        fields = (
            'pk',
            'text',
            'slug',
            'created_at',
            'modified_at',
        )
        
        extra_kwargs = {
            'slug': {'required': False}, # This is auto-filled when model object is saved
        }


class BookmarkSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    def create(self, validated_data):
        user = validated_data.pop('user')
        tags_data = validated_data.pop('tags')
        
        bookmark = Bookmark.objects.create(user=user, **validated_data)
        
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(user=user, **tag_data)
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
    
