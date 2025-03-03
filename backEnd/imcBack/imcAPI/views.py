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
            
            # Save file
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            absolute_file_path = default_storage.save(file_path, file)
            absolute_file_path = Path(absolute_file_path).resolve()
            log.write(f"File saved at {absolute_file_path}\n")

            # Set script path
            script_path = Path("/root/IMC/Proyecto IMC/Scripts/data_cleaner/quote_cleaning_script.py").resolve()
            script_path = script_path.resolve()
            log.write(f"Script path is set to: {script_path}\n")

            # Get virtual environment's Python
            venv_python = Path("/root/IMC/Proyecto IMC/Web App/imc/backEnd/imcBack/imc-back-env/bin/python").resolve()
            venv_python = venv_python.resolve()
            log.write(f"Using Python interpreter at: {venv_python}\n")

            # Check existence before executing
            if not script_path.exists():
                log.write(f"Error: Script not found at {script_path}\n")
                return JsonResponse({'status': 'error', 'message': f"Script not found: {script_path}"})

            if not venv_python.exists():
                log.write(f"Error: Python interpreter not found at {venv_python}\n")
                return JsonResponse({'status': 'error', 'message': f"Python interpreter not found: {venv_python}"})

            # Run script and capture logs
            # Corrected subprocess call to activate the virtual environment
            venv_path = "/root/IMC/Proyecto IMC/Web App/imc/backEnd/imcBack/imc-back-env"
            result = subprocess.run(
                f"source {venv_path}/bin/activate && python {script_path} {absolute_file_path}",
                capture_output=True, text=True, shell=True, executable="/bin/bash"
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
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        import sys

        logging.info(f"Django is running with Python: {sys.executable}")

        logging.info("File received: %s", file.name)
        
        try:
            file_path = default_storage.save(os.path.join(settings.MEDIA_ROOT, file.name), file)
            absolute_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            absolute_file_path = Path(absolute_file_path).resolve()
            logging.info("File saved to: %s", absolute_file_path)

            # Correct the script path based on the actual structure
            script_path = Path('/root/IMC/Proyecto IMC/Scripts/data_cleaner/partner_cleaning_script.py')
            logging.info("Script path: %s", script_path)
            venv_python = Path('/root/IMC/Proyecto IMC/Web App/imc/backEnd/imcBack/imc-back-env/bin/python3')
            venv_python = venv_python.resolve()
            logging.info("Python interpreter path: %s", venv_python)

            logging.info("Running script: %s with Python interpreter: %s", script_path, venv_python)
            result = subprocess.run([str(venv_python), str(script_path), str(absolute_file_path)], capture_output=True, text=True)

            if result.returncode == 0:
                logging.info("Script executed successfully")
                return JsonResponse({'status': 'success', 'message': 'File uploaded and processed successfully'})
            else:
                logging.error("Script execution failed: %s", result.stderr)
                return JsonResponse({'status': 'error', 'message': result.stderr})
        except Exception as e:
            logging.error("Exception occurred: %s", str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        logging.error("Invalid request: method=%s, files=%s", request.method, request.FILES)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


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