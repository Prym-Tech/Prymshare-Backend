# pages/views.py

from django.shortcuts import get_object_or_404 # Import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Page, Section
from .serializers import PageSerializer, PageCreateSerializer, SectionSerializer, SectionOrderSerializer




class PageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Page.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return PageCreateSerializer
        return PageSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if not user.can_create_page():
            return Response(
                {"detail": "You have reached the maximum number of pages for your plan."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        page = serializer.save(owner=user)
        
        # --- Default Header section now includes a `description` field ---
        Section.objects.create(
            page=page,
            section_type='header',
            position=0,
            is_enabled=True,
            content={
                "description": "This is my page! Check out my links below.",
                "social_links": {
                    "twitter": "", "instagram": "", "facebook": "", "linkedin": "", "tiktok": ""
                }
            }
        )


# --- SectionViewSet is updated ---
class SectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Sections within a page.
    This view now explicitly depends on 'page_pk' from the URL.
    """
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This queryset is now filtered based on the page_pk from the URL,
        ensuring we only ever see sections for the specified page.
        """
        page_pk = self.kwargs.get('page_pk')
        return Section.objects.filter(page__pk=page_pk, page__owner=self.request.user)

    def perform_create(self, serializer):
        """
        When creating a new section, we automatically associate it with the
        page identified by page_pk in the URL.
        """
        page_pk = self.kwargs.get('page_pk')
        page = get_object_or_404(Page, pk=page_pk, owner=self.request.user)
        serializer.save(page=page)
        
    @action(detail=False, methods=['post'], url_path='update-order')
    def update_order(self, request, page_pk=None):
        """
        Custom action to update the order of sections via drag-and-drop.
        """
        serializer = SectionOrderSerializer(data=request.data)
        if serializer.is_valid():
            section_ids = serializer.validated_data['section_ids']
            
            # Use the queryset logic to ensure we only touch sections for this page
            sections_queryset = self.get_queryset()
            
            for index, section_id in enumerate(section_ids):
                section = get_object_or_404(sections_queryset, pk=section_id)
                section.position = index
                section.save()
            
            return Response({"status": "order updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)