from rest_framework import generics, permissions
from helpers.auth import IsAuthenticated
from .models import City
from .serializers import CitySerializer
import json
from rest_framework.authentication import BasicAuthentication
from helpers.auth import SessionAuthAPIListView


class CityListView(SessionAuthAPIListView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]


class CitySearchView(SessionAuthAPIListView):
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.kwargs['search']

        # with open('assets/us_states.json') as f:
        #     states = json.load(f)
        #     for state in states:
        #         # laa = {
        #         #     "zip_code": "90005",
        #         #     "usps_city": "Los Angeles",
        #         #     "stusps_code": "CA",
        #         #     "ste_name": "California",
        #         #     "zcta": "TRUE",
        #         #     "parent_zcta": null,
        #         #     "population": 39732.0,
        #         #     "density": 14151.8,
        #         #     "primary_coty_code": "6037",
        #         #     "primary_coty_name": "Los Angeles",
        #         #     "county_weights": "{\"06037\": \"100\"}",
        #         #     "coty_name": ["Los Angeles"],
        #         #     "cty_code": ["6037"],
        #         #     "imprecise": "FALSE",
        #         #     "military": "FALSE",
        #         #     "timezone": "America/Los_Angeles",
        #         #     "geo_point_2d": {
        #         #         "lon": -118.30654,
        #         #         "lat": 34.05912
        #         #     }
        #         # },
        #         city, _ = City.objects.get_or_create(
        #             zip_code=state['zip_code'],
        #             city_name=state['usps_city'],
        #             state_code=state['stusps_code'],
        #             state_name=state['ste_name'],
        #             geo_point=str(state['geo_point_2d']['lon']) + ', ' + str(state['geo_point_2d']['lat'])
        #         )
        #         city.save()
        #         print(city.city_name)

        if query:
            queryset = City.search(query)
        else:
            queryset = City.objects.none()
        return queryset
