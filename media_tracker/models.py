from django.db import models
from django.contrib.auth.models import User

# Choices for Media Status
STATUS_CHOICES = (
    ('Planned', 'Planned to Watch'),
    ('Watching', 'Currently Watching'),
    ('Finished', 'Finished'),
)

# Choices for Media Type
MEDIA_TYPE_CHOICES = (
    ('Movie', 'Movie'),
    ('TV Show', 'TV Show'),
    ('Book', 'Book'),
    ('Game', 'Video Game'),
)

class MediaItem(models.Model):
    # This links the item to the user who created it.
    owner = models.ForeignKey(User, related_name='media_items', on_delete=models.CASCADE)
    
    title = models.CharField(max_length=255)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='Movie')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Planned')
    
    # Critical field used for Burden calculation
    time_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.0) 
    
    is_favorite = models.BooleanField(default=False)
    
    # Field required for the soft-delete/trash bin functionality
    deleted = models.BooleanField(default=False) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_favorite', 'title'] # Favorites first, then alphabetical
    
    def __str__(self):
        return f"{self.title} ({self.get_media_type_display()})"