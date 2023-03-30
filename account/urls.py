from django.urls import path

from .import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('login/', views.login_, name='login'),
    path('forgetpassword/', views.forgetpassword, name='forgetpassword'),
    path('change/<token>', views.change, name='change'),
    path('logout/', views.out, name='logout'),
    path('doimatkhau/', views.doimatkhau, name='doimatkhau')
]
