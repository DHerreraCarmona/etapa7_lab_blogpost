from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.create_post, name='create_post'),
]


"""
"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTM4MDEyNiwiaWF0IjoxNzQxMjkzNzI2LCJqdGkiOiIyMmM1ODFkZGEwY2Q0ODc2YmI4ZjRkZGMxMjMzNzI0YiIsInVzZXJfaWQiOjF9.LoGuFBsscF_VSivhik6ybUTd2ejEP1Z11_lqyxjVaSo",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxMjk0MDI2LCJpYXQiOjE3NDEyOTM3MjYsImp0aSI6IjA5ZTQyYjBjMGQxNDQ0NzA4NzkxOWExZTBkZDgzMDQxIiwidXNlcl9pZCI6MX0.xQyBkNQSCYwQIqijCvpoeogNlceMmNRufg06eEAy_Sg"
}

"""