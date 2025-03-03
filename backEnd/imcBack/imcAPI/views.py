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
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        logging.info("File received: %s", file.name)

        try:
            # Save file to MEDIA_ROOT
            file_path = default_storage.save(os.path.join(settings.MEDIA_ROOT, file.name), file)
            absolute_file_path = Path(settings.MEDIA_ROOT) / file_path
            logging.info("File saved to: %s", absolute_file_path)

            # Define paths
            script_path = Path('/root/IMC/Proyecto IMC/Scripts/data_cleaner/quote_cleaning_script.py').resolve()
            logging.info("Script path: %s", script_path)

            # ✅ Use the virtual environment's Python interpreter directly
            venv_python = Path('/root/imc_project/imc-back-env/bin/python').resolve()
            logging.info("Python interpreter path: %s", venv_python)

            # ✅ Explicitly activate the virtual environment before running the script
            command = [
                str(venv_python),
                str(script_path),
                str(absolute_file_path)
            ]
            logging.info("Running command: %s", " ".join(command))

            # ✅ Ensure the script runs inside the virtual environment
            result = subprocess.run(
                command,
                env={
                    **os.environ,
                    "PATH": "/root/imc_project/imc-back-env/bin:" + os.environ["PATH"],
                    "VIRTUAL_ENV": "/root/imc_project/imc-back-env",
                },
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                logging.info("Script executed successfully: %s", result.stdout)
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