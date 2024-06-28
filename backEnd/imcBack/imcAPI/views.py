from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# for BigQuery
from google.cloud import bigquery
import os
from django.http import JsonResponse, HttpResponseBadRequest

# for login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
import json
import bcrypt

# for file upload
from django.conf import settings
from django.core.files.storage import default_storage
import subprocess
from pathlib import Path

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


@csrf_exempt
def upload_quote_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_path = default_storage.save(os.path.join(settings.MEDIA_ROOT, file.name), file)
        absolute_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        absolute_file_path = Path(absolute_file_path).resolve()

        script_path = (Path(settings.BASE_DIR) / '../../../Scripts/data_cleaner/quote_cleaning_script.py').resolve()
        venv_python = Path(settings.BASE_DIR) / 'imc-back-env' / 'Scripts' / 'python.exe'
        venv_python = venv_python.resolve()

        result = subprocess.run([str(venv_python), str(script_path), str(absolute_file_path)], capture_output=True, text=True)

        if result.returncode == 0:
            return JsonResponse({'status': 'success', 'message': 'File uploaded and processed successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': result.stderr})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@csrf_exempt
def upload_partner_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_path = default_storage.save(os.path.join(settings.MEDIA_ROOT, file.name), file)
        absolute_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        absolute_file_path = Path(absolute_file_path).resolve()

        script_path = (Path(settings.BASE_DIR) / '../../../Scripts/data_cleaner/partner_cleaning_script.py').resolve()
        venv_python = Path(settings.BASE_DIR) / 'imc-back-env' / 'Scripts' / 'python.exe'
        venv_python = venv_python.resolve()

        result = subprocess.run([str(venv_python), str(script_path), str(absolute_file_path)], capture_output=True, text=True)

        if result.returncode == 0:
            return JsonResponse({'status': 'success', 'message': 'File uploaded and processed successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': result.stderr})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def get_last_10_quotes(request):
    client = bigquery.Client()

    query = """
    SELECT *
    FROM `imc-storage.imcData.valores_mes`
    ORDER BY Num DESC
    LIMIT 10
    """
    query_job = client.query(query)

    results = query_job.result()

    rows = [dict(row) for row in results]

    return JsonResponse(rows, safe=False)


@api_view(['GET'])
def get_last_10_partners(request):
    client = bigquery.Client()

    query = """
    SELECT IMC_PO, PARTNER_PO, MONTO_PARTNER_PO
    FROM `imc-storage.imcData.orders`
    ORDER BY IMC_PO DESC
    LIMIT 10
    """
    query_job = client.query(query)

    results = query_job.result()  # Wait for the job to complete

    # Convert results to a list of dictionaries
    rows = [dict(row) for row in results]

    return JsonResponse(rows, safe=False)
