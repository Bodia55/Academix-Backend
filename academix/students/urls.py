from django.urls import path
from .views import StudentAPIView

urlpatterns = [
    path('courses', StudentAPIView.as_view({
    'post': 'courses',
    })),
    path('gpa', StudentAPIView.as_view({
    'post': 'gpa',
    }))
]
