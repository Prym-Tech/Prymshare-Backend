from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Page, Section
# --- CHANGE START ---
from .serializers import (
    PageSerializer, PageCreateSerializer, SectionSerializer, 
    SectionOrderSerializer, PagePaymentSettingsSerializer
)
import requests
from django.conf import settings
# --- CHANGE END ---


# --- CHANGE START ---
# View to get the list of Nigerian banks from Paystack
@api_view(['GET'])
def get_nigerian_banks(request):
    url = 'https://api.paystack.co/bank?country=nigeria'
    headers = {'Authorization': f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return Response(response.json(), status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response({"error": f"Failed to fetch banks: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to resolve a bank account and get the account name
@api_view(['POST'])
def resolve_bank_account(request):
    account_number = request.data.get('account_number')
    bank_code = request.data.get('bank_code')
    if not account_number or not bank_code:
        return Response({"error": "Account number and bank code are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    url = f"https://api.paystack.co/bank/resolve?account_number={account_number}&bank_code={bank_code}"
    headers = {'Authorization': f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return Response(response.json(), status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response({"error": f"Failed to resolve account: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- CHANGE END ---


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Page.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return PageCreateSerializer
        # --- CHANGE START ---
        elif self.action == 'payment_settings':
            return PagePaymentSettingsSerializer
        # --- CHANGE END ---
        return PageSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if not user.can_create_page():
            return Response({"detail": "You have reached the maximum number of pages for your plan."}, status=status.HTTP_403_FORBIDDEN)
        
        page = serializer.save(owner=user)
        
        Section.objects.create(
            page=page,
            section_type='header',
            position=0,
            is_enabled=True,
            content={
                "style": "photo_top",
                "profileImageUrl": "",
                "bannerImageUrl": "",
                "description": "",
                "social_links": {}
            }
        )
    
    # --- CHANGE START ---
    # Custom action to handle creating/updating payment settings and Paystack subaccount
    @action(detail=True, methods=['post'], url_path='payment-settings')
    def payment_settings(self, request, pk=None):
        page = self.get_object()
        
        bank_code = request.data.get('bank_code')
        account_number = request.data.get('account_number')
        business_name = page.brand_name
        primary_contact_email = page.owner.email

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        
        # Data for Paystack subaccount API
        subaccount_data = {
            "business_name": business_name,
            "settlement_bank": bank_code,
            "account_number": account_number,
            "percentage_charge": 7.5, # Example percentage
            "primary_contact_email": primary_contact_email,
            "primary_contact_name": business_name,
        }

        try:
            if page.subaccount_code:
                # Update existing subaccount
                response = requests.put(f'https://api.paystack.co/subaccount/{page.subaccount_code}', headers=headers, json=subaccount_data)
            else:
                # Create new subaccount
                response = requests.post('https://api.paystack.co/subaccount', headers=headers, json=subaccount_data)
            
            response.raise_for_status()
            response_data = response.json()

            if response_data.get('status'):
                # Save the details to our Page model
                page_data = {
                    'subaccount_code': response_data['data']['subaccount_code'],
                    'bank_name': response_data['data']['settlement_bank'],
                    'bank_code': bank_code,
                    'account_number': account_number,
                    'account_name': response_data['data']['account_name'],
                }
                serializer = self.get_serializer(page, data=page_data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Paystack API error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # --- CHANGE END ---

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