from django.contrib import admin
from .models import Student, Skill, SkillOffer, SkillRequest, Connection, Message, Notification

# --- Custom Admin Actions ---
@admin.action(description='Undo Delete (Restore Selected)')
def restore_connections(modeladmin, request, queryset):
    # This sets is_deleted back to False for all selected items
    queryset.update(is_deleted=False)

# --- Student Admin ---
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'availability', 'bio', 'created_at')
    list_filter = ('availability', 'created_at')
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('created_at',)

# --- Skill Admin ---
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# --- SkillOffer Admin ---
@admin.register(SkillOffer)
class SkillOfferAdmin(admin.ModelAdmin):
    list_display = ('student', 'skill', 'proficiency_level')
    list_filter = ('proficiency_level',)
    search_fields = ('student__user__username', 'skill__name')

# --- SkillRequest Admin ---
@admin.register(SkillRequest)
class SkillRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'skill', 'desired_proficiency')
    list_filter = ('desired_proficiency',)
    search_fields = ('student__user__username', 'skill__name')

# --- Connection Admin (The Undo Feature) ---
@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    # Added 'is_deleted' to display so you can track hidden items
    list_display = ('sender', 'receiver', 'status', 'is_deleted', 'created_at')
    # Added 'is_deleted' to filters for easy searching
    list_filter = ('status', 'is_deleted', 'created_at')
    search_fields = ('sender__user__username', 'receiver__user__username')
    # Register the custom Restore action
    actions = [restore_connections]

# --- Message Admin ---
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('sender__user__username', 'receiver__user__username', 'content')

# --- Notification Admin ---
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('student', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('student__user__username', 'message')