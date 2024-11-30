from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from .serializers import UserCourseProgressSerializer, UserSerializer
from .models import UserCourseProgress
from drf_yasg import openapi

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password'] 

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

class CustomUserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(tags=['Auth'], operation_description="Register a new user")
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CustomUserLoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['Auth'], operation_description="Login user", request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                })
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProgress(generics.ListAPIView):
    """User progress"""
    serializer_class = UserCourseProgressSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['User'],
        operation_description="Retrieve a list of user courses and progress",
        responses={200: openapi.Response('retrieved successfully', UserCourseProgressSerializer(many=True))},
        operation_summary="List user courses progress"
    )
    def get(self, request):
        user = request.user
        user_courses = UserCourseProgress.objects.filter(user=user)
        serialized_data = UserCourseProgressSerializer(user_courses, many=True)
        return Response(serialized_data.data)

class UserInfo(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['User'],
        operation_description="Get logged in user info",
        responses={200: openapi.Response('retrieved successfully', UserSerializer)},
        operation_summary="List user details"
    )
    def get(self, request):
        user = request.user
        serialized_data = UserSerializer(user)
        return Response(serialized_data.data)

user_info = UserInfo.as_view()
register_user = CustomUserRegistrationView.as_view()
login_user = CustomUserLoginView.as_view()
user_course_progress  = UserProgress.as_view()