from typing import Dict
import numpy as np

EARTH_RADIUS_KM = 6371.0

def haversine_to_many(query_coordinate: Dict[str, float], listing_coordinates: np.recarray) -> np.ndarray:
    """
    Vectorized haversine from one query point to many listing points.

    Parameters:
    ---
    query_coordinate : mapping/record with fields "lat", "lon"
    listing_coordinates : NumPy structured/recarray with fields "id",'lat", "lon"

    Returns
    ---
    np.ndarray structured dtype [("id", listing_id_dtype), ("dist_km", float64)]
    """
    lat_query = np.deg2rad(np.asarray(query_coordinate["lat"], dtype=float))
    lon_query = np.deg2rad(np.asarray(query_coordinate["lon"], dtype=float))
    lat_listings = np.deg2rad(np.asarray(listing_coordinates["lat"], dtype=float))
    lon_listings = np.deg2rad(np.asarray(listing_coordinates["lon"], dtype=float))
    dlat = lat_listings - lat_query
    dlon = lon_listings - lon_query

    # haversine
    a = np.sin(dlat/2.0)**2 + np.cos(lat_query) * np.cos(lat_listings) * np.sin(dlon/2.0)**2
    c = 2.0 * np.arcsin(np.sqrt(a))
    dist = EARTH_RADIUS_KM * c

    out_dtype = np.dtype([("id", listing_coordinates["id"].dtype), ("dist_km", "f8")])
    out = np.empty(dist.shape[0], dtype=out_dtype)
    out["id"] = listing_coordinates["id"]
    out["dist_km"] = dist
    
    return out
