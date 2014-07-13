from django.contrib import admin
from ..attachments.admin import PhotoInlineAdmin
from .models import Project, Activity, Markers, ChannelReported, Organization, AnnualFunds


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        PhotoInlineAdmin,
    ]


class AnnualFundsInlineAdmin(admin.TabularInline):
    model = AnnualFunds
    extra = 1

class OrganizationAdmin(admin.ModelAdmin):
    inlines = [
        AnnualFundsInlineAdmin,
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Activity)
admin.site.register(Markers)
admin.site.register(ChannelReported)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(AnnualFunds)
