
from django.contrib import admin

from .models import (
    ImpactStat,
    Story,
    Program,
    Campaign,
    Project,
    MediaItem,
    PressRelease,
    ElectronicMedia,
    BlogPost,
    Event,
    VolunteerApplication,
    PartnershipInquiry,
    Partner,
    FundraisingCampaign,
    NewsletterSubscriber,
    ContactMessage,
    Donation,
    BannerSlide,
    HomePageContent,
)


admin.site.site_header = "Nayaa Administration"
admin.site.site_title = "Nayaa Admin"
admin.site.index_title = "Manage Nayaa Website"


@admin.register(BannerSlide)
class BannerSlideAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "active")
    list_editable = ("order", "active")
    search_fields = ("title", "description")
    list_filter = ("active",)
    ordering = ("order",)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "order", "active")
    list_editable = ("order", "active")
    search_fields = ("name", "description")
    list_filter = ("active",)
    ordering = ("order", "name")


@admin.register(ImpactStat)
class ImpactStatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "order", "active")
    list_editable = ("order", "active")
    search_fields = ("label", "value")
    list_filter = ("active",)
    ordering = ("order",)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "active")
    list_editable = ("active",)
    search_fields = ("title", "summary")
    list_filter = ("category", "active")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "sector",
        "status",
        "verified",
    )

    list_editable = (
        "status",
        "verified",
    )

    search_fields = (
        "title",
        "sector",
        "description",
        "location",
        "beneficiaries",
    )

    list_filter = (
        "status",
        "sector",
        "verified",
    )

    ordering = ("title",)


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):

    list_display = (
        "vision_title",
        "mission_title",
        "last_updated",
    )

    fieldsets = (
        ("Vision", {
            "fields": (
                "vision_title",
                "vision_description",
            )
        }),
        ("Mission", {
            "fields": (
                "mission_title",
                "mission_description",
            )
        }),
    )

    readonly_fields = ("last_updated",)


# Other models

for model in [
    Story,
    Campaign,
    MediaItem,
    PressRelease,
    ElectronicMedia,
    BlogPost,
    Event,
    VolunteerApplication,
    PartnershipInquiry,
    FundraisingCampaign,
    NewsletterSubscriber,
    ContactMessage,
    Donation,
]:
    admin.site.register(model)
