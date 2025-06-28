# pages/models.py

from django.db import models
from users.models import CustomUser
from django.utils.text import slugify

# Theme choices for Pro users
THEME_CHOICES = [
    ('default', 'Default'),
    ('dark_mode', 'Dark Mode'),
    ('misty_rose', 'Misty Rose'),
]

class Page(models.Model):
    """
    Represents a single user page (e.g., prymshare.co/theprympeeps).
    """
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='pages')
    brand_name = models.CharField(max_length=100, unique=True, help_text="Your unique brand name. This will be used in your page URL.")
    title = models.CharField(max_length=100, blank=True, help_text="e.g., Fitness Coach, Digital Artist, Podcaster")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Pro Features
    show_storefront_tab = models.BooleanField(default=False)
    background_color = models.CharField(max_length=7, default='#FFFFFF') # Hex color
    background_image = models.ImageField(upload_to='page_backgrounds/', blank=True, null=True)
    template_theme = models.CharField(max_length=50, choices=THEME_CHOICES, default='default')

    def save(self, *args, **kwargs):
        # Check plan limit on creation
        if not self.pk:
            if not self.owner.can_create_page():
                raise ValidationError("User has reached the maximum number of pages for their plan.")
        
        # Auto-generate slug from the unique brand_name
        self.slug = slugify(self.brand_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.brand_name


class Section(models.Model):
    """
    Represents a single, re-orderable section on a Page.
    """
    SECTION_TYPE_CHOICES = [
        ('header', 'Header'),
        ('links', 'Links'),
        ('carousel', 'Carousel'),
        ('video', 'Video'),
        ('paywall', 'Paywall'),
        ('courses', 'Courses'),
        ('events', 'Events'),
        ('masterclass', 'Masterclass/Webinar'),
        ('appointments', 'One-on-one Appointments'),
    ]

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=20, choices=SECTION_TYPE_CHOICES)
    position = models.PositiveIntegerField(default=0, help_text="Order of section on the page, managed by drag-and-drop.")
    is_enabled = models.BooleanField(default=True)
    
    # Using JSONField for ultimate flexibility across different section types
    content = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"{self.get_section_type_display()} section on {self.page.slug}"