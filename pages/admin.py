from django.contrib import admin

from .models import InventionDisclosure, PipelineCard


@admin.register(InventionDisclosure)
class InventionDisclosureAdmin(admin.ModelAdmin):
    list_display = ("reference_code", "title", "researcher", "technology_area", "created_at")
    search_fields = ("reference_code", "title", "researcher__email")
    list_filter = ("technology_area", "created_at")


@admin.register(PipelineCard)
class PipelineCardAdmin(admin.ModelAdmin):
    list_display = ("disclosure", "stage", "owner_label", "created_at")
    list_filter = ("stage", "created_at")
