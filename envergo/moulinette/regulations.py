from functools import cached_property

from django.contrib.gis.measure import Distance as D
from model_utils import Choices

from envergo.evaluations.models import RESULTS
from envergo.geodata.models import Zone


def fetch_zones_around(coords, radius, zone_type, data_certainty="certain"):
    """Helper method to fetch Zones around a given point."""

    qs = (
        Zone.objects.filter(map__data_type=zone_type)
        .filter(geometry__dwithin=(coords, D(m=radius)))
        .filter(map__data_certainty=data_certainty)
    )
    return qs


# Those dummy methods are useful for unit testing
def fetch_wetlands_around_25m(coords):
    return fetch_zones_around(coords, 25, "zone_humide")


def fetch_wetlands_around_100m(coords):
    return fetch_zones_around(coords, 100, "zone_humide")


def fetch_potential_wetlands(coords):
    qs = (
        Zone.objects.filter(map__data_type="zone_humide")
        .filter(map__data_certainty="uncertain")
        .filter(geometry__dwithin=(coords, D(m=0)))
    )
    return qs


def fetch_flood_zones_around_12m(coords):
    return fetch_zones_around(coords, 12, "zone_inondable")


class MoulinetteRegulation:
    """Run the moulinette for a single regulation (e.g Loi sur l'eau)."""

    criterion_classes = []

    def __init__(self, data_catalog):
        self.catalog = data_catalog
        self.catalog.update(self.get_catalog_data())
        self.criterions = [
            Criterion(self.catalog) for Criterion in self.criterion_classes
        ]

    def get_catalog_data(self):
        return {}

    @cached_property
    def result(self):
        """Compute global result from individual criterions."""

        results = [criterion.result for criterion in self.criterions]

        if RESULTS.soumis in results:
            result = RESULTS.soumis
        elif RESULTS.action_requise in results:
            result = RESULTS.action_requise
        else:
            result = RESULTS.non_soumis

        return result

    def __getattr__(self, attr):
        """Returs the corresponding criterion.

        Allows to do something like this:
        moulinette.loi_sur_leau.zones_inondables to fetch the correct criterion.
        """
        return self.get_criterion(attr)

    def get_criterion(self, criterion_slug):
        """Return the regulation with the given slug."""

        def select_criterion(criterion):
            return criterion.slug == criterion_slug

        criterion = next(filter(select_criterion, self.criterions), None)
        return criterion


class MoulinetteCriterion:
    """Run a single moulinette check."""

    def __init__(self, data_catalog):
        self.catalog = data_catalog
        self.catalog.update(self.get_catalog_data())

    def get_catalog_data(self):
        return {}

    @cached_property
    def result(self):
        raise NotImplementedError("Implement the `result` method in the subclass.")

    @property
    def result_code(self):
        """Return a unique code for the criterion result.

        Sometimes, a same criterion can have the same result for different reasons.
        Because of this, we want unique codes to display custom messages to
        the user.
        """

        return self.result


class WaterLaw3310(MoulinetteCriterion):
    slug = "zone_humide"
    title = "Construction en zone humide"
    subtitle = "Seuil de déclaration : 1000 m²"

    def get_catalog_data(self):
        catalog = {}
        catalog["wetlands_25"] = fetch_wetlands_around_25m(self.catalog["coords"])
        catalog["wetlands_within_25m"] = bool(catalog["wetlands_25"])
        catalog["wetlands_100"] = fetch_wetlands_around_100m(self.catalog["coords"])
        catalog["wetlands_within_100m"] = bool(catalog["wetlands_100"])
        catalog["potential_wetlands"] = fetch_potential_wetlands(self.catalog["coords"])
        catalog["within_potential_wetlands"] = bool(catalog["potential_wetlands"])

        return catalog

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

        if self.catalog["project_surface"] >= 1000:
            project_size = "big"
        elif self.catalog["project_surface"] >= 700:
            project_size = "medium"
        else:
            project_size = "small"

        return wetland_status, project_size

    @cached_property
    def result(self):
        """Run the check for the 3.3.1.0 rule.

        Associate a unique result code with a value from the RESULTS enum.
        """

        code = self.result_code
        result_matrix = {
            "soumis": RESULTS.soumis,
            "non_soumis": RESULTS.non_soumis,
            "non_applicable": RESULTS.non_applicable,
            "action_requise_inside": RESULTS.action_requise,
            "action_requise_close_to": RESULTS.action_requise,
            "action_requise_inside_potential": RESULTS.action_requise,
        }
        result = result_matrix[code]
        return result

    @property
    def result_code(self):
        """Return the unique result code"""

        wetland_status, project_size = self.get_result_data()
        code_matrix = {
            ("inside", "big"): "soumis",
            ("inside", "medium"): "action_requise_inside",
            ("inside", "small"): "non_soumis",
            ("close_to", "big"): "action_requise_close_to",
            ("close_to", "medium"): "non_soumis",
            ("close_to", "small"): "non_soumis",
            ("inside_potential", "big"): "action_requise_inside_potential",
            ("inside_potential", "medium"): "non_soumis",
            ("inside_potential", "small"): "non_soumis",
            ("outside", "big"): "non_applicable",
            ("outside", "medium"): "non_applicable",
            ("outside", "small"): "non_soumis",
        }
        code = code_matrix[(wetland_status, project_size)]
        return code


class WaterLaw3220(MoulinetteCriterion):
    slug = "zone_inondable"
    title = "Construction en zone inondable"
    subtitle = "Seuil de déclaration : 400 m²"

    def get_catalog_data(self):
        catalog = {}
        catalog["flood_zones_12"] = fetch_flood_zones_around_12m(self.catalog["coords"])
        catalog["flood_zones_within_12m"] = bool(catalog["flood_zones_12"])
        return catalog

    @cached_property
    def result(self):
        """Run the check for the 3.1.2.0 rule."""

        if self.catalog["flood_zones_within_12m"]:
            flood_zone_status = "inside"
        else:
            flood_zone_status = "outside"

        if self.catalog["project_surface"] >= 400:
            project_size = "big"
        elif self.catalog["project_surface"] >= 300:
            project_size = "medium"
        else:
            project_size = "small"

        result_matrix = {
            "inside": {
                "big": RESULTS.soumis,
                "medium": RESULTS.action_requise,
                "small": RESULTS.non_soumis,
            },
            "outside": {
                "big": RESULTS.non_applicable,
                "medium": RESULTS.non_applicable,
                "small": RESULTS.non_soumis,
            },
        }

        result = result_matrix[flood_zone_status][project_size]
        return result


class WaterLaw2150(MoulinetteCriterion):
    slug = "ruissellement"
    title = "Imperméabilisation et captation du ruissellement des eaux de pluie"
    subtitle = "Seuil réglementaire : 1 ha"

    @cached_property
    def result(self):

        if self.catalog["project_surface"] >= 10000:
            res = RESULTS.soumis
        elif self.catalog["project_surface"] >= 8000:
            res = RESULTS.action_requise
        else:
            res = RESULTS.non_soumis

        return res


class WaterLaw(MoulinetteRegulation):
    slug = "loi_sur_leau"
    title = "Loi sur l'eau"
    criterion_classes = [WaterLaw3310, WaterLaw3220, WaterLaw2150]