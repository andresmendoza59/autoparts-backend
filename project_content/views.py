from django.views.generic import ListView
from django.views import View
from django.shortcuts import render, redirect
from .models import *
import googlemaps
from django.conf import settings
from .forms import *
from datetime import datetime
from django.http import JsonResponse
import json

# Create your views here.
class HomeView(ListView):
    template_name = "project_content/home.html"
    context_object_name = 'mydata'
    model = Locations
    success_url = "/"

class MapView(View):
    template_name = "project_content/map.html"

    def get(self,request): 
        key = settings.GOOGLE_API_KEY
        eligable_locations = Locations.objects.filter(place_id__isnull=False)
        locations = []

        for a in eligable_locations: 
            data = {
                'lat': float(a.lat), 
                'lng': float(a.lng), 
                'name': a.name,
                'address': f"{a.adress}, {a.zipcode}, {a.city}, {a.country}",
                'hours': a.hours if hasattr(a, 'hours') else '9:00 - 18:00'
            }

            locations.append(data)


        context = {
            "key":key, 
            "locations": json.dumps(locations)
        }

        return render(request, self.template_name, context)

class CalculateDistanceView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_lat = data.get('user_lat')
            user_lng = data.get('user_lng')
            workshop_lat = data.get('workshop_lat')
            workshop_lng = data.get('workshop_lng')
            
            if not all([user_lat, user_lng, workshop_lat, workshop_lng]):
                return JsonResponse({'error': 'Missing coordinates'}, status=400)

            gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
            now = datetime.now()
            
            # Calcular distancia y tiempo
            result = gmaps.distance_matrix(
                origins=(user_lat, user_lng),
                destinations=(workshop_lat, workshop_lng),
                mode="driving",
                departure_time=now
            )

            if result['rows'][0]['elements'][0]['status'] != 'OK':
                return JsonResponse({'error': 'Could not calculate distance'}, status=400)

            distance_km = result['rows'][0]['elements'][0]['distance']['value'] / 1000
            duration_mins = result['rows'][0]['elements'][0]['duration']['value'] / 60
            
            # Redondear valores
            distance_km = round(distance_km, 1)
            duration_mins = round(duration_mins)
            
            return JsonResponse({
                'distance': f"{distance_km} km",
                'duration': f"{duration_mins} min"
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class DistanceView(View):
    template_name = "project_content/distance.html"

    def get(self, request):
        form = DistanceForm
        distances = Distances.objects.all()
        context = {
            'form': form,
            'distances': distances,
        }

        return render(request, self.template_name, context)
    
    def post(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            from_location_info = Locations.objects.get(name=from_location)
            from_adress_string = str(from_location_info.adress)+", "+str(from_location_info.zipcode)+", "+str(from_location_info.city)+", "+str(from_location_info.country)

            to_location = form.cleaned_data['to_location']
            to_location_info = Locations.objects.get(name=to_location)
            to_adress_string = str(to_location_info.adress)+", "+str(to_location_info.zipcode)+", "+str(to_location_info.city)+", "+str(to_location_info.country)

            mode = form.cleaned_data['mode']
            now = datetime.now()

            gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
            calculate = gmaps.distance_matrix(
                    from_adress_string,
                    to_adress_string,
                    mode = mode,
                    departure_time = now
            )


            duration_seconds = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_seconds/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_kilometers = distance_meters/1000

            if 'duration_in_traffic' in calculate['rows'][0]['elements'][0]: 
                duration_in_traffic_seconds = calculate['rows'][0]['elements'][0]['duration_in_traffic']['value']
                duration_in_traffic_minutes = duration_in_traffic_seconds/60
            else: 
                duration_in_traffic_minutes = None

            
            obj = Distances(
                from_location = Locations.objects.get(name=from_location),
                to_location = Locations.objects.get(name=to_location),
                mode = mode,
                distance_km = distance_kilometers,
                duration_mins = duration_minutes,
                duration_traffic_mins = duration_in_traffic_minutes
            )

            obj.save()
        else:
            print(form.errors)

        return redirect('my_distance_view')

class GeocodingView(View):
    template_name = "project_content/geocoding.html"

    def get(self, request, pk):
        location = Locations.objects.get(pk = pk)

        if location.lng and location.lat and location.place_id != None:
            lat = location.lat
            lng = location.lng
            place_id = location.place_id
            label = "from my database"

        elif location.adress and location.country and location.zipcode and location.city != None:
            adress_string = str(location.adress)+", "+str(location.zipcode)+", "+ str(location.city)+","+ str(location.country)

            gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
            result = gmaps.geocode(adress_string)[0]

            lat = result.get('geometry', {}).get('location', {}).get('lat', None)
            lng = result.get('geometry', {}).get('location', {}).get('lng', None)
            place_id = result.get('place_id', {})
            label = "from my api call"

            location.lat = lat
            location.lng = lng
            location.place_id = place_id
            location.save()


        else:
            result = ""
            lat = ""
            lng = ""
            place_id = ""
            label = "no call made"

        context = {
            'location': location,
            'lat': lat,
            'lng': lng,
            'place_id': place_id,
            'label': label,
        }
        return render(request, self.template_name, context)
    