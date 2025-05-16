from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
  # admin stuff
  path('admin/', admin.site.urls),
  path("accounts/", include("django.contrib.auth.urls")),
  # app
  path('', views.index, name='index'),
  path('register/<str:hunt>/<str:egg>', views.register, name='register'),
  path('register/<str:hunt>', views.register, name='register'),
  path('egg/<str:hunt>', views.start, name='start'),
  path('egg/<str:hunt>/<str:egg>', views.egg, name='egg'),
  # app admin
  path('overview', views.overview_list, name='overview_list'),
  path('overview/<str:hunt>', views.overview_details, name='overview_details'),
  path('overview/<str:hunt>/clear', views.overview_details_clear, name='overview_details_clear'),
]
