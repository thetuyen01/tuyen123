from django.urls import path
from .import views

app_name = 'core'


urlpatterns = [
    path('product/<int:id>/', views.oneproduct, name='oneproduct'),
    path('', views.index, name='index'),
    path('product/<slug:slug>/', views.ViewCategory, name='viewcategory'),
    path('search/', views.serach, name='search'),
    path('cart/', views.cart__, name='cart'),
    path('addorderitem/', views.addorderitem, name='addorderitem'),
    path('edit/<int:id>/', views.edititem, name='edit'),
    path('checkout/', views.checkout, name='checkout'),
    path('pending/', views.pending, name='pending'),
    path('profile/', views.profile, name='profile'),
    path('commet/', views.comment_, name='commet'),
    path('contact/', views.contact, name='contact'),
    path('updateprofile/', views.updateprofile, name='updateprofile')
]
