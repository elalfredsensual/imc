from django.urls import path
from . import views

urlpatterns = [
    path('hello-world/', views.hello_world, name='hello_world'),
    path('get-bigquery-table/', views.get_bigquery_table, name='get_bigquery_table'),
    path('login/', views.login_user, name='login_user'),
    path('upload-quote/', views.upload_quote_file, name='upload_quote_file'),
]
