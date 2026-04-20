from django.contrib import admin
from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
)
from .models import Business, Entity, EntityMerge, Person


class BaseEntityAdmin(PolymorphicChildModelAdmin):
    base_model = Entity  # Optional, explicitly set here.

    # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # the additional fields of the child models are automatically added to the admin form.
    # base_form = ...
    # base_fieldsets = ()


@admin.register(Person)
class PersonAdmin(BaseEntityAdmin):
    base_model = Person  # Explicitly set here!
    show_in_index = True  # makes child  admin visible in main admin site
    # define custom features here
    search_fields = ("name", "canonical__name")
    list_filter = ("active",)
    list_display = (
        "entity_ptr",
        # "entity_ptr__active",
        # "entity_ptr__canonical",
        "name_parsed",
    )


@admin.register(Business)
class BusinessAdmin(BaseEntityAdmin):
    base_model = Business  # Explicitly set here!
    show_in_index = True  # makes child  admin visible in main admin site
    # define custom features here


@admin.register(Entity)
class EntityParentAdmin(PolymorphicParentModelAdmin):
    base_model = Entity  # Optional, explicitly set here.
    child_models = (Person, Business)
    list_filter = (PolymorphicChildModelFilter, "active")
    list_display = (
        "name",
        "active",
        "canonical",
    )
    search_fields = ("name",)


@admin.register(EntityMerge)
class EntityMergeAdmin(admin.ModelAdmin):
    list_display = (
        "merged_entity",
        "surviving_entity",
        "status",
        "performed_by",
        "performed_at",
    )
    list_filter = ("status",)
    search_fields = ("merged_entity__name", "surviving_entity__name", "reason")
    readonly_fields = ("performed_at", "reverted_at")
    autocomplete_fields = ("surviving_entity", "merged_entity", "performed_by", "reverted_by")
