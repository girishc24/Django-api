from django.urls import path
from . import views
urlpatterns = [
    path('project/', views.projectadd),
    path('category/', views.Categoryadd),
    path('CategorySave/', views.CategorySave, name="CategorySave"),
   
]
