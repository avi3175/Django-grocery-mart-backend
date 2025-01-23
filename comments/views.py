# from rest_framework import viewsets, permissions
# from .models import Comment
# from .serializers import CommentSerializer

# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all().order_by('-created_at')
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)





from rest_framework import viewsets, permissions
from .models import Comment
from .serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Get the current user from the request and filter comments by that user
        user = self.request.user
        return Comment.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
