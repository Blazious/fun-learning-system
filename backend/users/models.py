import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Uses email as the primary identifier for authentication.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Override username and email fields
    username = models.CharField(
        max_length=100, 
        unique=True,
        help_text=_('Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only.')
    )
    email = models.EmailField(
        unique=True,
        help_text=_('Required. A valid email address.')
    )
    
    # Remove first_name and last_name from AbstractUser
    first_name = None
    last_name = None
    
    # Additional fields
    is_verified = models.BooleanField(default=False)
    is_alumni = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use email for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'users_user'
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the username as full name."""
        return self.username
    
    def get_short_name(self):
        """Return the username as short name."""
        return self.username


class Profile(models.Model):
    """
    Extended user profile with academic and professional information.
    Uses JSON fields for flexible data structures.
    """
    ROLE_CHOICES = [
        ('listener', 'Listener'),
        ('moderator', 'Moderator'),
        ('speaker', 'Speaker'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    
    # Academic information stored as JSON for flexibility
    academic = models.JSONField(
        default=dict, 
        blank=True,
        help_text=_('Academic information: institution, graduation_year, degree_program, current_status')
    )
    
    # Professional information stored as JSON for flexibility
    professional = models.JSONField(
        default=dict, 
        blank=True,
        help_text=_('Professional information: company, role, experience_level, industry')
    )
    
    # Personal information
    bio = models.TextField(blank=True, help_text=_('User biography'))
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True,
        help_text=_('User profile picture')
    )
    
    # Interests and social links
    interests = models.JSONField(
        default=list, 
        blank=True,
        help_text=_('List of user interests as strings')
    )
    social_links = models.JSONField(
        default=dict, 
        blank=True,
        help_text=_('Social media links: linkedin, github, twitter, etc.')
    )
    
    # Platform role and points
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='listener'
    )
    total_points = models.IntegerField(default=0, help_text=_('Total gamification points'))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        db_table = 'users_profile'
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_academic_info(self):
        """Return formatted academic information."""
        academic = self.academic or {}
        return {
            'institution': academic.get('institution', ''),
            'graduation_year': academic.get('graduation_year', ''),
            'degree_program': academic.get('degree_program', ''),
            'current_status': academic.get('current_status', '')
        }
    
    def get_professional_info(self):
        """Return formatted professional information."""
        professional = self.professional or {}
        return {
            'company': professional.get('company', ''),
            'role': professional.get('role', ''),
            'experience_level': professional.get('experience_level', ''),
            'industry': professional.get('industry', '')
        }


class AlumniVerification(models.Model):
    """
    Model for verifying alumni status of users.
    Supports multiple verification methods.
    """
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    VERIFICATION_METHOD_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('manual', 'Manual Upload'),
        ('email', 'Email'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='verifications'
    )
    
    # Institution details
    institution = models.CharField(max_length=255, help_text=_('Educational institution name'))
    graduation_year = models.IntegerField(help_text=_('Year of graduation'))
    degree_program = models.CharField(max_length=255, help_text=_('Degree program or major'))
    
    # Verification details
    verification_status = models.CharField(
        max_length=20, 
        choices=VERIFICATION_STATUS_CHOICES, 
        default='pending'
    )
    verification_method = models.CharField(
        max_length=20, 
        choices=VERIFICATION_METHOD_CHOICES
    )
    
    # Verification metadata
    verified_at = models.DateTimeField(blank=True, null=True)
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='verifications_approved'
    )
    
    # Additional verification data
    verification_data = models.JSONField(
        default=dict, 
        blank=True,
        help_text=_('Additional verification data (e.g., LinkedIn profile URL, document metadata)')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Alumni Verification')
        verbose_name_plural = _('Alumni Verifications')
        db_table = 'users_alumni_verification'
        unique_together = ['user', 'institution', 'graduation_year']
    
    def __str__(self):
        return f"{self.user.username} - {self.institution} ({self.graduation_year})"
    
    def mark_as_verified(self, verified_by_user):
        """Mark the verification as verified."""
        self.verification_status = 'verified'
        self.verified_at = timezone.now()
        self.verified_by = verified_by_user
        self.save()
        
        # Update user's alumni status
        self.user.is_alumni = True
        self.user.save()
    
    def mark_as_rejected(self, verified_by_user):
        """Mark the verification as rejected."""
        self.verification_status = 'rejected'
        self.verified_by = verified_by_user
        self.save()


class Badge(models.Model):
    """
    Model for managing gamification badges and achievements.
    """
    BADGE_TYPE_CHOICES = [
        ('participation', 'Participation'),
        ('achievement', 'Achievement'),
        ('milestone', 'Milestone'),
        ('special', 'Special Recognition'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, help_text=_('Badge name'))
    description = models.TextField(help_text=_('Badge description'))
    
    # Badge details
    badge_type = models.CharField(
        max_length=20,
        choices=BADGE_TYPE_CHOICES,
        default='achievement'
    )
    icon_url = models.URLField(blank=True, help_text=_('Badge icon URL'))
    
    # Badge requirements
    required_points = models.IntegerField(
        default=0,
        help_text=_('Points required to earn this badge')
    )
    required_actions = models.JSONField(
        default=list,
        blank=True,
        help_text=_('Required actions to earn this badge')
    )
    
    # Badge metadata
    is_active = models.BooleanField(default=True)
    rarity = models.CharField(
        max_length=20,
        choices=[
            ('common', 'Common'),
            ('uncommon', 'Uncommon'),
            ('rare', 'Rare'),
            ('epic', 'Epic'),
            ('legendary', 'Legendary'),
        ],
        default='common'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Badge')
        verbose_name_plural = _('Badges')
        db_table = 'users_badge'
        ordering = ['required_points', 'name']
    
    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """
    Model for tracking user badges and achievements.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='badges'
    )
    badge = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
        related_name='user_badges'
    )
    
    # Badge earning details
    earned_at = models.DateTimeField(auto_now_add=True)
    earned_for = models.TextField(
        blank=True,
        help_text=_('What the user did to earn this badge')
    )
    
    class Meta:
        verbose_name = _('User Badge')
        verbose_name_plural = _('User Badges')
        db_table = 'users_user_badge'
        unique_together = ['user', 'badge']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class PointsTransaction(models.Model):
    """
    Model for tracking points transactions and history.
    """
    TRANSACTION_TYPE_CHOICES = [
        ('earned', 'Earned'),
        ('spent', 'Spent'),
        ('bonus', 'Bonus'),
        ('penalty', 'Penalty'),
    ]
    
    SOURCE_CHOICES = [
        ('session_hosted', 'Session Hosted'),
        ('session_attended', 'Session Attended'),
        ('session_moderated', 'Session Moderated'),
        ('article_published', 'Article Published'),
        ('community_contribution', 'Community Contribution'),
        ('mentorship', 'Mentorship'),
        ('badge_earned', 'Badge Earned'),
        ('admin_adjustment', 'Admin Adjustment'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='points_transactions'
    )
    
    # Transaction details
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE_CHOICES,
        default='earned'
    )
    source = models.CharField(
        max_length=50,
        choices=SOURCE_CHOICES,
        help_text=_('Source of the points transaction')
    )
    
    # Points details
    points = models.IntegerField(help_text=_('Points amount (positive for earned, negative for spent)'))
    balance_after = models.IntegerField(help_text=_('User balance after this transaction'))
    
    # Transaction metadata
    description = models.TextField(help_text=_('Transaction description'))
    reference_id = models.UUIDField(
        blank=True,
        null=True,
        help_text=_('Reference to related object (session, article, etc.)')
    )
    reference_type = models.CharField(
        max_length=50,
        blank=True,
        help_text=_('Type of reference object')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Points Transaction')
        verbose_name_plural = _('Points Transactions')
        db_table = 'users_points_transaction'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.points} points ({self.source})"


class Notification(models.Model):
    """
    Model for managing user notifications and alerts.
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('session_reminder', 'Session Reminder'),
        ('session_scheduled', 'New Session Scheduled'),
        ('recording_available', 'Recording Available'),
        ('feedback_received', 'Feedback Received'),
        ('community_activity', 'Community Activity'),
        ('milestone_achieved', 'Milestone Achieved'),
        ('badge_earned', 'Badge Earned'),
        ('mentorship_update', 'Mentorship Update'),
        ('career_opportunity', 'Career Opportunity'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    # Notification content
    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPE_CHOICES,
        help_text=_('Type of notification')
    )
    title = models.CharField(max_length=255, help_text=_('Notification title'))
    message = models.TextField(help_text=_('Notification message'))
    
    # Notification settings
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal'
    )
    is_read = models.BooleanField(default=False)
    is_email_sent = models.BooleanField(default=False)
    
    # Action and reference
    action_url = models.URLField(
        blank=True,
        help_text=_('URL to navigate to when notification is clicked')
    )
    reference_id = models.UUIDField(
        blank=True,
        null=True,
        help_text=_('Reference to related object')
    )
    reference_type = models.CharField(
        max_length=50,
        blank=True,
        help_text=_('Type of reference object')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        db_table = 'users_notification'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read."""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])


class NotificationPreference(models.Model):
    """
    Model for managing user notification preferences.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    
    # Email preferences
    email_sessions = models.BooleanField(default=True, help_text=_('Email notifications for sessions'))
    email_recordings = models.BooleanField(default=True, help_text=_('Email notifications for recordings'))
    email_feedback = models.BooleanField(default=True, help_text=_('Email notifications for feedback'))
    email_community = models.BooleanField(default=True, help_text=_('Email notifications for community activity'))
    email_milestones = models.BooleanField(default=True, help_text=_('Email notifications for milestones'))
    email_mentorship = models.BooleanField(default=True, help_text=_('Email notifications for mentorship'))
    email_career = models.BooleanField(default=True, help_text=_('Email notifications for career opportunities'))
    
    # In-app preferences
    in_app_sessions = models.BooleanField(default=True, help_text=_('In-app notifications for sessions'))
    in_app_recordings = models.BooleanField(default=True, help_text=_('In-app notifications for recordings'))
    in_app_feedback = models.BooleanField(default=True, help_text=_('In-app notifications for feedback'))
    in_app_community = models.BooleanField(default=True, help_text=_('In-app notifications for community activity'))
    in_app_milestones = models.BooleanField(default=True, help_text=_('In-app notifications for milestones'))
    in_app_mentorship = models.BooleanField(default=True, help_text=_('In-app notifications for mentorship'))
    in_app_career = models.BooleanField(default=True, help_text=_('In-app notifications for career opportunities'))
    
    # General preferences
    quiet_hours_start = models.TimeField(
        blank=True,
        null=True,
        help_text=_('Start time for quiet hours (no notifications)')
    )
    quiet_hours_end = models.TimeField(
        blank=True,
        null=True,
        help_text=_('End time for quiet hours (no notifications)')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Notification Preference')
        verbose_name_plural = _('Notification Preferences')
        db_table = 'users_notification_preference'
    
    def __str__(self):
        return f"Notification Preferences: {self.user.username}"
    
    def is_quiet_hours(self):
        """Check if current time is within quiet hours."""
        if not self.quiet_hours_start or not self.quiet_hours_end:
            return False
        
        current_time = timezone.now().time()
        if self.quiet_hours_start <= self.quiet_hours_end:
            return self.quiet_hours_start <= current_time <= self.quiet_hours_end
        else:  # Quiet hours span midnight
            return current_time >= self.quiet_hours_start or current_time <= self.quiet_hours_end
