from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

# import Response
from rest_framework.response import Response

# importing models
from .models import Log

# importing status
from rest_framework import status

# Create your views here.
class LogViewset(viewsets.ViewSet):
    
    '''
    Esse método fara uma requisição para
    o endpoint /log/hello-world e retornará uma
    mensagem de Hello, world!
    '''
    @action(detail=False, methods=["get"], url_path="hello-world")
    def hello_world(self, request):
        return Response({"message": "Hello, world!"})
    
    '''
      Esse método fara uma requisição para
      o endpoint /log/ping e retornará uma
      mensagem de pong com os dados da requisição
    '''
    @action(detail=False, methods=["post"], url_path="ping")
    def ping(self, request):
        return Response({"message": "pong", "data": request.data})
      
    # Você pode fazer sua mágica aqui mesmo :)