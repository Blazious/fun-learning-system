import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from users.models import User


class Session(models.Model):
    """
    Model for managing keynote sessions and learning events.
    """
    SESSION_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    SESSION_TYPE_CHOICES = [
        ('keynote', 'Keynote'),
        ('workshop', 'Workshop'),
        ('panel', 'Panel Discussion'),
        ('qna', 'Q&A Session'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, help_text=_('Session title'))
    description = models.TextField(help_text=_('Detailed session description'))
    
    # Session details
    session_type = models.CharField(
        max_length=20, 
        choices=SESSION_TYPE_CHOICES, 
        default='keynote'
    )
    status = models.CharField(
        max_length=20, 
        choices=SESSION_STATUS_CHOICES, 
        default='draft'
    )
    
    # Scheduling
    scheduled_date = models.DateTimeField(help_text=_('When the session is scheduled'))
    duration_minutes = models.IntegerField(default=60, help_text=_('Session duration in minutes'))
    
    # Meeting details
    meeting_link = models.URLField(blank=True, help_text=_('Zoom, Google Meet, or platform link'))
    meeting_platform = models.CharField(
        max_length=50, 
        blank=True,
        help_text=_('Platform used for the session (Zoom, Google Meet, etc.)')
    )
    
    # Participants
    speaker = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sessions_as_speaker'
    )
    moderator = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='sessions_as_moderator'
    )
    
    # Community and topics
    community = models.ForeignKey(
        'communities.Community', 
        on_delete=models.CASCADE, 
        related_name='sessions'
    )
    topics = models.JSONField(
        default=list, 
        blank=True,
        help_text=_('List of topics covered in this session')
    )
    
    # Session metadata
    max_participants = models.IntegerField(
        default=100, 
        help_text=_('Maximum number of participants allowed')
    )
    is_public = models.BooleanField(default=True, help_text=_('Whether session is publicly visible'))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = _('Session')
        verbose_name_plural = _('Sessions')
        db_table = 'sessions_session'
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.title} - {self.speaker.username}"
    
    def is_upcoming(self):
        """Check if session is scheduled for the future."""
        return self.status == 'scheduled' and self.scheduled_date > timezone.now()
    
    def is_live(self):
        """Check if session is currently live."""
        return self.status == 'live'
    
    def can_join(self):
        """Check if users can still join the session."""
        return self.status in ['scheduled', 'live'] and self.participants.count() < self.max_participants


class SessionParticipant(models.Model):
    """
    Model for tracking session participants and their roles.
    """
    PARTICIPANT_ROLE_CHOICES = [
        ('attendee', 'Attendee'),
        ('speaker', 'Speaker'),
        ('moderator', 'Moderator'),
        ('observer', 'Observer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        Session, 
        on_delete=models.CASCADE, 
        related_name='participants'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='session_participations'
    )
    role = models.CharField(
        max_length=20, 
        choices=PARTICIPANT_ROLE_CHOICES, 
        default='attendee'
    )
    
    # Participation tracking
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(blank=True, null=True)
    duration_attended = models.IntegerField(
        default=0, 
        help_text=_('Total minutes attended')
    )
    
    # Engagement metrics
    asked_questions = models.IntegerField(default=0)
    provided_feedback = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('Session Participant')
        verbose_name_plural = _('Session Participants')
        db_table = 'sessions_participant'
        unique_together = ['session', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.session.title} ({self.role})"


class SessionRecording(models.Model):
    """
    Model for storing session recordings and metadata.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.OneToOneField(
        Session, 
        on_delete=models.CASCADE, 
        related_name='recording'
    )
    
    # Recording details
    recording_url = models.URLField(help_text=_('URL to the recorded session'))
    thumbnail_url = models.URLField(blank=True, help_text=_('Thumbnail image for the recording'))
    duration_seconds = models.IntegerField(help_text=_('Recording duration in seconds'))
    
    # Processing status
    processing_status = models.CharField(
        max_length=20, 
        choices=[
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='processing'
    )
    
    # Analytics
    views_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = _('Session Recording')
        verbose_name_plural = _('Session Recordings')
        db_table = 'sessions_recording'
    
    def __str__(self):
        return f"Recording: {self.session.title}"


class SessionFeedback(models.Model):
    """
    Model for collecting feedback and ratings after sessions.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        Session, 
        on_delete=models.CASCADE, 
        related_name='feedback'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='session_feedback'
    )
    
    # Rating and feedback
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text=_('Rating from 1 to 5')
    )
    comment = models.TextField(blank=True, help_text=_('Optional feedback comment'))
    
    # Specific feedback categories
    content_quality = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        blank=True, 
        null=True
    )
    speaker_effectiveness = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        blank=True, 
        null=True
    )
    technical_quality = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        blank=True, 
        null=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Session Feedback')
        verbose_name_plural = _('Session Feedback')
        db_table = 'sessions_feedback'
        unique_together = ['session', 'user']
    
    def __str__(self):
        return f"Feedback from {self.user.username} on {self.session.title}"
