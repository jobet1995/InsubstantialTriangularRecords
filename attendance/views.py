from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        employee = Employee.objects(user=request.user.id)
        serializer = EmployeeSerializer(employee, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'lastname': request.data.get('lastname'),
            'firstname': request.data.get('firstname'),
            'middlename': request.data.get('middlename'),
            'ranks': request.data.get('ranks'),
            'assignment': request.data.get('assignment'),
            'user': request.user.id,
            'password': request.data.get('password')
        }

        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_employee(self, employee_id, user_id):
        try:
            return Employee.objects.get(id=employee_id, user=user_id)
        except Employee.DoesNotExist:
            return None

    def get(self, request, employee_id, *args, **kwargs):
        employee_instance = self.get_employee(employee_id, request.user_id)
        if not employee_instance:
            return Response(
                {
                    "res": "Object with employee id does not exist"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            serializer = EmployeeSerializer(employee_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, employee_id, *args, **kwargs):
        employee_instance = self.get_employee(employee_id, request.user_id)

        if not employee_instance:
            return Response(
                {"res": "Object with employee id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            'lastname': request.data.get('lastname'),
            'firstname': request.data.get('firstname'),
            'middlename': request.data.get('middlename'),
            'ranks': request.data.get('ranks'),
            'assignment': request.data.get('assignment'),
            'user': request.user.id,
            'password': request.data.get('password')
        }
        serializer = EmployeeSerializer(
            instance=employee_instance, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, employee_id, *args, **kwargs):
        employee_instance = self.get_employee(employee_id, request.user_id)

        if not employee_instance:
            return Response(
                {"res": "Object with employee id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        employee_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
