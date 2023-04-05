from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from .models import Entity, Person, Business


class BaseEntityAdmin(PolymorphicChildModelAdmin):
    base_model = Entity  # Optional, explicitly set here.

    # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # the additional fields of the child models are automatically added to the admin form.
    # base_form = ...
    base_fieldsets = (
    )


@admin.register(Person)
class PersonAdmin(BaseEntityAdmin):
    base_model = Person  # Explicitly set here!
    show_in_index = True  # makes child  admin visible in main admin site
    # define custom features here


@admin.register(Business)
class BusinessAdmin(BaseEntityAdmin):
    base_model = Business  # Explicitly set here!
    show_in_index = True  # makes child  admin visible in main admin site
    # define custom features here


@admin.register(Entity)
class EntityParentAdmin(PolymorphicParentModelAdmin):
    base_model = Entity  # Optional, explicitly set here.
    child_models = (Person, Business)
    list_filter = (PolymorphicChildModelFilter,)  # This is optional.
