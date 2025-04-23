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
import pandas as pd

import shlex

#for rebates model
from .models import Rebate
from rest_framework.decorators import api_view
from rest_framework import status



# Configure logging
import logging
logging.basicConfig(level=logging.INFO)

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
    log_file = Path(settings.BASE_DIR) / "upload_debug.log"

    with open(log_file, "a") as log:
        log.write("\n===== File Upload Attempt =====\n")
        log.write("Received request for file upload\n")

        if request.method == 'POST' and request.FILES.get('file'):
            log.write("File received\n")
            file = request.FILES['file']
            
            # Ensure MEDIA_ROOT exists
            media_path = Path(settings.MEDIA_ROOT)
            media_path.mkdir(parents=True, exist_ok=True)

            # Save file correctly
            absolute_file_path = media_path / file.name
            default_storage.save(str(absolute_file_path), file)
            absolute_file_path = absolute_file_path.resolve()

            log.write(f"File saved at {absolute_file_path}\n")

            # Set script path
            script_path = Path(r'C:\Users\alfre\OneDrive\Documents\Trabajo\IMC\Proyecto IMC\Scripts\data_cleaner\quote_cleaning_script.py').resolve()
            log.write(f"Script path is set to: {script_path}\n")

            # Get virtual environment's Python
            venv_path = Path(r'C:\Users\alfre\OneDrive\Documents\Trabajo\IMC\Proyecto IMC\Web App\imc\backEnd\imcBack\imc-back-env').resolve()
            venv_python = venv_path / "bin/python"
            log.write(f"Using Python interpreter at: {venv_python}\n")

            # Check if paths exist before executing
            if not script_path.exists():
                log.write(f"ERROR: Script not found at {script_path}\n")
                return JsonResponse({'status': 'error', 'message': f"Script not found: {script_path}"})

            if not venv_python.exists():
                log.write(f"ERROR: Python interpreter not found at {venv_python}\n")
                return JsonResponse({'status': 'error', 'message': f"Python interpreter not found: {venv_python}"})

            # Run script and capture logs
            command = f"source \"{venv_path}/bin/activate\" && \"{venv_python}\" \"{script_path}\" \"{absolute_file_path}\""
            log.write(f"Running command: {command}\n")

            result = subprocess.run(
                command, capture_output=True, text=True, shell=True, executable="/bin/bash"
            )

            log.write(f"Subprocess return code: {result.returncode}\n")
            log.write(f"Subprocess stdout: {result.stdout}\n")
            log.write(f"Subprocess stderr: {result.stderr}\n")

            if result.returncode == 0:
                return JsonResponse({'status': 'success', 'message': 'File uploaded and processed successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': result.stderr})

        log.write("Invalid request\n")
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


#  Configure logging
logging.basicConfig(level=logging.INFO)

@csrf_exempt
def upload_partner_file(request):
    log_file = Path(settings.BASE_DIR) / "partner_upload_debug.log"

    with open(log_file, "a") as log:
        log.write("\n===== Partner File Upload Attempt =====\n")
        log.write("Received request for file upload\n")

        if request.method == 'POST' and request.FILES.get('file'):
            log.write("File received\n")
            file = request.FILES['file']

            # Ensure MEDIA_ROOT exists
            media_path = Path(settings.MEDIA_ROOT)
            media_path.mkdir(parents=True, exist_ok=True)

            # Save file correctly
            absolute_file_path = media_path / file.name
            default_storage.save(str(absolute_file_path), file)
            absolute_file_path = absolute_file_path.resolve()

            log.write(f"File saved at {absolute_file_path}\n")

            # Set script path
            script_path = Path("/root/IMC/Proyecto IMC/Scripts/data_cleaner/partner_cleaning_script.py").resolve()
            log.write(f"Script path is set to: {script_path}\n")

            # Get virtual environment's Python
            venv_path = Path("/root/IMC/Proyecto IMC/Web App/imc/backEnd/imcBack/imc-back-env").resolve()
            venv_python = venv_path / "bin/python"
            log.write(f"Using Python interpreter at: {venv_python}\n")

            # Check if paths exist before executing
            if not script_path.exists():
                log.write(f"ERROR: Script not found at {script_path}\n")
                return JsonResponse({'status': 'error', 'message': f"Script not found: {script_path}"})

            if not venv_python.exists():
                log.write(f"ERROR: Python interpreter not found at {venv_python}\n")
                return JsonResponse({'status': 'error', 'message': f"Python interpreter not found: {venv_python}"})

            # Run script and capture logs
            command = f"source \"{venv_path}/bin/activate\" && \"{venv_python}\" \"{script_path}\" \"{absolute_file_path}\""
            log.write(f"Running command: {command}\n")

            result = subprocess.run(
                command, capture_output=True, text=True, shell=True, executable="/bin/bash"
            )

            log.write(f"Subprocess return code: {result.returncode}\n")
            log.write(f"Subprocess stdout: {result.stdout}\n")
            log.write(f"Subprocess stderr: {result.stderr}\n")

            if result.returncode == 0:
                return JsonResponse({'status': 'success', 'message': 'File uploaded and processed successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': result.stderr})

        log.write("Invalid request\n")
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



## rebates GET/POST
@api_view(['GET'])
def get_rebates_from_bigquery(request):
    client = bigquery.Client()

    query = """
        SELECT fiscal_year, quarter, amount
        FROM `imc-storage.imcData.rebates`
        ORDER BY fiscal_year DESC, quarter
    """
    query_job = client.query(query)
    results = query_job.result()
    rows = [dict(row) for row in results]

    return JsonResponse(rows, safe=False)


@csrf_exempt
@api_view(['POST'])
def upsert_rebate_in_bigquery(request):
    try:
        data = json.loads(request.body)
        fiscal_year = data.get("fiscal_year")
        quarter = data.get("quarter")
        amount = data.get("amount")

        client = bigquery.Client()

        query = f"""
        MERGE `imc-storage.imcData.rebates` T
        USING (SELECT '{fiscal_year}' AS fiscal_year, '{quarter}' AS quarter, {amount} AS amount) S
        ON T.fiscal_year = S.fiscal_year AND T.quarter = S.quarter
        WHEN MATCHED THEN UPDATE SET amount = S.amount
        WHEN NOT MATCHED THEN INSERT (fiscal_year, quarter, amount) VALUES (S.fiscal_year, S.quarter, S.amount)
        """
        query_job = client.query(query)
        query_job.result()

        return JsonResponse({"status": "success"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@api_view(['POST'])
def delete_rebate_in_bigquery(request):
    try:
        data = json.loads(request.body)
        fiscal_year = data.get("fiscal_year")
        quarter = data.get("quarter")

        if not fiscal_year or not quarter:
            return JsonResponse({"error": "Missing fiscal_year or quarter"}, status=400)

        client = bigquery.Client()

        query = f"""
        DELETE FROM `imc-storage.imcData.rebates`
        WHERE fiscal_year = '{fiscal_year}' AND quarter = '{quarter}'
        """
        query_job = client.query(query)
        query_job.result()

        return JsonResponse({"status": "deleted"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
