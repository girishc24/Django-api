from rest_framework import serializers
from .models import Sports, Customers, Projecttable, Category, Task, Comment, Unit, Material, MaterialPurchaseItem, MaterialPurchase, Party, Used
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer, UserSerializer  
from django.contrib.auth.hashers import make_password


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sports
        fields = ['id', 'Fullname', 'score']
    Fullname=serializers.SerializerMethodField(method_name='get_fullname')
    

    def get_fullname(self, obj):
        return obj.fname + obj.lname
    
    
class UserCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['id', 'username', 'password', 'email', 'first_name', 'last_name',]

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)



class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ('phone', 'birth_date')

 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',  'email', 'first_name', 'last_name',]



class CustomersTabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ('phone', ) 

        
class UserSerializeCommon(serializers.ModelSerializer):
    
    fullname = serializers.SerializerMethodField(method_name='get_fullnames')
    #customers=CustomersTabelSerializer(many=True)

    class Meta:
        model = User
        fields = ['fullname']
        

    def get_fullnames(self, a):
        return a.first_name + a.last_name



class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projecttable
        fields = ['title', 'description', 'city', 'address', 'categories']

    

class ProjectRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projecttable
        fields = ['id', 'title', 'description', 'city', 'address', 'current_date']



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =['id','name',]

class ProjectCommonSerializer(serializers.ModelSerializer):
    #create_user = UserSerializeCommon(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    fullname = serializers.SerializerMethodField(read_only=True)
    
    
    def get_fullname(self, obj):
        return obj.create_user.first_name + obj.create_user.last_name 
    

    class Meta:
        model = Projecttable
        fields = ['id', 'title', 'description', 'city', 'address', 'current_date', 'fullname', 'categories']


class ProjectIDSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Projecttable
        fields = ['id']
    


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projecttable
        fields = ['title', 'description', 'city', 'address']

    

class TaskSerializer(serializers.ModelSerializer):
    #project = ProjectCommonSerializer()
    #user = UserSerializer(many=True)
    class Meta:
        model =Task
        fields = ['title','name','description','sdate','edate','progress','status','project','user']

class GetTaskSerializer(serializers.ModelSerializer):
    project = ProjectCommonSerializer()
    user = UserSerializer(many=True)
    class Meta:
        model =Task
        fields = ['title','name','description','sdate','edate','progress','status','project','user']


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['progress', 'status']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['task', 'user', 'name']


class CommentGetSerializer(serializers.ModelSerializer):
    task = GetTaskSerializer()
    user = UserSerializer()
    comment = serializers.CharField(source='name')

    class Meta:
        model = Comment
        fields = ['task', 'user', 'comment']


class UnitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Unit
        fields =['id','unit_name']

class MaterialNameSerializer(serializers.ModelSerializer):
    unit = UnitSerializer()
    class Meta:
        model = Material
        fields =['material_name', 'unit', ]

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields =['material_name', 'project', 'unit']


class MaterilaGetSerializer(serializers.ModelSerializer):
    
    project = ProjectIDSerializer()
    unit = UnitSerializer()


    class Meta:
        model = Material
        fields =['create_date','updated_date','material_name', 'project', 'unit']


class MaterialUpadteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['material_name', 'project', 'unit']


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields =['Party_name', 'phone_number']


class PartyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields =['Party_name']


class MaterialPurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialPurchaseItem
        fields = ['material', 'unitrate', 'quantity', 'total', 'project']


class MaterialPurchaseItemGetSerializer(serializers.ModelSerializer):
    material = MaterialNameSerializer()
    class Meta:
        model = MaterialPurchaseItem
        fields = ['material', 'unitrate', 'quantity', 'total']

class MaterialPurchaseViewSerializer(serializers.ModelSerializer):
    person = PartySerializer(many=True)

    class Meta:
        model = MaterialPurchase
        fields = ['person', 'date', 'additional_charge', 'discount',  'gst', 'total_amount', 'paid_amount', 'balance', 'add_notes', 'project', 'materials' ]


class UsedGetSerilaizer(serializers.ModelSerializer):
    user_id = UserSerializeCommon()
    class Meta:
        model = Used
        fields = ['create_date','quantity','notes', 'user_id']


class UsedGetItemSerilaizer(serializers.ModelSerializer):
    user_id = UserSerializeCommon()
    class Meta:
        model = Used
        fields = ['create_date','quantity','notes', 'user_id']


class UsedSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Used
        fields = ['create_date','quantity','notes','materialpurchaseitem']


class MaterialPurchaseSignalItemSerializer(serializers.ModelSerializer):
    person = PartyViewSerializer(source='material_purchase.person', read_only=True)
    material = MaterialNameSerializer()
    total_received = serializers.IntegerField(source='quantity')
    used = serializers.SerializerMethodField()
    
    class Meta:
        model = MaterialPurchaseItem
        fields = ['create_date',  'quantity', 'total', 'person', 'total_received', 'material', 'used']

    def get_used(self, obj):
        used_instance = Used.objects.filter(materialpurchaseitem=obj.id)
        used_data = []
        total_used = 0
        for used_instance in used_instance:
            used_serializer = UsedGetSerilaizer(used_instance)
            used_data.append(used_serializer.data)
            total_used += used_instance.quantity
        return {'used': used_data, 'total_used': total_used}
    

class MaterialPurchaseSerializer(serializers.ModelSerializer):
    materials = MaterialPurchaseItemSerializer(many=True)

    class Meta:
        model = MaterialPurchase
        fields = ['person', 'date', 'additional_charge', 'discount',  'gst', 'total_amount', 'paid_amount', 'balance', 'add_notes', 'project', 'materials' ]

    def create(self, validated_data):
        materials_data = validated_data.pop('materials')
        material_purchase = MaterialPurchase.objects.create(**validated_data)
        for material_data in materials_data:
            MaterialPurchaseItem.objects.create(material_purchase=material_purchase, **material_data)
        return material_purchase



