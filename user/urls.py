from django.urls import path

from .views import adduser, statistic, export_excel, export_txt

urlpatterns = [
    path('useradd/', adduser, name='adduser'),
    path('statistic/', statistic, name='statistic'),
    path('export_excel/', export_excel, name='export_excel'),
    path('export_txt/', export_txt, name='export_txt'),
]
