from django.contrib import admin

from .models import (
    About,
    Certification,
    ContactMessage,
    Education,
    Experience,
    FAQ,
    Language,
    Project,
    Service,
    Skill,
    Stat,
    Testimonial,
    Value,
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_live', 'is_featured', 'order')
    list_editable = ('is_live', 'is_featured', 'order')
    list_filter = ('category', 'is_live', 'is_featured')
    search_fields = ('title', 'short_desc', 'tech_stack')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon', 'level', 'order')
    list_editable = ('icon', 'level', 'order')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'headline', 'location', 'available')

    def has_add_permission(self, request):
        # Instance unique
        return not About.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order')
    list_editable = ('icon', 'order')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'period', 'order')
    list_editable = ('order',)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'school', 'period', 'order')
    list_editable = ('order',)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'order')
    list_editable = ('status', 'order')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'order')
    list_editable = ('level', 'order')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_role', 'is_active', 'order')
    list_editable = ('is_active', 'order')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'suffix', 'order')
    list_editable = ('value', 'suffix', 'order')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'project_type', 'created_at', 'is_read')
    list_filter = ('is_read', 'project_type', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'subject', 'project_type', 'message', 'created_at')

    def has_add_permission(self, request):
        return False
