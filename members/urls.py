from django.urls import path
from .import views 
from .views import CreateUserView 

app_name = 'members'

urlpatterns = [
    path('', views.new),
    path('sports/', views.sports),
    path('sports/<int:pk>/', views.sportsview),
    path('createproject/', views.project),
    path('viewproject/', views.viewproject),
    path('projectview/', views.projectview),
    path('viewprojectcommon/<int:page_size>/', views.viewprojectcommon),
    path('deleteproject/<int:pk>/', views.deleteproject),
    path('update_project/<int:pk>/', views.update_project),
    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path('create-category/', views.createcategory),
    path('create-task/', views.createtask),
    path('viewtask/', views.viewtask),
    path('updatetask/<int:pk>/', views.updatetask),
    path('commenttask/', views.commenttask),
    path('unit/', views.unit),
    path('material/', views.material),
    path('material/<int:pk>/', views.materialUpdate),
    path('deletematerial/<int:pk>/', views.deletematerial),
    path('addparty/', views.party),
    path('materialpurchase/', views.MaterialPurchase),
    path('materialitem/<int:pk>/', views.materialitem),
    path('materialitemview/<int:pk>/', views.materialitemview),
    path('materialused/', views.materialused),
    path('materialuseditem/<int:pk>/', views.materialuseditem),
    path('deleteuseditem/<int:pk>/', views.deleteuseditem),
    path('html-to-pdf/', views.html_to_pdf, name='html_to_pdf'),
    path('htmltopdf/', views.htmltopdfnew, name='htmltopdf'),
    
]
