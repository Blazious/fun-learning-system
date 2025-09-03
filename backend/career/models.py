import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from users.models import User


class CareerPath(models.Model):
    """
    Model for defining career paths and progression tracks.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text=_('Career path name'))
    description = models.TextField(help_text=_('Career path description'))
    
    # Career path details
    industry = models.CharField(max_length=100, help_text=_('Industry sector'))
    level = models.CharField(
        max_length=20,
        choices=[
            ('entry', 'Entry Level'),
            ('mid', 'Mid Level'),
            ('senior', 'Senior Level'),
            ('lead', 'Lead'),
            ('executive', 'Executive'),
        ],
        default='entry'
    )
    
    # Skills and requirements
    required_skills = models.JSONField(
        default=list,
        help_text=_('List of required skills for this career path')
    )
    recommended_skills = models.JSONField(
        default=list,
        help_text=_('List of recommended skills for this career path')
    )
    
    # Career progression
    next_level = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='previous_level'
    )
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Career Path')
        verbose_name_plural = _('Career Paths')
        db_table = 'career_career_path'
        ordering = ['level', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.level}"


class JobPosting(models.Model):
    """
    Model for managing job postings and opportunities.
    """
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ]
    
    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry Level'),
        ('junior', 'Junior'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
        ('executive', 'Executive'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, help_text=_('Job title'))
    company = models.CharField(max_length=255, help_text=_('Company name'))
    
    # Job details
    description = models.TextField(help_text=_('Job description'))
    requirements = models.TextField(help_text=_('Job requirements'))
    responsibilities = models.TextField(help_text=_('Job responsibilities'))
    
    # Employment details
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='full_time'
    )
    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVEL_CHOICES,
        default='entry'
    )
    
    # Location and compensation
    location = models.CharField(max_length=255, help_text=_('Job location'))
    is_remote = models.BooleanField(default=False, help_text=_('Whether job is remote'))
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('Minimum salary')
    )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('Maximum salary')
    )
    salary_currency = models.CharField(
        max_length=3,
        default='USD',
        help_text=_('Salary currency code')
    )
    
    # Skills and requirements
    required_skills = models.JSONField(
        default=list,
        help_text=_('List of required skills')
    )
    preferred_skills = models.JSONField(
        default=list,
        help_text=_('List of preferred skills')
    )
    
    # Application details
    application_deadline = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_('Application deadline')
    )
    application_url = models.URLField(
        blank=True,
        help_text=_('External application URL')
    )
    
    # Status and visibility
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Metadata
    views_count = models.IntegerField(default=0)
    applications_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='job_postings'
    )
    
    class Meta:
        verbose_name = _('Job Posting')
        verbose_name_plural = _('Job Postings')
        db_table = 'career_job_posting'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    def is_expired(self):
        """Check if job posting has expired."""
        if self.application_deadline:
            return timezone.now() > self.application_deadline
        return False


class Skill(models.Model):
    """
    Model for managing skills and competencies.
    """
    SKILL_CATEGORY_CHOICES = [
        ('technical', 'Technical'),
        ('soft', 'Soft Skills'),
        ('domain', 'Domain Knowledge'),
        ('tool', 'Tools & Technologies'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, help_text=_('Skill name'))
    description = models.TextField(blank=True, help_text=_('Skill description'))
    
    # Skill categorization
    category = models.CharField(
        max_length=20,
        choices=SKILL_CATEGORY_CHOICES,
        default='technical'
    )
    subcategory = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('Skill subcategory')
    )
    
    # Skill metadata
    difficulty_level = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        default=1,
        help_text=_('Skill difficulty level (1-5)')
    )
    is_active = models.BooleanField(default=True)
    
    # Related skills
    related_skills = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        help_text=_('Related skills')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
        db_table = 'career_skill'
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name


class UserSkill(models.Model):
    """
    Model for tracking user skills and proficiency levels.
    """
    PROFICIENCY_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='user_skills'
    )
    
    # Proficiency details
    proficiency_level = models.CharField(
        max_length=20,
        choices=PROFICIENCY_LEVEL_CHOICES,
        default='beginner'
    )
    years_experience = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0,
        help_text=_('Years of experience with this skill')
    )
    
    # Skill validation
    is_verified = models.BooleanField(default=False, help_text=_('Whether skill is verified'))
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='skills_verified'
    )
    verified_at = models.DateTimeField(blank=True, null=True)
    
    # Evidence and portfolio
    portfolio_items = models.JSONField(
        default=list,
        blank=True,
        help_text=_('Portfolio items demonstrating this skill')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User Skill')
        verbose_name_plural = _('User Skills')
        db_table = 'career_user_skill'
        unique_together = ['user', 'skill']
    
    def __str__(self):
        return f"{self.user.username} - {self.skill.name} ({self.proficiency_level})"


class JobApplication(models.Model):
    """
    Model for tracking job applications.
    """
    APPLICATION_STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('reviewing', 'Under Review'),
        ('interviewing', 'Interviewing'),
        ('offered', 'Offer Made'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_posting = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )
    
    # Application details
    cover_letter = models.TextField(blank=True, help_text=_('Cover letter'))
    resume_url = models.URLField(blank=True, help_text=_('Resume/CV URL'))
    
    # Application status
    status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS_CHOICES,
        default='applied'
    )
    
    # Application metadata
    notes = models.TextField(blank=True, help_text=_('Internal notes'))
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_changed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Job Application')
        verbose_name_plural = _('Job Applications')
        db_table = 'career_job_application'
        unique_together = ['job_posting', 'applicant']
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.applicant.username} - {self.job_posting.title}"
