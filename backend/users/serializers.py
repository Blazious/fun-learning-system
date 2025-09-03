from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Profile, AlumniVerification
from django.utils import timezone

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile data."""
    
    class Meta:
        model = Profile
        fields = [
            'id', 'academic', 'professional', 'bio', 'avatar', 
            'interests', 'social_links', 'role', 'total_points',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_points', 'created_at', 'updated_at']
    
    def validate_academic(self, value):
        """Validate academic information structure."""
        if value:
            required_fields = ['institution', 'graduation_year', 'degree_program']
            for field in required_fields:
                if field not in value:
                    raise serializers.ValidationError(f"Missing required field: {field}")
            
            # Validate graduation year
            if 'graduation_year' in value:
                year = value['graduation_year']
                if not isinstance(year, int) or year < 1900 or year > 2100:
                    raise serializers.ValidationError("Invalid graduation year")
        
        return value
    
    def validate_professional(self, value):
        """Validate professional information structure."""
        if value:
            required_fields = ['company', 'role', 'experience_level']
            for field in required_fields:
                if field not in value:
                    raise serializers.ValidationError(f"Missing required field: {field}")
        
        return value
    
    def validate_interests(self, value):
        """Validate interests list."""
        if value and not isinstance(value, list):
            raise serializers.ValidationError("Interests must be a list")
        
        if value:
            for interest in value:
                if not isinstance(interest, str) or len(interest.strip()) == 0:
                    raise serializers.ValidationError("Each interest must be a non-empty string")
        
        return value
    
    def validate_social_links(self, value):
        """Validate social links structure."""
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("Social links must be a dictionary")
        
        if value:
            for platform, url in value.items():
                if not isinstance(platform, str) or not isinstance(url, str):
                    raise serializers.ValidationError("Social links must have string keys and values")
                if not url.startswith(('http://', 'https://')):
                    raise serializers.ValidationError(f"Invalid URL format for {platform}")
        
        return value


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password_retype = serializers.CharField(write_only=True, required=True)
    
    # Profile fields for initial setup
    bio = serializers.CharField(required=False, allow_blank=True)
    academic = serializers.JSONField(required=False)
    professional = serializers.JSONField(required=False)
    interests = serializers.ListField(
        child=serializers.CharField(), 
        required=False
    )
    social_links = serializers.JSONField(required=False)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'password_retype',
            'bio', 'academic', 'professional', 'interests', 'social_links'
        ]
        read_only_fields = ['id']
    
    def validate(self, attrs):
        """Validate password confirmation and email uniqueness."""
        if attrs['password'] != attrs['password_retype']:
            raise serializers.ValidationError("Passwords don't match")
        
        # Check if email already exists
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("A user with this email already exists")
        
        # Check if username already exists
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("A user with this username already exists")
        
        return attrs
    
    def create(self, validated_data):
        """Create user and profile with validated data."""
        # Extract profile-related fields
        profile_fields = ['bio', 'academic', 'professional', 'interests', 'social_links']
        profile_data = {field: validated_data.pop(field, None) for field in profile_fields}
        
        # Remove password_retype as it's not needed for user creation
        validated_data.pop('password_retype', None)
        
        # Create user
        user = User.objects.create_user(**validated_data)
        
        # Create profile with extracted data
        Profile.objects.create(
            user=user,
            **{k: v for k, v in profile_data.items() if v is not None}
        )
        
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data including profile information."""
    
    profile = ProfileSerializer(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    is_alumni = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'is_verified', 'is_alumni',
            'is_active', 'date_joined', 'last_login', 'profile',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'is_verified', 'is_alumni', 'is_active', 
            'date_joined', 'last_login', 'created_at', 'updated_at'
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information."""
    
    profile = ProfileSerializer()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'profile']
    
    def validate_email(self, value):
        """Validate email uniqueness excluding current user."""
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists")
        return value
    
    def validate_username(self, value):
        """Validate username uniqueness excluding current user."""
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists")
        return value
    
    def update(self, instance, validated_data):
        """Update user and profile data."""
        profile_data = validated_data.pop('profile', {})
        
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update profile fields
        if profile_data and hasattr(instance, 'profile'):
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class AlumniVerificationSerializer(serializers.ModelSerializer):
    """Serializer for alumni verification requests."""
    
    user = UserSerializer(read_only=True)
    verified_by = UserSerializer(read_only=True)
    
    class Meta:
        model = AlumniVerification
        fields = [
            'id', 'user', 'institution', 'graduation_year', 'degree_program',
            'verification_status', 'verification_method', 'verified_at',
            'verified_by', 'verification_data', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'verification_status', 'verified_at',
            'verified_by', 'created_at', 'updated_at'
        ]
    
    def validate(self, attrs):
        """Validate verification data."""
        # Check if user already has a pending or verified verification for this institution
        user = self.context['request'].user
        existing_verification = AlumniVerification.objects.filter(
            user=user,
            institution=attrs['institution'],
            graduation_year=attrs['graduation_year']
        ).first()
        
        if existing_verification:
            if existing_verification.verification_status == 'pending':
                raise serializers.ValidationError(
                    "You already have a pending verification for this institution"
                )
            elif existing_verification.verification_status == 'verified':
                raise serializers.ValidationError(
                    "You are already verified for this institution"
                )
        
        return attrs
    
    def create(self, validated_data):
        """Create verification request with current user."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AlumniVerificationAdminSerializer(serializers.ModelSerializer):
    """Admin serializer for managing verification requests."""
    
    user = UserSerializer(read_only=True)
    verified_by = UserSerializer(read_only=True)
    
    class Meta:
        model = AlumniVerification
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def update(self, instance, validated_data):
        """Update verification status and metadata."""
        # If status is being changed to verified, set verified_at and verified_by
        if 'verification_status' in validated_data:
            if validated_data['verification_status'] == 'verified':
                validated_data['verified_at'] = timezone.now()
                validated_data['verified_by'] = self.context['request'].user
        
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change requests."""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_retype = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs['new_password'] != attrs['new_password_retype']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs
    
    def validate_old_password(self, value):
        """Validate old password."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value
