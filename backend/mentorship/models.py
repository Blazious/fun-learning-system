import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from users.models import User


class MentorshipProgram(models.Model):
    """
    Model for managing mentorship programs and initiatives.
    """
    PROGRAM_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text=_('Program name'))
    description = models.TextField(help_text=_('Program description'))
    
    # Program details
    program_type = models.CharField(
        max_length=50,
        choices=[
            ('career', 'Career Development'),
            ('technical', 'Technical Skills'),
            ('leadership', 'Leadership'),
            ('academic', 'Academic'),
            ('personal', 'Personal Development'),
        ],
        default='career'
    )
    
    # Program settings
    max_mentees_per_mentor = models.IntegerField(
        default=5,
        help_text=_('Maximum number of mentees per mentor')
    )
    program_duration_weeks = models.IntegerField(
        default=12,
        help_text=_('Program duration in weeks')
    )
    
    # Program status
    status = models.CharField(
        max_length=20,
        choices=PROGRAM_STATUS_CHOICES,
        default='active'
    )
    is_public = models.BooleanField(default=True)
    
    # Program metadata
    start_date = models.DateField(help_text=_('Program start date'))
    end_date = models.DateField(help_text=_('Program end date'))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='mentorship_programs_created'
    )
    
    class Meta:
        verbose_name = _('Mentorship Program')
        verbose_name_plural = _('Mentorship Programs')
        db_table = 'mentorship_program'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def is_active(self):
        """Check if program is currently active."""
        today = timezone.now().date()
        return (self.status == 'active' and 
                self.start_date <= today <= self.end_date)


class MentorProfile(models.Model):
    """
    Model for managing mentor profiles and expertise.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='mentor_profile'
    )
    
    # Mentor expertise
    expertise_areas = models.JSONField(
        default=list,
        help_text=_('List of expertise areas')
    )
    years_experience = models.IntegerField(
        default=0,
        help_text=_('Years of professional experience')
    )
    
    # Mentorship preferences
    preferred_mentee_level = models.CharField(
        max_length=20,
        choices=[
            ('student', 'Student'),
            ('early_career', 'Early Career'),
            ('mid_career', 'Mid Career'),
            ('any', 'Any Level'),
        ],
        default='any'
    )
    
    # Availability and capacity
    max_mentees = models.IntegerField(
        default=3,
        help_text=_('Maximum number of active mentees')
    )
    available_for_mentorship = models.BooleanField(default=True)
    
    # Mentor statistics
    total_mentees_helped = models.IntegerField(default=0)
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00
    )
    total_sessions = models.IntegerField(default=0)
    
    # Bio and motivation
    bio = models.TextField(blank=True, help_text=_('Mentor bio'))
    motivation = models.TextField(
        blank=True,
        help_text=_('Why they want to mentor')
    )
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(blank=True, null=True)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mentors_verified'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Mentor Profile')
        verbose_name_plural = _('Mentor Profiles')
        db_table = 'mentorship_mentor_profile'
    
    def __str__(self):
        return f"Mentor: {self.user.username}"
    
    def current_mentee_count(self):
        """Get current number of active mentees."""
        return self.mentorship_relationships.filter(
            status='active'
        ).count()
    
    def can_accept_mentees(self):
        """Check if mentor can accept new mentees."""
        return (self.available_for_mentorship and 
                self.current_mentee_count() < self.max_mentees)


class MenteeProfile(models.Model):
    """
    Model for managing mentee profiles and goals.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='mentee_profile'
    )
    
    # Mentee goals and needs
    learning_goals = models.JSONField(
        default=list,
        help_text=_('List of learning goals')
    )
    career_goals = models.TextField(
        blank=True,
        help_text=_('Career goals and aspirations')
    )
    
    # Current status
    current_level = models.CharField(
        max_length=20,
        choices=[
            ('student', 'Student'),
            ('early_career', 'Early Career'),
            ('mid_career', 'Mid Career'),
            ('career_changer', 'Career Changer'),
        ],
        default='student'
    )
    
    # Mentorship preferences
    preferred_mentor_qualities = models.JSONField(
        default=list,
        help_text=_('Preferred mentor qualities')
    )
    preferred_meeting_frequency = models.CharField(
        max_length=20,
        choices=[
            ('weekly', 'Weekly'),
            ('biweekly', 'Bi-weekly'),
            ('monthly', 'Monthly'),
            ('flexible', 'Flexible'),
        ],
        default='weekly'
    )
    
    # Mentee statistics
    total_mentors = models.IntegerField(default=0)
    total_sessions = models.IntegerField(default=0)
    
    # Bio and motivation
    bio = models.TextField(blank=True, help_text=_('Mentee bio'))
    motivation = models.TextField(
        blank=True,
        help_text=_('Why they want to be mentored')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Mentee Profile')
        verbose_name_plural = _('Mentee Profiles')
        db_table = 'mentorship_mentee_profile'
    
    def __str__(self):
        return f"Mentee: {self.user.username}"


class MentorshipRelationship(models.Model):
    """
    Model for managing mentor-mentee relationships.
    """
    RELATIONSHIP_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('terminated', 'Terminated'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey(
        MentorProfile,
        on_delete=models.CASCADE,
        related_name='mentorship_relationships'
    )
    mentee = models.ForeignKey(
        MenteeProfile,
        on_delete=models.CASCADE,
        related_name='mentorship_relationships'
    )
    program = models.ForeignKey(
        MentorshipProgram,
        on_delete=models.CASCADE,
        related_name='relationships'
    )
    
    # Relationship details
    status = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_STATUS_CHOICES,
        default='pending'
    )
    
    # Goals and expectations
    goals = models.JSONField(
        default=list,
        help_text=_('Specific goals for this mentorship')
    )
    expectations = models.TextField(
        blank=True,
        help_text=_('Mentorship expectations')
    )
    
    # Meeting preferences
    preferred_meeting_frequency = models.CharField(
        max_length=20,
        choices=[
            ('weekly', 'Weekly'),
            ('biweekly', 'Bi-weekly'),
            ('monthly', 'Monthly'),
            ('flexible', 'Flexible'),
        ],
        default='weekly'
    )
    
    # Relationship tracking
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    total_sessions = models.IntegerField(default=0)
    
    # Feedback and ratings
    mentee_rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        blank=True,
        null=True
    )
    mentor_rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        blank=True,
        null=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Mentorship Relationship')
        verbose_name_plural = _('Mentorship Relationships')
        db_table = 'mentorship_relationship'
        unique_together = ['mentor', 'mentee', 'program']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.mentor.user.username} → {self.mentee.user.username}"


class MentorshipSession(models.Model):
    """
    Model for managing individual mentorship sessions.
    """
    SESSION_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    relationship = models.ForeignKey(
        MentorshipRelationship,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    
    # Session details
    title = models.CharField(max_length=255, help_text=_('Session title'))
    description = models.TextField(blank=True, help_text=_('Session description'))
    
    # Scheduling
    scheduled_date = models.DateTimeField(help_text=_('Scheduled session date/time'))
    duration_minutes = models.IntegerField(
        default=60,
        help_text=_('Session duration in minutes')
    )
    
    # Meeting details
    meeting_link = models.URLField(blank=True, help_text=_('Meeting link'))
    meeting_platform = models.CharField(
        max_length=50,
        blank=True,
        help_text=_('Meeting platform (Zoom, Google Meet, etc.)')
    )
    
    # Session status
    status = models.CharField(
        max_length=20,
        choices=SESSION_STATUS_CHOICES,
        default='scheduled'
    )
    
    # Session content
    agenda = models.JSONField(
        default=list,
        blank=True,
        help_text=_('Session agenda items')
    )
    notes = models.TextField(
        blank=True,
        help_text=_('Session notes')
    )
    action_items = models.JSONField(
        default=list,
        blank=True,
        help_text=_('Action items from the session')
    )
    
    # Feedback
    mentee_feedback = models.TextField(blank=True)
    mentor_feedback = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = _('Mentorship Session')
        verbose_name_plural = _('Mentorship Sessions')
        db_table = 'mentorship_session'
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.title} - {self.relationship}"
    
    def is_upcoming(self):
        """Check if session is scheduled for the future."""
        return (self.status in ['scheduled', 'confirmed'] and 
                self.scheduled_date > timezone.now())
    
    def is_live(self):
        """Check if session is currently live."""
        return self.status == 'in_progress'
