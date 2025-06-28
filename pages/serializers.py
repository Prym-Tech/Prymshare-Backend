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
            'id', 'owner', 'brand_name', 'title', 'slug', 'sections', 'created_at',
            'show_storefront_tab', 'background_color', 'background_image', 'template_theme'
        ]
        read_only_fields = ['slug']

class PageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['brand_name', 'title']
        
    def validate_brand_name(self, value):
        if Page.objects.filter(brand_name__iexact=value).exists():
            raise serializers.ValidationError("This page name is already taken.")
        return value

    def create(self, validated_data):
        """
        This explicit create method ensures that the owner, brand_name, and title
        are all correctly passed when creating a new Page instance.
        """
        # The owner is passed from the view via `serializer.save(owner=...)`
        # and becomes available in `validated_data` here.
        return Page.objects.create(**validated_data)

class SectionOrderSerializer(serializers.Serializer):
    section_ids = serializers.ListField(
        child=serializers.IntegerField()
    )