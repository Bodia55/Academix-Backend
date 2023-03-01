from django.http import HttpRequest
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .scrapper import Scrapper

class StudentAPIView(ViewSet):
    def courses(self, request):
        if request.method == 'POST':
            username = request.data["username"]
            password = request.data["password"]
            scrapper = Scrapper(username, password)
            courses, success = scrapper.get_courses_data()
            return Response({'courses': courses, 'success': success})
    def gpa(self, request):
        if request.method == 'POST':
            username = request.data["username"]
            password = request.data["password"]
            scrapper = Scrapper(username, password)
            gpa, success = scrapper.get_gpa('2022-2023')
            return Response({'gpa': gpa, 'success':success})

