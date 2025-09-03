from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin   # ✅ import the correct admin
from axes.models import AccessAttempt
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from .models import Tenant, Document, TenantType, DocumentType, ExpiryRule, TenantExpiryRule
from simple_history.admin import SimpleHistoryAdmin


# ------------------------------
# Unregister default User admin
# ------------------------------
admin.site.unregister(User)


# ------------------------------
# Tenant-related admins
# ------------------------------
@admin.register(Tenant)
class TenantAdmin(SimpleHistoryAdmin):
    list_display = ("name", "email", "tenant_type_fk", "created_at")
    search_fields = ("name", "email")
    list_filter = ("tenant_type_fk",)


@admin.register(Document)
class DocumentAdmin(SimpleHistoryAdmin):
    list_display = ("tenant", "doc_type_fk", "upload_date", "commencement_date", "expiry_date")
    list_filter = ("doc_type_fk", "commencement_date", "expiry_date")
    search_fields = ("tenant__name",)


admin.site.register(TenantType)
admin.site.register(DocumentType)


@admin.register(ExpiryRule)
class ExpiryRuleAdmin(admin.ModelAdmin):
    list_display = ("tenant_type", "doc_type", "days_valid")
    list_filter = ("tenant_type", "doc_type")
    search_fields = ("tenant_type__label", "doc_type__label")


@admin.register(TenantExpiryRule)
class TenantExpiryRuleAdmin(admin.ModelAdmin):
    list_display = ("tenant", "doc_type", "days_valid")
    list_filter = ("tenant", "doc_type")
    search_fields = ("tenant__name", "doc_type__label")


# ------------------------------
# Custom User admin
# ------------------------------
@admin.register(User)
class CustomUserAdmin(UserAdmin):   # ✅ extend from UserAdmin, not ModelAdmin
    list_display = UserAdmin.list_display + ('locked_out', 'unlock_button')
    actions = ['unlock_selected_users']

    def locked_out(self, obj):
        """Check if user is currently locked out by django-axes."""
        return AccessAttempt.objects.filter(username=obj.username).exists()
    locked_out.boolean = True
    locked_out.short_description = 'Locked Out?'

    def unlock_selected_users(self, request, queryset):
        """Bulk unlock selected users."""
        count = 0
        for user in queryset:
            deleted, _ = AccessAttempt.objects.filter(username=user.username).delete()
            if deleted:
                count += 1
        self.message_user(request, f"{count} user(s) unlocked successfully.")
    unlock_selected_users.short_description = "Unlock selected users"

    def unlock_button(self, obj):
        """Show 'Unlock' button in user list view."""
        if AccessAttempt.objects.filter(username=obj.username).exists():
            return format_html('<a class="button" href="{}">Unlock</a>', f'{obj.id}/unlock/')
        return "-"
    unlock_button.short_description = 'Unlock User'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/unlock/', self.admin_site.admin_view(self.unlock_user_view), name='unlock_user'),
        ]
        return custom_urls + urls

    def unlock_user_view(self, request, user_id):
        """Unlock a single user by deleting AccessAttempt records."""
        user = User.objects.get(pk=user_id)
        AccessAttempt.objects.filter(username=user.username).delete()
        self.message_user(request, f"User '{user.username}' unlocked successfully.")
        return redirect(request.META.get('HTTP_REFERER', '/admin/auth/user/'))
