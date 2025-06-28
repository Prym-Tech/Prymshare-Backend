# prymshare_project/prymshare_project/context_processors.py

from django.conf import settings

def frontend_url_context_processor(request):
    """
    Passes the FRONTEND_URL from settings into the template context.
    """
    return {
        'FRONTEND_URL': settings.FRONTEND_URL,
    }