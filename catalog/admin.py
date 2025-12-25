from django.contrib import admin
from .models import Destination, Package, Review, Comment, AirlineFareRule, VisaRequirement


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "region", "is_active")
    search_fields = ("name", "country", "region", "tags")
    list_filter = ("is_active", "country")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("title", "destination", "base_price", "label", "is_active")
    list_filter = ("label", "is_active")
    search_fields = ("title", "destination__name")
    filter_horizontal = ("tours", "hotels", "flights")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "rating", "status", "content_type", "object_id", "created_at")
    list_filter = ("status", "rating", "content_type")
    search_fields = ("user__email", "comment")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "review", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user__email", "content")


@admin.register(AirlineFareRule)
class AirlineFareRuleAdmin(admin.ModelAdmin):
    list_display = ("carrier", "route_type", "trip_type", "base_price", "multiplier_advance", "tax_fee", "is_active")
    list_filter = ("carrier", "route_type", "trip_type", "is_active")
    search_fields = ("carrier",)


@admin.register(VisaRequirement)
class VisaRequirementAdmin(admin.ModelAdmin):
    list_display = ("country_code", "visa_required")
    list_filter = ("visa_required",)
    search_fields = ("country_code",)

