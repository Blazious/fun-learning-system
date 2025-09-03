from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Profile, AlumniVerification


class ProfileInline(admin.StackedInline):
    """Inline admin for User Profile."""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = [
        'academic', 'professional', 'bio', 'avatar', 
        'interests', 'social_links', 'role', 'total_points'
    ]
    readonly_fields = ['total_points']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model."""
    
    inlines = [ProfileInline]
    
    list_display = [
        'email', 'username', 'is_verified', 'is_alumni', 
        'is_active', 'date_joined', 'last_login'
    ]
    list_filter = [
        'is_verified', 'is_alumni', 'is_active', 'is_staff', 
        'is_superuser', 'date_joined', 'last_login'
    ]
    search_fields = ['email', 'username']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'is_verified', 'is_alumni',
                'groups', 'user_permissions'
            ),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Profile model."""
    
    list_display = [
        'user', 'role', 'total_points', 'institution_display', 
        'company_display', 'created_at'
    ]
    list_filter = ['role', 'created_at', 'updated_at']
    search_fields = ['user__email', 'user__username', 'bio']
    readonly_fields = ['total_points', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role', 'total_points')
        }),
        ('Academic Information', {
            'fields': ('academic',),
            'description': 'JSON field containing institution, graduation_year, degree_program, current_status'
        }),
        ('Professional Information', {
            'fields': ('professional',),
            'description': 'JSON field containing company, role, experience_level, industry'
        }),
        ('Personal Information', {
            'fields': ('bio', 'avatar', 'interests', 'social_links')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def institution_display(self, obj):
        """Display institution from academic JSON field."""
        academic = obj.academic or {}
        return academic.get('institution', 'N/A')
    institution_display.short_description = 'Institution'
    
    def company_display(self, obj):
        """Display company from professional JSON field."""
        professional = obj.professional or {}
        return professional.get('company', 'N/A')
    company_display.short_description = 'Company'


@admin.register(AlumniVerification)
class AlumniVerificationAdmin(admin.ModelAdmin):
    """Admin configuration for AlumniVerification model."""
    
    list_display = [
        'user', 'institution', 'graduation_year', 'degree_program',
        'verification_status', 'verification_method', 'verified_at', 'created_at'
    ]
    list_filter = [
        'verification_status', 'verification_method', 'graduation_year', 
        'created_at', 'verified_at'
    ]
    search_fields = [
        'user__email', 'user__username', 'institution', 'degree_program'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Institution Details', {
            'fields': ('institution', 'graduation_year', 'degree_program')
        }),
        ('Verification Details', {
            'fields': (
                'verification_status', 'verification_method', 
                'verified_at', 'verified_by', 'verification_data'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_verifications', 'reject_verifications']
    
    def approve_verifications(self, request, queryset):
        """Approve selected verification requests."""
        approved_count = 0
        for verification in queryset.filter(verification_status='pending'):
            verification.mark_as_verified(request.user)
            approved_count += 1
        
        self.message_user(
            request, 
            f'Successfully approved {approved_count} verification request(s).'
        )
    approve_verifications.short_description = 'Approve selected verifications'
    
    def reject_verifications(self, request, queryset):
        """Reject selected verification requests."""
        rejected_count = 0
        for verification in queryset.filter(verification_status='pending'):
            verification.mark_as_rejected(request.user)
            rejected_count += 1
        
        self.message_user(
            request, 
            f'Successfully rejected {rejected_count} verification request(s).'
        )
    reject_verifications.short_description = 'Reject selected verifications'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user', 'verified_by')
