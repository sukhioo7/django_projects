from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('<int:page>/',views.patient_home,name='patient_home_page'),
    path('delete/<str:id>',views.delete_patient,name='delete_patient'),
    path('update/<int:id>/',views.update_patient,name='update_patient'),
    path('search/',views.search,name='search'),
    path('filter/<slug:filter_by>/',views.filter_patient,name='filter'),
    path('signup/',views.signup_emp,name='signup'),
    path('login/',views.login_emp,name='login'),
    path('logout/',views.logout_emp,name='logout')

]