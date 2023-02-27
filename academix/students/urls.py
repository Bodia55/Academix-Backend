from django.urls import path
from .views import StudentAPIView

urlpatterns = [
    path('schedule/', StudentAPIView.as_view({
    'post': 'schedule',
    }))
]
