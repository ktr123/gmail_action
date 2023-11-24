from rest_framework.views import APIView
from django.http import JsonResponse
import json

class Rules(APIView):

    def get(self, request):
        with open("emails/rules.json", 'r') as json_file:
            rules_data = json.load(json_file)
        return JsonResponse(rules_data, safe=False)
