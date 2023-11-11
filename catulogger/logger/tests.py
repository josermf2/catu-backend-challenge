from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
import json
from datetime import datetime, timedelta

from .models import Log

class LogViewsetTestCase(APITestCase):

    def setUp(self):
        Log.objects.create(who='user1', action_type='CREATE', object_type='Object1')
        Log.objects.create(who='user2', action_type='EDIT', object_type='Object2')

    def test_new_log_success(self):
        data = {"who": "user3", "action_type": "CREATE", "object_type": "Object3"}
        response = self.client.post('http://localhost:8080/log/new-log/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Log created"})
        self.assertEqual(Log.objects.filter(who="user3").count(), 1)

    def test_new_log_missing_parameter(self):
        data = {"who": "user4", "action_type": "CREATE"}  
        response = self.client.post('http://localhost:8080/log/new-log/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_get_logs_all(self):
        response = self.client.post('http://localhost:8080/log/get-logs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("All logs retrived", response.data["message"])

    def test_get_logs_by_user(self):
        data = {"user": "user1"}
        response = self.client.post('http://localhost:8080/log/get-logs/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("All logs from user1 retrived", response.data["message"])

    def test_get_logs_by_date_range(self):
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        finish_date = datetime.now().strftime("%Y-%m-%d")
        data = {"date": {"start_date": start_date, "finish_date": finish_date}}
        response = self.client.post('http://localhost:8080/log/get-logs/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("All logs from", response.data["message"])

    def test_get_logs_by_user_and_date_range(self):
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        finish_date = datetime.now().strftime("%Y-%m-%d")
        data = {"user": "user1", "date": {"start_date": start_date, "finish_date": finish_date}}
        response = self.client.post('http://localhost:8080/log/get-logs/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("All logs from user1 from", response.data["message"])

    def test_action_counts_success(self):
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        finish_date = datetime.now().strftime("%Y-%m-%d")
        data = {"start_date": start_date, "finish_date": finish_date}
        response = self.client.post('http://localhost:8080/log/action-counts/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("The count of log types", response.data["message"])

    def test_action_counts_invalid_date_format(self):
        data = {"start_date": "invalid_date", "finish_date": "invalid_date"}
        response = self.client.post('http://localhost:8080/log/action-counts/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid date format", response.data["error"])
