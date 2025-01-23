from django.contrib.auth.models import User
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, TokenSerializer

class SignupView(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(TokenSerializer({'access': str(refresh.access_token), 'refresh': str(refresh)}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]






class LogoutView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        except (AttributeError, TypeError):
            return Response({"detail": "User is not authenticated"}, status=status.HTTP_400_BAD_REQUEST)
