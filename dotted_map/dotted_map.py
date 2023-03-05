import json
import os
from svgwrite import Drawing
from shapely.geometry import Point, Polygon, MultiPolygon
from typing import List, Dict, Union


class DottedMap:
    def __init__(
        self,
        geojson: str = os.path.join("dotted_map", "countries.geo.json"),
        filename: str = "map.svg",
        width: int = 600,
        height: int = 600,
        radius: int = 2,
        step: int = 10,
        fill: str = "#423b38",
        style: str = None,
        markers: List[Dict[str, Union[float, int, str]]] = None,
        countries: List[str] = None,
        boundaries: Dict[str, Dict[str, Union[int, float]]] = None,
    ) -> None:
        self.geojson = geojson
        self.filename = filename
        self.width = width
        self.height = height
        self.radius = radius
        self.step = step
        self.fill = fill
        self.style = style
        self.markers = markers or []
        self.dwg = Drawing(
            self.filename,
            size=(self.width, self.height),
            style=self.style,
        )
        self.countries = countries or []
        self.boundaries = boundaries or {
            "lat": {"min": -56, "max": 71},
            "lng": {"min": -179, "max": 179},
        }

        self.load_data()
        self.render_points()
        self.dwg.save()

    def get_x(self, lon: float) -> float:
        return (
            (lon - self.boundaries["lng"]["min"])
            * self.width
            / (self.boundaries["lng"]["max"] - self.boundaries["lng"]["min"])
        )

    def get_y(self, lat: float) -> float:
        return (
            (self.boundaries["lat"]["max"] - lat)
            * self.height
            / (self.boundaries["lat"]["max"] - self.boundaries["lat"]["min"])
        )

    def get_lat(self, y: float) -> float:
        return (
            self.boundaries["lat"]["max"]
            - y
            * (self.boundaries["lat"]["max"] - self.boundaries["lat"]["min"])
            / self.height
        )

    def get_lon(self, x: float) -> float:
        return (
            self.boundaries["lng"]["min"]
            + x
            * (self.boundaries["lng"]["max"] - self.boundaries["lng"]["min"])
            / self.width
        )

    def render_points(self) -> None:

        for feature in self.data["features"]:

            if self.countries and feature["id"] not in self.countries:
                continue

            if feature["geometry"]["type"] == "Polygon":
                polygon = Polygon(feature["geometry"]["coordinates"][0])
            elif feature["geometry"]["type"] == "MultiPolygon":
                polygon = MultiPolygon(
                    [
                        Polygon(_coords[0])
                        for _coords in feature["geometry"]["coordinates"]
                    ]
                )

            dots_group = self.dwg.add(self.dwg.g())

            dots = [
                (x, y)
                for x in range(0, self.width, self.step)
                for y in range(0, self.height, self.step)
            ]

            for x, y in dots:
                lon = self.get_lon(x)
                lat = self.get_lat(y)

                if polygon.contains(Point(lon, lat)):
                    dots_group.add(
                        self.dwg.circle(
                            center=(self.get_x(lon), self.get_y(lat)),
                            r=self.radius,
                            fill=self.fill,
                        )
                    )

        for _marker in self.markers:
            dots_group.add(self.get_marker(**_marker))

    def load_data(self):
        with open(self.geojson, "r") as f:
            self.data = json.load(f)

    def get_marker(self, lat, lon, radius, fill="#00E5E8"):
        return self.dwg.circle(
            center=(self.get_x(lon), self.get_y(lat)),
            r=radius or self.radius,
            fill=fill,
        )
