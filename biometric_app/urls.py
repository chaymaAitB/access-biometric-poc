from django.urls import path
from .views import home, biometric_test

urlpatterns = [
    path('', home, name='home'),  # Page principale
    path('biometric_test/', biometric_test, name='biometric_test'),  # Page test biométrique
]