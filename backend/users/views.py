from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Profile, AlumniVerification
from .serializers import (
    UserCreateSerializer, UserSerializer, UserUpdateSerializer,
    ProfileSerializer, AlumniVerificationSerializer, 
    AlumniVerificationAdminSerializer, ChangePasswordSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint.
    Creates both User and Profile models.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create user with profile in a single transaction."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        
        # Return user data with profile
        user_serializer = UserSerializer(user, context={'request': request})
        return Response(
            {
                'message': 'User created successfully',
                'user': user_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update current user's profile.
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Return the current user."""
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        """Get current user data with profile."""
        user = self.get_object()
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """Update user and profile data."""
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        updated_user = serializer.save()
        response_serializer = UserSerializer(updated_user, context={'request': request})
        
        return Response(
            {
                'message': 'Profile updated successfully',
                'user': response_serializer.data
            }
        )


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Get and update specific profile fields.
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Return the current user's profile."""
        return get_object_or_404(Profile, user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        """Update profile data."""
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        updated_profile = serializer.save()
        return Response(
            {
                'message': 'Profile updated successfully',
                'profile': ProfileSerializer(updated_profile).data
            }
        )


class AlumniVerificationView(generics.CreateAPIView):
    """
    Submit alumni verification request.
    """
    serializer_class = AlumniVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        """Create verification request."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        verification = serializer.save()
        return Response(
            {
                'message': 'Verification request submitted successfully',
                'verification': AlumniVerificationSerializer(verification).data
            },
            status=status.HTTP_201_CREATED
        )


class AlumniVerificationListView(generics.ListAPIView):
    """
    List user's verification requests.
    """
    serializer_class = AlumniVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return verifications for current user."""
        return AlumniVerification.objects.filter(user=self.request.user)


class AlumniVerificationDetailView(generics.RetrieveAPIView):
    """
    Get specific verification request details.
    """
    serializer_class = AlumniVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return verifications for current user."""
        return AlumniVerification.objects.filter(user=self.request.user)


class AdminVerificationListView(generics.ListAPIView):
    """
    List all verification requests (admin only).
    """
    serializer_class = AlumniVerificationAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = AlumniVerification.objects.all().order_by('-created_at')


class AdminVerificationDetailView(generics.RetrieveUpdateAPIView):
    """
    Admin view for managing verification requests.
    """
    serializer_class = AlumniVerificationAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = AlumniVerification.objects.all()
    
    def update(self, request, *args, **kwargs):
        """Update verification status."""
        verification = self.get_object()
        serializer = self.get_serializer(verification, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        updated_verification = serializer.save()
        
        # Handle status changes
        if 'verification_status' in request.data:
            new_status = request.data['verification_status']
            if new_status == 'verified':
                verification.mark_as_verified(request.user)
            elif new_status == 'rejected':
                verification.mark_as_rejected(request.user)
        
        return Response(
            {
                'message': 'Verification updated successfully',
                'verification': AlumniVerificationAdminSerializer(updated_verification).data
            }
        )


class ChangePasswordView(APIView):
    """
    Change user password.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Change password with validation."""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response(
            {'message': 'Password changed successfully'},
            status=status.HTTP_200_OK
        )


class UserListView(generics.ListAPIView):
    """
    List all users (admin only).
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all().order_by('-date_joined')


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin view for managing specific users.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete user (deactivate instead of hard delete)."""
        user = self.get_object()
        user.is_active = False
        user.save()
        
        return Response(
            {'message': 'User deactivated successfully'},
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """
    Get current user statistics.
    """
    user = request.user
    profile = getattr(user, 'profile', None)
    
    stats = {
        'total_points': profile.total_points if profile else 0,
        'verification_count': user.verifications.count(),
        'verified_verifications': user.verifications.filter(verification_status='verified').count(),
        'is_alumni': user.is_alumni,
        'is_verified': user.is_verified,
    }
    
    return Response(stats)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_points(request):
    """
    Add points to user profile (for gamification).
    """
    points = request.data.get('points', 0)
    
    if not isinstance(points, int) or points <= 0:
        return Response(
            {'error': 'Points must be a positive integer'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        profile = request.user.profile
        profile.total_points += points
        profile.save()
        
        return Response(
            {
                'message': f'{points} points added successfully',
                'total_points': profile.total_points
            }
        )
    except Profile.DoesNotExist:
        return Response(
            {'error': 'Profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )
