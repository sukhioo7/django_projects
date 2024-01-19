from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('',views.patient_home,name='patient_home_page'),
    path('delete/<str:id>',views.delete_patient,name='delete_patient'),
    # path('search/',views.searching,name='search_patient')
]