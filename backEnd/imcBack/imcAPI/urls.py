from django.urls import path
from . import views

urlpatterns = [
    path('hello-world/', views.hello_world, name='hello_world'),
    path('get-bigquery-table/', views.get_bigquery_table, name='get_bigquery_table'),
    path('login/', views.login_user, name='login_user'),
    path('upload-quote/', views.upload_quote_file, name='upload_quote_file'),
    path('upload-partner/', views.upload_partner_file, name='upload_partner_file'),  # Add this line
    path('get-last-10-quotes/', views.get_last_10_quotes, name='get_last_10_quotes'),
    path('get-last-10-partners/', views.get_last_10_partners, name='get_last_10_partners'),

]
