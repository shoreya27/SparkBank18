from django.urls import path

from . import views
from .CustomerRegisterationInterface import CustomerRegisteration
from .analytics import generate_report

urlpatterns = [
    #Register New User in Sparks18 Account
    path('register/', CustomerRegisteration.as_view()),
    path('enquiry/<str:phone>', views.enquiry),
    path('deposit/', views.deposit),
    path('withdraw/', views.withdraw),
    path('report/',generate_report)
]