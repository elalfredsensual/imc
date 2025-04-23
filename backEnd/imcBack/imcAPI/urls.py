from django.http import JsonResponse
from django.urls import path
from . import views

def home_view(request):
    return JsonResponse({"message": "Welcome to the API!"})

urlpatterns = [
    path('', home_view, name='home'),  # This ensures `/` works
    path('hello-world/', views.hello_world, name='hello_world'),
    path('get-bigquery-table/', views.get_bigquery_table, name='get_bigquery_table'),
    path('login/', views.login_user, name='login_user'),
    path('upload-quote/', views.upload_quote_file, name='upload_quote_file'),
    path('upload-partner/', views.upload_partner_file, name='upload_partner_file'),
    path('upload-facturas/', views.upload_facturas_file, name='upload_facturas_file'),  # <--- NUEVA RUTA
    path('get-last-10-quotes/', views.get_last_10_quotes, name='get_last_10_quotes'),
    path('get-last-10-partners/', views.get_last_10_partners, name='get_last_10_partners'),
    path('rebates/', views.get_rebates_from_bigquery, name='get_rebates'),
    path('rebates/update/', views.upsert_rebate_in_bigquery, name='upsert_rebate'),
    path('rebates/delete/', views.delete_rebate_in_bigquery, name='delete_rebate'),
    path('get-last-10-facturas/', views.get_last_10_facturas, name='get_last_10_facturas'),


    # Default route for the homepage
    path('', views.hello_world, name='home'),  # This ensures root `/` works
]
