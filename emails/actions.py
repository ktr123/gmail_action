from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Q
from emails.models import emails_data
from loguru import logger
import json
import datetime
import os
with open("emails/rules.json", 'r') as json_file:
    rules_data = json.load(json_file)

def custom_decorator(func):
    def inner(self, request):
        if request.data.get('condition', "") not in rules_data["rules"]["rules_to_satisfy"]:
            return JsonResponse({"statusCode": 500,
                                 "msg": "Please check the rules to be implemented"}, safe=False)
        response = func(self, request)
        return JsonResponse(response, safe=False)
    return inner

class Actions(APIView):

    def perform_action(self, msg_ids, action: str= "UNREAD"):
        SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json')
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        service = build('gmail', 'v1', credentials=creds)
        for msg_id in msg_ids:
            service.users().messages().modify(userId='me',
                                              id=msg_id,
                                              body={'removeLabelIds': [action]}).execute()
 

    def get_filtered_messages(self, request):
        """
        Used for filtering messages
        """
        filters = Q()
        q_objects = []
        rules = request.data.get("rules", [])
        condition = request.data.get("condition", "Any")
        for rule in rules:
            if rule["predicate"] == "Contains":
                q_objects.append(Q(**{f"{rule['field']}__icontains": rule["value"]}))
            elif rule["predicate"] == "Does not Contains":
                q_objects.append(~Q(**{f"{rule['field']}__icontains": rule["value"]}))
            elif rule["predicate"] == "Equals":
                q_objects.append(Q(**{f"{rule['field']}": rule["value"]}))
            elif rule["predicate"] == "Does Not Equals":
               q_objects.append(~Q(**{f"{rule['field']}": rule["value"]}))
            elif rule["predicate"] == "less_than_days":
                date_threshold = datetime.datetime.now() - datetime.timedelta(days=rule["value"])
                q_objects.append(Q(**{f"{rule['field']}__lt": date_threshold}))
        for q_object in q_objects:
            if condition == "Any":
                filters |= q_object
            else:
                filters &= q_object
        data = [msg["message_id"] for msg in list(emails_data.objects.filter(filters).all().values('message_id'))]
        return data
 
    @custom_decorator
    def post(self, request):
        """
        Used for performing actions based on the rules provided and accepts body in the below format
        {
            "rules": [
              {
                "field": "From",
                "predicate": "Contains",
                "value": "example.com"
              },
              {
                "field": "Subject",
                "predicate": "does not contain",
                "value": "spam"
              },
              {
                "field": "Received Date/Time",
                "predicate": "less than",
                "value": "2023-01-01"
              }
            ],
            "condition": "all",  
            "action": "mark_as_read"}
        """
        msg_ids = self.get_filtered_messages(request)
        try:
            self.perform_action(msg_ids)
            return {"statusCode": 200,
                    "msg": f"Action Performed Succesfully for the below msgIds: {msg_ids}"}
        except Exception as e:
            logger.error(f"Error : {e} while performing action...!!")
            return {"statusCode": 500,
                    "msg": f"{e}"}
        

        
