from django.urls import path
from . import views
from .views import flm_dashboard_view
from .views import engineer_dashboard_view
from .views import get_fault_calls

urlpatterns = [
    path('call/', views.call_engineer_view, name='call_engineer'),
    path('call/success/', views.call_success_view, name='call_success'),
    path('dashboard/flm/', flm_dashboard_view, name='flm_dashboard'),
    path('dashboard/engineer/', engineer_dashboard_view, name='engineer_dashboard'),
    path('poll_calls/', get_fault_calls, name='poll_calls'),
    path('engineer/calls-json/', views.engineer_calls_json, name='engineer_calls_json'),
    path('engineer/action/', views.engineer_action_api, name='engineer_action_api'),
    path('engineer/calls/update/', views.update_call_status, name='update_call_status'),
]
