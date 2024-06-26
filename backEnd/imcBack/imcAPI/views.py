# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# for bq 
from google.cloud import bigquery
import os
from django.http import JsonResponse, HttpResponseBadRequest

# for login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
import json
import bcrypt



@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, worldito!'})

def get_bigquery_table(request):
    client = bigquery.Client()

    query = """
    SELECT *
    FROM `imc-storage.imcData.orders`
    LIMIT 10
    """
    query_job = client.query(query)

    results = query_job.result()  # Wait for the job to complete

    # Convert results to a list of dictionaries
    rows = [dict(row) for row in results]

    return JsonResponse(rows, safe=False)

@csrf_exempt
def login_user(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method")

    try:
        body = json.loads(request.body)
        email = body.get('email')
        password = body.get('password')

        if not email or not password:
            return HttpResponseBadRequest("Missing 'email' or 'password'")

        client = bigquery.Client()

        query = """
        SELECT email, password, userType
        FROM `imc-storage.imcData.credentials`
        WHERE email = @username
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("username", "STRING", email)
            ]
        )
        query_job = client.query(query, job_config=job_config)

        results = query_job.result()
        user_data = None

        for row in results:
            user_data = row
            break

        if user_data and password == user_data['password']:
            try:
                user = User.objects.get(username=email)
            except User.DoesNotExist:
                user = User.objects.create_user(username=email, email=email, password=password)

            login(request, user)
            return JsonResponse({"status": "success", "userType": user_data['userType']})
        else:
            return JsonResponse({"status": "failure"}, status=401)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
