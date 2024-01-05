from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Sports, Customers, Projecttable, Category, Task, Comment, Material, Party, MaterialPurchaseItem, Used, Unit
from .serializers import SportSerializer, CustomersSerializer, UserCreateSerializers, ProjectSerializer, UserSerializer, ProjectRetrieveSerializer, ProjectUpdateSerializer, ProjectCommonSerializer, CategorySerializer,TaskSerializer, GetTaskSerializer, TaskUpdateSerializer, CommentSerializer, CommentGetSerializer, MaterialSerializer, MaterilaGetSerializer, MaterialUpadteSerializer, MaterialPurchaseSerializer, PartySerializer, MaterialPurchaseItemGetSerializer, MaterialPurchaseSignalItemSerializer, MaterialPurchaseViewSerializer, UsedSerilaizer, UsedGetSerilaizer, UsedGetItemSerilaizer, UnitSerializer
from rest_framework.views import APIView
from weasyprint import HTML, CSS
from django.template.loader import get_template
import requests
import tempfile
import codecs

def new(request):
    return HttpResponse('HELLO WORLD')

@api_view(['GET', 'POST'])
def sports(request):
    if request.method == 'GET':
        queryset = Sports.objects.filter(active=0)
        serializers=SportSerializer(queryset, many=True)
        return Response(serializers.data)
    else:
        serializers = SportSerializer(data=request.data)
        if serializers.is_valid():
            fullname = request.data.get('fullname')
            names = fullname.split(' ')
            fname = names[0]
            lname = names[-1]
            serializers.save(fname=fname, lname=lname)
            return Response(serializers.data)
       

@api_view(['GET', 'PUT'])
def sportsview(request, pk):
    sports =get_object_or_404(Sports, id=pk)
    if request.method =='GET':
        serializer=SportSerializer(sports)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializers =SportSerializer(sports, data=request.data)
        if serializers.is_valid():
            fullname = request.data.get('fullname')
            names = fullname.split(' ')
            fname = names[0]
            lname = names[-1]
            serializers.save(fname=fname, lname=lname)
            return Response(serializers.data)
    

class CreateUserView(APIView):
    def post(self, request):
        user_serializer = UserCreateSerializers(data=request.data)
        customer_serializer = CustomersSerializer(data=request.data)

        if user_serializer.is_valid(raise_exception=True) and customer_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            customer = customer_serializer.save(users=user)
            return Response({'message': 'Data entered successfully', 'data': request.data}, status=status.HTTP_201_CREATED)

        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view([ 'POST'])
def project(request):
    if request.method == 'POST':
        user_id = request.user.id
        project_data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'city': request.data.get('city'),
            'address': request.data.get('address'),
            'categories': request.data.get('categories'),
        }
        serializer = ProjectSerializer(data=project_data)
        if serializer.is_valid():
            project = serializer.save(create_user_id=user_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
        
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


    
@api_view(['GET'])
def viewproject(request):
    if request.method == 'GET':
        user_id = request.user.id
        queryset = Projecttable.objects.filter(delete_status=0, create_user_id=user_id).order_by('-id')
        project_serializer  = ProjectRetrieveSerializer(queryset, many=True)
        projects_data = project_serializer.data

        for project_data in projects_data:
            
            users = User.objects.filter(id=user_id)
            userserializer = UserSerializer(users, many=True)
            project_data['users'] = userserializer.data

            customer = Customers.objects.filter(users_id=user_id)
            customersserializer = CustomersSerializer(customer, many=True)
            project_data['Customers'] = customersserializer.data

        return Response(projects_data)
    


@api_view(['GET'])
def viewprojectcommon(request, page_size):
    if request.method == 'GET':
        
        class CustomPagination(PageNumberPagination):
   
          page_size = 2  
          page_size_query_param = 'page_size'  
          max_page_size = 100 

        paginator = CustomPagination()
        paginator.page_size = int(page_size)
        queryset = Projecttable.objects.filter(delete_status=0).order_by('-id')
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        project_serializers  = ProjectCommonSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(project_serializers.data)


@api_view(['GET'])
def projectview(request):
    if request.method == 'GET':
        user_id = request.user.id
        queryset = Projecttable.objects.filter(delete_status=0, create_user_id=user_id).order_by('-id')
        project_serializer  = ProjectRetrieveSerializer(queryset, many=True)
        return Response(project_serializer.data)

@api_view(['DELETE'])
def deleteproject(request, pk):
    Project = Projecttable.objects.get(id=pk)
    if request.method == 'DELETE':
        Projecttable.objects.filter(id=Project.id).update(delete_status=1)
        return Response('Data Deleted Succefully', status=status.HTTP_204_NO_CONTENT)
    
    

@api_view(['PUT'])
def update_project(request, pk):
    project = Projecttable.objects.get(id=pk)
    serializer = ProjectUpdateSerializer(project, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST','GET'])
def createcategory(request):
    if request.method == 'POST':
        serializer_category=CategorySerializer(data=request.data)
        if serializer_category.is_valid():
            serializer_category.save()
            return Response(serializer_category.data)
    elif request.method == 'GET':
        queryset = Category.objects.all()
        serializer =CategorySerializer(queryset, many=True)
        return Response(serializer.data)
    

@api_view(['POST','GET'])
def createtask(request):
    if request.method == 'POST':
        serlializer_task = TaskSerializer(data=request.data)
        if serlializer_task.is_valid():
            serlializer_task.save()
            return Response(serlializer_task.data)
        else:
            return Response(serlializer_task.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        queryset =Task.objects.all().order_by('-id')
        serializer = GetTaskSerializer(queryset, many=True)
        return Response(serializer.data)



@api_view(['GET'])
def viewtask(request):
    if request.method == 'GET':
        user_id = request.user.id
        sql = Task.objects.filter(user=user_id).order_by('-id')
        serializer =GetTaskSerializer(sql, many=True)
        return Response(serializer.data)
    else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def updatetask(request, pk):
    if request.method == 'POST':
        user_id = request.user.id
        task = Task.objects.get(id=pk, user=user_id)
        
        serializer = TaskUpdateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def commenttask(request):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,  status=status.HTTP_200_OK)
    if request.method == 'GET':
        querset = Comment.objects.all()
        serializer = CommentGetSerializer(querset, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def unit(request):
    if request.method == 'GET':
        queryset = Unit.objects.all()
        serializer = UnitSerializer(queryset, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        
    
    
@api_view(['POST','GET'])
def material(request):
    if request.method == 'POST':
        user_id = request.user.id
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=user_id)
            serializer.save(user_id=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        material = Material.objects.filter(delete_status=0)
        serializer = MaterilaGetSerializer(material, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['PUT'])
def materialUpdate(request, pk):
    mid = Material.objects.get(id=pk)
    serializer = MaterialUpadteSerializer(mid, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deletematerial(request, pk):
    new = Material.objects.get(id=pk)
    if request.method == 'DELETE':
        Material.objects.filter(id=new.id).update(delete_status=1)
        return Response('Data Deleted Succefully', status=status.HTTP_204_NO_CONTENT)
    

@api_view(['POST'])
def party(request):
    user_id = request.user.id
    if request.method == 'POST':
        serializer = PartySerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(id=user_id)
            serializer.save(user_id=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def MaterialPurchase(request):
    user_id = request.user.id
    if request.method == 'POST':
        serializer = MaterialPurchaseSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=user_id)
            serializer.save(user_id=user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def materialitem(request,pk):
    if request.method == 'GET':
        project = MaterialPurchaseItem.objects.filter(project=pk)
        serializer = MaterialPurchaseItemGetSerializer(project, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def materialitemview(request,pk):
    if request.method == 'GET':
        project = MaterialPurchaseItem.objects.filter(id=pk)
        serializer = MaterialPurchaseSignalItemSerializer(project, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        

@api_view(['POST','GET'])
def materialused(request):
    user_id = request.user.id
    if request.method=='POST':
        serializer = UsedSerilaizer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=user_id)
            serializer.save(user_id=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method=='GET':
        used = Used.objects.filter(delete_status=0)
        serializer = UsedGetSerilaizer(used, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT','GET'])
def materialuseditem(request,pk):
    
    if request.method=='PUT':
        used_instance = Used.objects.get(id=pk)
        serializer = UsedGetItemSerilaizer(used_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method=='GET':
        used = Used.objects.filter(id=pk)
        serializer = UsedGetItemSerilaizer(used, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
@api_view(['DELETE'])
def deleteuseditem(request, pk):
    new = Used.objects.get(id=pk)
    if request.method == 'DELETE':
        Material.objects.filter(id=new.id).update(delete_status=1)
        return Response('Data Deleted Succefully', status=status.HTTP_204_NO_CONTENT)

def html_to_pdf(request):
    html_file_path = 'members/templates/pdf/transaction.html'

    with open(html_file_path, 'r') as file:
        html_content = file.read()
    

    pdf_file = HTML(string=html_content).write_pdf(
       
        presentational_hints=True,
        base_url=request.build_absolute_uri(),
       
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="output.pdf"'
    response.write(pdf_file)

    return response


def htmltopdfnew(request):
    html_file_path = 'members/templates/pdf/new.html'

    with codecs.open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    pdf_file = HTML(string=html_content).write_pdf(
        presentational_hints=True,
        base_url=request.build_absolute_uri(),
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="output.pdf"'
    response.write(pdf_file)

    return response