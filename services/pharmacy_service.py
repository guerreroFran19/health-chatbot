import requests
from geopy.distance import geodesic
import geocoder

def find_nearby_pharmacies(radius: int = 3000):
    """
    Buscar farmacias cercanas a la ubicación actual usando IP + Overpass API.
    Devuelve hasta 5 farmacias con dirección y distancia aproximada.
    """
    try:
        # 🔹 Obtener ubicación actual
        location = geocoder.ip('me')
        if not location.ok:
            return "No pude obtener tu ubicación actual."
        user_lat, user_lon = location.latlng

        # 🔹 Consulta Overpass API para farmacias
        overpass_url = "http://overpass-api.de/api/interpreter"
        query = f"""
        [out:json];
        node["amenity"="pharmacy"](around:{radius},{user_lat},{user_lon});
        out;
        """
        resp = requests.get(overpass_url, params={"data": query}).json()
        elements = resp.get("elements", [])

        if not elements:
            return "No encontré farmacias cerca de tu ubicación."

        # 🔹 Formatear resultados
        pharmacies = []
        for elem in elements[:5]:
            tags = elem.get("tags", {})
            name = tags.get("name", "Sin nombre")
            street = tags.get("addr:street", "")
            housenumber = tags.get("addr:housenumber", "")
            city = tags.get("addr:city", "")
            address = ", ".join(filter(None, [street, housenumber, city])) or "Dirección desconocida"

            lat = elem.get("lat")
            lon = elem.get("lon")
            distance = geodesic((user_lat, user_lon), (lat, lon)).meters
            distance_text = f"{int(distance)} metros"

            pharmacies.append(f"{name} - {address} ({distance_text})")

        return pharmacies

    except Exception:
        return "Ocurrió un error buscando farmacias. Intenta nuevamente más tarde."
