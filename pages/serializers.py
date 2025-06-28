# pages/serializers.py

from rest_framework import serializers
from .models import Page, Section

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'section_type', 'position', 'is_enabled', 'content']

class PageSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField()
    
    class Meta:
        model = Page
        fields = [
            'id', 'owner', 'slug', 'sections', 'created_at',
            # Pro Features
            'show_storefront_tab', 'background_color', 'background_image', 'template_theme'
        ]

class PageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['slug'] # User only needs to provide a slug to start
        
    def validate_slug(self, value):
        if Page.objects.filter(slug__iexact=value).exists():
            raise serializers.ValidationError("This page name is already taken.")
        return value

class SectionOrderSerializer(serializers.Serializer):
    section_ids = serializers.ListField(
        child=serializers.IntegerField()
    )