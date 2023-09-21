from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from envergo.geodata.models import Map
from envergo.moulinette.models import Criterion, MoulinetteConfig, Perimeter, Regulation
from envergo.moulinette.regulations import CriterionEvaluator


@admin.register(Regulation)
class RegulationAdmin(admin.ModelAdmin):
    list_display = ["get_regulation_display", "regulation_slug", "has_perimeters"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("weight")

    @admin.display(description=_("Regulation slug"))
    def regulation_slug(self, obj):
        return obj.regulation


class CriterionAdminForm(forms.ModelForm):
    def get_initial_for_field(self, field, field_name):
        """Prevent Evaluator choice to be instanciated.

        In the legacy's version of this function, callable values are, well,
        called.

        But since we have a custom field that should return
        `CriterionEvaluator` subclasses, we don't want the form to actually
        instanciate those classes.
        """

        value = self.initial.get(field_name, field.initial)
        if callable(value) and not issubclass(value, CriterionEvaluator):
            value = value()
        return value

    def clean(self):
        """Ensure required action and stake are both set if one is set."""

        data = super().clean()
        has_required_action = bool(data.get("required_action"))
        has_stake = bool(data.get("required_action_stake"))
        if any([has_required_action, has_stake]) and not all(
            [has_required_action, has_stake]
        ):
            raise forms.ValidationError(
                "Both required action and stake are required if one is set."
            )
        return data


@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
    list_display = [
        "backend_title",
        "slug",
        "regulation",
        "activation_map",
        "activation_distance",
        "evaluator_column",
    ]
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ["unique_slug"]
    form = CriterionAdminForm

    @admin.display(description=_("Evaluator"))
    def evaluator_column(self, obj):
        return obj.evaluator.choice_label


class PerimeterAdminForm(forms.ModelForm):
    def get_initial_for_field(self, field, field_name):
        """Prevent Criterion choice to be instanciated.

        In the legacy's version of this function, callable values are, well,
        called.

        But since we have a custom field that should return
        `MoulinetteCriterion` subclasses, we don't want the form to actually
        instanciate those classes.
        """

        value = self.initial.get(field_name, field.initial)
        if callable(value) and not getattr(value, "do_not_call_in_templates", False):
            value = value()
        return value


@admin.register(Perimeter)
class PerimeterAdmin(admin.ModelAdmin):
    list_display = [
        "backend_name",
        "name",
        "regulation",
        "activation_map",
        "activation_distance",
    ]
    form = PerimeterAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit map choices to those with empty "map type".

        Maps for wetlands or flood zones are not used for perimeters.

        Also, I find it weird that there is no better way to filter foreign key
        choices.
        """
        if db_field.name == "map":
            kwargs["queryset"] = Map.objects.filter(map_type="")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MoulinetteConfigForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["n2000_lotissement_proximite"].strip = False


@admin.register(MoulinetteConfig)
class MoulinetteConfigAdmin(admin.ModelAdmin):
    list_display = ["department", "is_activated"]
    form = MoulinetteConfigForm
