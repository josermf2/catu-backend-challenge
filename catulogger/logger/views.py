from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

# import Response
from rest_framework.response import Response

# importing models
from .models import Log

# importing status
from rest_framework import status

import json
import datetime

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
      
    '''
        Esse método fará uma requisição para
        o endpoint /log/new-log com um payload
        que será salvo com um log no database e 
        retornará uma mensagem de sucesso ou de
        erro caso o payload não seja encontrado
        ou não possua um dos parâmetros necessarios
    '''
    @action(detail=False, methods=["post"], url_path="new-log")
    def new_log(self, request):
        if not request.body:
            return Response({"error": "Body not found in request"}, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({"error": "Error reading the body, check it to see if there is any error"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_log = Log(
                who = body["who"],
                action_type = body["action_type"],  
                object_type = body["object_type"],
            )
        except KeyError as e:
            return Response({"error": f"parameter {e} missing, check your body"}, status=status.HTTP_400_BAD_REQUEST)


        new_log.created_at = timezone.now()

        new_log.save()

        return Response({"message": "Log created"})

    '''
        Esse método fará uma requisição para
        o endpoint /log/get-logs e retornará 
        os logs salvos no database. Caso não 
        possua payload retornará todos os logs,
        caso possua um usuário no payload retornará
        os logs daquele usuário, caso possua uma 
        data de início e de fim retornará os logs
        naquele período. Ainda, se o payload 
        possuir data de inicío e fim e um usuário
        retornará os logs daquele usuário no período
        selecionado.
    '''
    @action(detail=False, methods=["post"], url_path="get-logs")
    def get_logs(self, request):
        all_logs = Log.objects.all().values()

        if not request.body:
            return Response({"message": "All logs retrived", "data": list(all_logs)})

        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({"error": "Bad request body"}, status=status.HTTP_400_BAD_REQUEST)


        if "user" in body:
            user = body["user"]
            if "date" not in body:
                return Response({"message": f"All logs from {user} retrived", "data": list(all_logs.filter(who=user))})

        if "date" in body:
            if "start_date" in body["date"] and "finish_date" in body["date"]:
                try:
                    start_date = timezone.make_aware(timezone.datetime.strptime(body["date"]["start_date"], "%Y-%m-%d"))
                    finish_date = timezone.make_aware(timezone.datetime.strptime(body["date"]["finish_date"], "%Y-%m-%d"))
                    if start_date == finish_date: 
                        return Response({"error": "The start_date and finish_date cannot be the same"}, status=status.HTTP_400_BAD_REQUEST)
                    if "user" not in body:
                        return Response({"message": f"All logs from {body['date']['start_date']} to {body['date']['finish_date']} retrived", "data": list(all_logs.filter(created_at__range=[start_date, finish_date]))})
                except ValueError:
                    return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": f"All logs from {user} from {body['date']['start_date']} to {body['date']['finish_date']} retrived", "data": list(all_logs.filter(who=user, created_at__range=[start_date, finish_date]))})

    '''
        Esse método fará uma requisição para
        o endpoint /log/action-counts e retornará
        a contagem de tipos de log por data no 
        período enviado no payload da requisição.
        Caso o período não seja enviado, a requisição
        retorna um erro.
    '''
    @action(detail=False, methods=["post"], url_path="action-counts")
    def action_counts(self, request):
        if not request.body:
            return Response({"error": "Body not found in request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({"error": "Bad request body"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = timezone.make_aware(timezone.datetime.strptime(body["start_date"], "%Y-%m-%d"))
            finish_date = timezone.make_aware(timezone.datetime.strptime(body["finish_date"], "%Y-%m-%d"))
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        if start_date == finish_date: 
            return Response({"error": "The start_date and finish_date cannot be the same"}, status=status.HTTP_400_BAD_REQUEST)

        action_counts = Log.objects.filter(created_at__range=(start_date, finish_date)).values(
            'created_at__date',
            'action_type'
        ).annotate(count=Count('action_type'))
        
        response_data = {}

        for count in action_counts:
            date_key = count['created_at__date'].strftime('%d/%m/%Y')

            if date_key not in response_data:
                response_data[date_key] = {}

            response_data[date_key][count['action_type'].upper()] = count['count']

        current_date = start_date
        while current_date <= finish_date:
            date_key = current_date.strftime('%d/%m/%Y')
            if date_key not in response_data:
                response_data[date_key] = {'CREATE': 0, 'EDIT': 0, 'UPDATE': 0, 'DELETE': 0}
            current_date += timezone.timedelta(days=1)

        return Response({"message": f"The count of log types from {body['start_date']} to {body['finish_date']} was retrived", "data": response_data})