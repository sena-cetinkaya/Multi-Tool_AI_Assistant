import httpx
from langchain_core.tools import tool

from src.core.logger import get_logger

logger = get_logger(__name__)

_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

_WEATHER_CODES = {
    0: "Açık", 1: "Az bulutlu", 2: "Parçalı bulutlu", 3: "Kapalı",
    45: "Sisli", 48: "Kırağı sisi",
    51: "Hafif çisenti", 53: "Çisenti", 55: "Yoğun çisenti",
    61: "Hafif yağmur", 63: "Yağmur", 65: "Kuvvetli yağmur",
    71: "Hafif kar", 73: "Kar", 75: "Yoğun kar",
    80: "Sağanak sağanak", 81: "Kuvvetli sağanak", 82: "Şiddetli sağanak",
    95: "Gök gürültülü fırtına",
}

@tool("weather")
def weather(city: str) -> str:
    """
    Belirtilen şehir için GÜNCEL, GERÇEK ZAMANLI hava durumu verisini
    (sıcaklık, hissedilen sıcaklık, nem, rüzgar, hava durumu tipi) getirir.
    Hava durumuyla ilgili her soruda web_search yerine bu tool tercih edilmeli.

    Args:
        city: Şehir adı, örn. "Ankara", "İstanbul", "İzmir".

    Returns:
        Güncel hava durumu bilgisini içeren kısa bir metin.
    """
    try:
        with httpx.Client(timeout=8.0) as client:
            geo_resp = client.get(
                _GEOCODE_URL,
                params={"name": city, "count": 1, "language": "tr"},
            )
            geo_resp.raise_for_status()
            geo_data = geo_resp.json()

            results = geo_data.get("results")
            if not results:
                return f"'{city}' için konum bulunamadı."

            location = results[0]
            lat, lon = location["latitude"], location["longitude"]
            resolved_name = location.get("name", city)

            forecast_resp = client.get(
                _FORECAST_URL,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,"
                    "apparent_temperature,wind_speed_10m,weather_code",
                    "timezone": "auto",
                },
            )
            forecast_resp.raise_for_status()
            current = forecast_resp.json().get("current", {})

        code = current.get("weather_code")
        condition = _WEATHER_CODES.get(code, "Bilinmiyor")

        logger.info(f"Hava durumu alındı: {resolved_name}")

        return (
            f"{resolved_name} için güncel hava durumu:\n"
            f"- Durum: {condition}\n"
            f"- Sıcaklık: {current.get('temperature_2m')}°C\n"
            f"- Hissedilen: {current.get('apparent_temperature')}°C\n"
            f"- Nem: %{current.get('relative_humidity_2m')}\n"
            f"- Rüzgar: {current.get('wind_speed_10m')} km/s"
        )

    except Exception as exc:  # noqa: BLE001
        logger.error(f"Hava durumu alınamadı: {exc}")
        return f"Hava durumu servisi şu anda erişilemez durumda ({exc})."