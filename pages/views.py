from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests

def home(request):
    return render(request, "pages/home.html")

def getweather(request):
    # ✅ Use env var if available, else fallback to your old hardcoded key
    api_key = settings.OPENWEATHER_API_KEY or "68c2f3daa8022e4825d3c575c4cbe8c6"

    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    city_name = request.GET.get("name")

    if not api_key:
        return JsonResponse({"error": "API key not configured"}, status=500)

    if lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    elif city_name:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}"
    else:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    try:
        res = requests.get(url, timeout=8)
        data = res.json()

        if res.status_code != 200:
            return JsonResponse({"error": data.get("message", "API Error")}, status=res.status_code)

        if "main" in data:
            for key in ["temp", "temp_max", "temp_min", "feels_like"]:
                if key in data["main"]:
                    data["main"][key] = round(data["main"][key])

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)





