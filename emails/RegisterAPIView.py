from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from emails.serializers import UserRegisterSerializer
User = get_user_model()


class RegisterAPIView(APIView):
    serializer_class = UserRegisterSerializer
    permission_classes = []

    def post(self, request, format=None):
        username = request.data.get('username', '')

        serializer = self.serializer_class(data=request.data)
        if (serializer.is_valid()) or (
                ('username' in serializer.errors) and (
                len(serializer.errors['username']) > 0) and (
                serializer.errors[
                    'username'][0] == 'A user with that '
                                      'username already exists.')):
            if (serializer.is_valid()):
                user = serializer.save()
            else:
                user = User.objects.filter(username=username).first()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }

            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token", '')
            RefreshToken(refresh_token).blacklist()
            return Response('Success')
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
