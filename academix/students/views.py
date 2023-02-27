from django.http import HttpRequest
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .scrapper import Scrapper

class StudentAPIView(ViewSet):
    def schedule(self, request):
        if request.method == 'POST':
            username = request.data["username"]
            password = request.data["password"]
            scrapper = Scrapper(username, password)
            courses, response_code = scrapper.get_courses_data()
            return Response({'schedule': courses, 'success': response_code})

