import os
from typing import List, Dict, Union
from tronmap import TronMap

CZE_SVK_REGION: Dict[str, Dict[str, float]] = {
    "lat": {"min": 47.80819952020968, "max": 51.565655326824526},
    "lng": {"min": 6.462022610336817, "max": 27.555772610336817},
}

markers = [
    {"lat": 50.073658, "lon": 14.418540, "fill": "#d6ff79", "radius": 6},
    {"lat": 49.195061, "lon": 16.606836, "fill": "#00e5e8", "radius": 5},
]


# map = DottedMap(
#     filename=os.path.join("examples", "map.svg"),
#     width=1260,
#     height=600,
#     markers=markers,
#     radius=2,
#     step=10,
#     style="background-color:#020300",
# )

map_cze_svk = TronMap(
    filename=os.path.join("examples", "map_cze_svk.svg"),
    width=2000,
    height=600,
    markers=markers,
    radius=2,
    step=10,
    boundaries=CZE_SVK_REGION,
    countries=["CZE", "SVK"],
    style="background-color:#020300",
)
