from django.urls import path
from . import views
from .views import XRayListView, XRayUpdateView

urlpatterns = [
    path('', XRayListView.as_view(), name='xraylab-home'),
    path('about/', views.about, name='xraylab-about'),
    path('details_update/<int:pk>/', XRayUpdateView.as_view(), name='xraylab-details-update'),
]
