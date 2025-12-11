from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import MediaItem
from .serializers import MediaItemSerializer

class MediaItemViewSet(viewsets.ModelViewSet):
    serializer_class = MediaItemSerializer
    # Enforce authentication for all methods (CRUD) on this ViewSet
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Base queryset: Filter items by the logged-in user and only show active items
        return MediaItem.objects.filter(owner=self.request.user, deleted=False)

    def perform_create(self, serializer):
        # Automatically set the owner of the media item to the logged-in user
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        # Implement soft-delete instead of hard delete
        instance.deleted = True
        instance.save()
        # You may want to return a more informative status code/response for soft-delete
        return Response(status=status.HTTP_204_NO_CONTENT)

    # --- Custom Action: GET /api/media-items/deleted/ ---
    @action(detail=False, methods=['get'])
    def deleted(self, request):
        """Returns a list of soft-deleted media items for the current user."""
        deleted_items = MediaItem.objects.filter(owner=request.user, deleted=True)
        serializer = self.get_serializer(deleted_items, many=True)
        return Response(serializer.data)

    # --- Custom Action: POST /api/media-items/{id}/restore/ ---
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Restores a soft-deleted media item."""
        item = get_object_or_404(MediaItem, pk=pk, owner=request.user, deleted=True)
        item.deleted = False
        item.save()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    # --- Custom Action: POST /api/media-items/{id}/unmark_finished/ ---
    @action(detail=True, methods=['post'])
    def unmark_finished(self, request, pk=None):
        """Changes a finished item back to watching/planned (example logic)."""
        item = get_object_or_404(MediaItem, pk=pk, owner=request.user)
        # Assuming you reset it to 'Watching' or 'Planned'
        item.status = 'Watching' 
        item.save()
        serializer = self.get_serializer(item)
        return Response(serializer.data)