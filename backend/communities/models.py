import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from users.models import User


class Community(models.Model):
    """
    Model for managing learning communities and discussion forums.
    """
    COMMUNITY_TYPE_CHOICES = [
        ('institution', 'Institution'),
        ('subject', 'Subject Matter'),
        ('professional', 'Professional Network'),
        ('interest', 'Interest Group'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, help_text=_('Community name'))
    description = models.TextField(help_text=_('Community description'))
    
    # Community type and categorization
    community_type = models.CharField(
        max_length=20, 
        choices=COMMUNITY_TYPE_CHOICES, 
        default='subject'
    )
    category = models.CharField(
        max_length=100, 
        help_text=_('Main category (e.g., Web Dev, AI/ML, DevOps)')
    )
    
    # Institution-specific fields (if applicable)
    institution = models.CharField(
        max_length=255, 
        blank=True,
        help_text=_('Educational institution name (if institution-based)')
    )
    
    # Community settings
    is_public = models.BooleanField(default=True, help_text=_('Whether community is publicly visible'))
    is_active = models.BooleanField(default=True, help_text=_('Whether community is active'))
    requires_approval = models.BooleanField(
        default=False, 
        help_text=_('Whether joining requires moderator approval')
    )
    
    # Community metadata
    avatar = models.ImageField(
        upload_to='community_avatars/', 
        blank=True, 
        null=True
    )
    banner_image = models.ImageField(
        upload_to='community_banners/', 
        blank=True, 
        null=True
    )
    
    # Statistics
    member_count = models.IntegerField(default=0)
    session_count = models.IntegerField(default=0)
    article_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='communities_created'
    )
    
    class Meta:
        verbose_name = _('Community')
        verbose_name_plural = _('Communities')
        db_table = 'communities_community'
        ordering = ['-member_count']
    
    def __str__(self):
        return self.name
    
    def update_member_count(self):
        """Update the member count."""
        self.member_count = self.members.count()
        self.save(update_fields=['member_count'])


class CommunityMember(models.Model):
    """
    Model for managing community membership and roles.
    """
    MEMBER_ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(
        Community, 
        on_delete=models.CASCADE, 
        related_name='members'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='community_memberships'
    )
    
    # Membership details
    role = models.CharField(
        max_length=20, 
        choices=MEMBER_ROLE_CHOICES, 
        default='member'
    )
    is_active = models.BooleanField(default=True)
    
    # Membership tracking
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(blank=True, null=True)
    
    # Contribution metrics
    sessions_attended = models.IntegerField(default=0)
    sessions_hosted = models.IntegerField(default=0)
    articles_published = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = _('Community Member')
        verbose_name_plural = _('Community Members')
        db_table = 'communities_member'
        unique_together = ['community', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.community.name} ({self.role})"


class CommunityTopic(models.Model):
    """
    Model for managing discussion topics within communities.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(
        Community, 
        on_delete=models.CASCADE, 
        related_name='topics'
    )
    title = models.CharField(max_length=255, help_text=_('Topic title'))
    description = models.TextField(blank=True, help_text=_('Topic description'))
    
    # Topic metadata
    is_pinned = models.BooleanField(default=False, help_text=_('Whether topic is pinned'))
    is_locked = models.BooleanField(default=False, help_text=_('Whether topic is locked for new posts'))
    
    # Statistics
    post_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='topics_created'
    )
    
    class Meta:
        verbose_name = _('Community Topic')
        verbose_name_plural = _('Community Topics')
        db_table = 'communities_topic'
        ordering = ['-is_pinned', '-updated_at']
    
    def __str__(self):
        return f"{self.title} - {self.community.name}"


class CommunityPost(models.Model):
    """
    Model for managing posts and discussions within community topics.
    """
    POST_TYPE_CHOICES = [
        ('discussion', 'Discussion'),
        ('question', 'Question'),
        ('announcement', 'Announcement'),
        ('resource', 'Resource Share'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(
        CommunityTopic, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='community_posts'
    )
    
    # Post content
    post_type = models.CharField(
        max_length=20, 
        choices=POST_TYPE_CHOICES, 
        default='discussion'
    )
    title = models.CharField(max_length=255, help_text=_('Post title'))
    content = models.TextField(help_text=_('Post content'))
    
    # Post metadata
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    
    # Engagement metrics
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Community Post')
        verbose_name_plural = _('Community Posts')
        db_table = 'communities_post'
        ordering = ['-is_pinned', '-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"


class CommunityArticle(models.Model):
    """
    Model for managing knowledge articles and blog posts within communities.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(
        Community, 
        on_delete=models.CASCADE, 
        related_name='articles'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='community_articles'
    )
    
    # Article content
    title = models.CharField(max_length=255, help_text=_('Article title'))
    content = models.TextField(help_text=_('Article content'))
    excerpt = models.TextField(
        blank=True, 
        help_text=_('Short excerpt/summary of the article')
    )
    
    # Article metadata
    tags = models.JSONField(
        default=list, 
        blank=True,
        help_text=_('List of tags for the article')
    )
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    
    # Engagement metrics
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = _('Community Article')
        verbose_name_plural = _('Community Articles')
        db_table = 'communities_article'
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
