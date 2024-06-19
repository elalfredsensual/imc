# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


# for bq 
from google.cloud import bigquery
import os
from django.http import JsonResponse


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