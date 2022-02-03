import glob
import zipfile
from tempfile import TemporaryDirectory

from django.contrib.gis.utils.layermapping import LayerMapping

from envergo.geodata.models import Zone


class CustomMapping(LayerMapping):
    def __init__(self, *args, **kwargs):
        self.extra_kwargs = kwargs.pop("extra_kwargs")
        super().__init__(*args, **kwargs)

    def feature_kwargs(self, feat):
        kwargs = super().feature_kwargs(feat)
        kwargs.update(self.extra_kwargs)
        return kwargs


def extract_shapefile(map, file):

    with TemporaryDirectory() as tmpdir:
        zf = zipfile.ZipFile(file)
        zf.extractall(tmpdir)

        paths = glob.glob(f"{tmpdir}/*shp")  # glop glop !
        shapefile = paths[0]

        mapping = {"geometry": "POLYGON"}
        extra = {"map": map}
        lm = CustomMapping(Zone, shapefile, mapping, extra_kwargs=extra)
        lm.save()
