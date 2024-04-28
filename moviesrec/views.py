from django.http import JsonResponse
from rest_framework.views import APIView
from aima3.logic import *
from rest_framework.response import Response
# Create your views here.
from .InferenceSystem import *
class MovieRec(APIView):

    def post(self, request, *args, **kwargs):

        #send the data in json format like this
        # data={
        #"language":value,
        #"type": value,
        #"time": value,
        #"genre": value,
        #"principalactor": value,
        # }
        # to send post request axios.post('http://localhost:8000/api/movie',data)
        data = request.data
        print(data)
        language = data.get('language')
        type = data.get('type')
        time = data.get('time')
        genre = data.get('genre')
        principalactor = data.get('principalactor')
        data_list =[ principalactor, language, type, genre, time]
        print(data_list)
        movies = final_Movie(data, data_list)
        print(movies)

        return JsonResponse({'movies':movies}, safe=False)
