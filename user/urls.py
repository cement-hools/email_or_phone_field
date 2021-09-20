from django.urls import path, include

from .views import adduser, statistic, export_excel, export_txt, login_view, \
    logout_view

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('useradd/', adduser, name='adduser'),
    path('statistic/', statistic, name='statistic'),
    path('export_excel/', export_excel, name='export_excel'),
    path('export_txt/', export_txt, name='export_txt'),
]
