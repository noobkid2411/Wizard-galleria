
from django.contrib import admin
from django.conf.urls import url

from .views import MagiciansView, Total_priceView, PingView, Magician_hire_costView

urlpatterns = [
    url('admin/', admin.site.urls),

    url('ping/', PingView.as_view()),

    # Endpoints for customers URL.
    url('Magicians/',MagiciansView.as_view(), name='magicians'),
    url('magician/<int:id>/',MagiciansView.as_view(), name='magicians'),

    # Endpoints for customers URL.
    url('Hire cost /',Magician_hire_costView.as_view(), name='hire cost'),
    url('Hire cost/<int:id>/',Magician_hire_costView.as_view(), name='hire cost'),

    url('Total Price/', Total_priceView.as_view(), name='total price'),
]
