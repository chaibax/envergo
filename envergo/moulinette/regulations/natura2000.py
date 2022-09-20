from functools import cached_property

from django import forms
from django.contrib.gis.db.models import MultiPolygonField, Union
from django.db.models import F
from django.db.models.functions import Cast
from django.utils.translation import gettext_lazy as _

from envergo.evaluations.models import RESULTS
from envergo.moulinette.regulations import (
    Map,
    MoulinetteCriterion,
    MoulinetteRegulation,
)


class ZoneHumide44(MoulinetteCriterion):
    slug = "zone_humide_44"
    choice_label = "Natura 2000 > 44 - Zone humide"
    title = "Impact sur zone humide Natura 2000"
    subtitle = "Seuil de déclaration : 100 m²"
    header = "« Liste locale 2 » Natura 2000 en Loire-Atlantique (10° de l'art. 1 de l'<a href='/static/pdfs/arrete_08042014.pdf' target='_blank' rel='noopener'>arrêté préfectoral du 8 avril 2014</a>)"  # noqa

    def get_catalog_data(self):
        data = {}
        data["wetlands_within_25m"] = bool(self.catalog["wetlands_25"])
        data["wetlands_within_100m"] = bool(self.catalog["wetlands_100"])
        data["within_potential_wetlands"] = bool(self.catalog["potential_wetlands"])
        return data

    def get_result_data(self):
        """Evaluate the project and return the different parameter results.

        For this criterion, the evaluation results depends on the project size
        and wether it will impact known wetlands.
        """

        if self.catalog["wetlands_within_25m"]:
            wetland_status = "inside"
        elif self.catalog["wetlands_within_100m"]:
            wetland_status = "close_to"
        elif self.catalog["within_potential_wetlands"]:
            wetland_status = "inside_potential"
        else:
            wetland_status = "outside"

        if self.catalog["created_surface"] >= 100:
            project_size = "big"
        else:
            project_size = "small"

        return wetland_status, project_size

    @property
    def result_code(self):
        """Return the unique result code"""

        wetland_status, project_size = self.get_result_data()
        code_matrix = {
            ("inside", "big"): "soumis",
            ("inside", "small"): "non_soumis",
            ("close_to", "big"): "action_requise_proche",
            ("close_to", "small"): "non_soumis_proche",
            ("inside_potential", "big"): "action_requise_dans_doute",
            ("inside_potential", "small"): "non_soumis_dans_doute",
            ("outside", "big"): "non_concerne",
            ("outside", "small"): "non_concerne",
        }
        code = code_matrix[(wetland_status, project_size)]
        return code

    @cached_property
    def result(self):
        """Run the check for the 3.3.1.0 rule.

        Associate a unique result code with a value from the RESULTS enum.
        """

        code = self.result_code
        result_matrix = {
            "soumis": RESULTS.soumis,
            "non_soumis": RESULTS.non_soumis,
            "action_requise_proche": RESULTS.action_requise,
            "non_soumis_proche": RESULTS.non_soumis,
            "action_requise_dans_doute": RESULTS.action_requise,
            "non_soumis_dans_doute": RESULTS.non_soumis,
            "non_concerne": RESULTS.non_concerne,
        }
        result = result_matrix[code]
        return result

    def _get_map(self):

        inside_qs = self.catalog["wetlands_25"].filter(map__display_for_user=True)
        close_qs = self.catalog["wetlands_100"].filter(map__display_for_user=True)
        potential_qs = self.catalog["potential_wetlands"].filter(
            map__display_for_user=True
        )
        polygons = None

        if inside_qs:
            caption = "Le projet se situe dans une zone humide référencée."
            geometries = inside_qs.annotate(geom=Cast("geometry", MultiPolygonField()))
            polygons = [
                {
                    "polygon": geometries.aggregate(polygon=Union(F("geom")))[
                        "polygon"
                    ],
                    "color": "blue",
                    "label": "Zone humide",
                }
            ]
            maps = set([zone.map for zone in inside_qs.select_related("map")])

        elif close_qs and not potential_qs:
            caption = "Le projet se situe à proximité d'une zone humide référencée."
            geometries = close_qs.annotate(geom=Cast("geometry", MultiPolygonField()))
            polygons = [
                {
                    "polygon": geometries.aggregate(polygon=Union(F("geom")))[
                        "polygon"
                    ],
                    "color": "blue",
                    "label": "Zone humide",
                }
            ]
            maps = set([zone.map for zone in close_qs.select_related("map")])

        elif close_qs and potential_qs:
            caption = "Le projet se situe à proximité d'une zone humide référencée et dans une zone humide potentielle."
            geometries = close_qs.annotate(geom=Cast("geometry", MultiPolygonField()))
            wetlands_polygon = geometries.aggregate(polygon=Union(F("geom")))["polygon"]

            geometries = potential_qs.annotate(
                geom=Cast("geometry", MultiPolygonField())
            )
            potentials_polygon = geometries.aggregate(polygon=Union(F("geom")))[
                "polygon"
            ]

            polygons = [
                {"polygon": wetlands_polygon, "color": "blue", "label": "Zone humide"},
                {
                    "polygon": potentials_polygon,
                    "color": "lightblue",
                    "label": "ZH potentielle",
                },
            ]
            wetlands_maps = [zone.map for zone in close_qs.select_related("map")]
            potential_maps = [zone.map for zone in potential_qs.select_related("map")]
            maps = set(wetlands_maps + potential_maps)

        elif potential_qs:
            caption = "Le projet se situe dans une zone humide potentielle."
            geometries = potential_qs.annotate(
                geom=Cast("geometry", MultiPolygonField())
            )
            polygons = [
                {
                    "polygon": geometries.aggregate(polygon=Union(F("geom")))[
                        "polygon"
                    ],
                    "color": "dodgerblue",
                    "label": "Zone humide potentielle",
                }
            ]
            maps = set([zone.map for zone in potential_qs.select_related("map")])

        if polygons:
            criterion_map = Map(
                center=self.catalog["coords"],
                polygons=polygons,
                caption=caption,
                sources=maps,
            )
        else:
            criterion_map = None

        return criterion_map


class ZoneInondable44(MoulinetteCriterion):
    slug = "zone_inondable_44"
    choice_label = "Natura 2000 > 44 - Zone inondable"
    title = "Impact sur zone inondable Natura 2000"
    subtitle = "Seuil de déclaration : 200 m²"
    header = "« Liste locale 2 » Natura 2000 en Loire-Atlantique (13° de l'art. 1 de l'<a href='/static/pdfs/arrete_08042014.pdf' target='_blank' rel='noopener'>arrêté préfectoral du 8 avril 2014</a>)"  # noqa

    def get_catalog_data(self):
        data = {}
        data["flood_zones_within_12m"] = bool(self.catalog["flood_zones_12"])
        return data

    @cached_property
    def result_code(self):
        """Run the check for the 3.1.2.0 rule."""

        if self.catalog["flood_zones_within_12m"]:
            flood_zone_status = "inside"
        else:
            flood_zone_status = "outside"

        if self.catalog["created_surface"] >= 200:
            project_size = "big"
        else:
            project_size = "small"

        result_matrix = {
            "inside": {
                "big": RESULTS.soumis,
                "small": RESULTS.non_soumis,
            },
            "outside": {
                "big": RESULTS.non_applicable,
                "small": RESULTS.non_applicable,
            },
        }

        result = result_matrix[flood_zone_status][project_size]
        return result

    def _get_map(self):
        zone_qs = self.catalog["flood_zones_12"].filter(map__display_for_user=True)
        polygons = None

        if zone_qs:
            caption = "Le projet se situe dans une zone inondable."
            geometries = zone_qs.annotate(geom=Cast("geometry", MultiPolygonField()))
            polygons = [
                {
                    "polygon": [
                        geometries.aggregate(polygon=Union(F("geom")))["polygon"]
                    ][0],
                    "color": "red",
                    "label": "Zone inondable",
                }
            ]
            maps = set([zone.map for zone in zone_qs.select_related("map")])

        if polygons:
            criterion_map = Map(
                center=self.catalog["coords"],
                polygons=polygons,
                caption=caption,
                sources=maps,
            )
        else:
            criterion_map = None

        return criterion_map


class IOTA(MoulinetteCriterion):
    slug = "iota"
    choice_label = "Natura 2000 > IOTA"
    title = "Projet soumis à la Loi sur l'eau"
    header = "« Liste nationale » Natura 2000 (4° du I de l'<a href='https://www.legifrance.gouv.fr/codes/id/LEGISCTA000022090322/' target='_blank' rel='noopener'>article R414-19 du Code de l'Environnement</a>)"  # noqa

    @cached_property
    def result_code(self):
        return self.moulinette.loi_sur_leau.result


class LotissementForm(forms.Form):

    # I sacrificed a frog to the god of bad translations for the right to use
    # this variable name. Sorry.
    is_lotissement = forms.ChoiceField(
        label=_("Le projet concerne-t-il un lotissement ?"),
        widget=forms.RadioSelect,
        choices=(("oui", "Oui"), ("non", "Non")),
        required=True,
    )


class Lotissement44(MoulinetteCriterion):
    slug = "lotissement_44"
    choice_label = "Natura 2000 > 44 - Lotissement"
    title = "Lotissement dans zone Natura 2000"
    header = "« Liste locale 1 » Natura 2000 en Loire-Atlantique (1° de l'art. 2 de l'<a href='/static/pdfs/arrete_16062011.pdf' target='_blank' rel='noopener'>arrêté préfectoral du 16 juin 2011</a>)"  # noqa
    form_class = LotissementForm

    @cached_property
    def result_code(self):

        form = self.get_form()
        if form.is_valid():
            is_lotissement = form.cleaned_data["is_lotissement"] == "oui"
            return "soumis" if is_lotissement else "non_soumis"

        return "non_disponible"


class Natura2000(MoulinetteRegulation):
    slug = "natura2000"
    title = "Natura 2000"
    criterion_classes = [ZoneHumide44, ZoneInondable44, IOTA, Lotissement44]

    def _get_map(self):
        """Display a Natura 2000 map if a single criterion has been activated.

        Since there is probably a single Natura 2000 map for all Natura 2000
        criterions, we only display a single polygon and a single map source.
        """

        # We don't display the map if only the IOTA criterion is activated
        # because it means the project is submitted to N2000 without being
        # in a N2000 zone
        crits = self.criterions
        if len(crits) == 0 or len(crits) == 1 and isinstance(crits[0], IOTA):
            return None

        geometries = [
            p.geometry
            for p in self.moulinette.perimeters
            if p.criterion in self.criterion_classes
        ]
        polygons = [
            {
                "polygon": geometry,
                "color": "green",
                "label": "Site Natura 2000",
            }
            for geometry in geometries[:1]
        ]
        maps = [
            p.map
            for p in self.moulinette.perimeters
            if p.criterion in self.criterion_classes
        ]

        caption = "Le projet se situe sur un site Natura 2000."
        map = Map(
            center=self.catalog["coords"],
            polygons=polygons,
            caption=caption,
            sources=maps[:1],
            truncate=False,
        )

        return map