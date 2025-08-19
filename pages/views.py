from django.shortcuts import render
from django.http import JsonResponse
import requests

def home(request):
    return render(request, "pages/home.html")

def getweather(request):
    api_key = "68c2f3daa8022e4825d3c575c4cbe8c6"

    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    city_name = request.GET.get("name")

    if lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    elif city_name:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}"
    else:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    try:
        res = requests.get(url)
        data = res.json()

        if res.status_code != 200:
            return JsonResponse({"error": data.get("message", "API Error")}, status=res.status_code)

        if "main" in data:
            data["main"]["temp"] = round(data["main"]["temp"])
            data["main"]["temp_max"] = round(data["main"]["temp_max"])
            data["main"]["temp_min"] = round(data["main"]["temp_min"])
            data["main"]["feels_like"] = round(data["main"]["feels_like"])

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)






