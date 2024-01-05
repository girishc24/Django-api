from django.contrib.auth.models import User
from django.db import models
from django.conf import settings



class Sports(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    score=models.CharField(max_length=2)
    active=models.CharField(max_length=1, default=0)

    def __str__(self):
        return  f"{self.fname} {self.lname}"
    


class Customers(models.Model):
    
    phone=models.CharField(max_length=255)
    birth_date=models.DateField(blank=True, null=True)
    users = models.ForeignKey(User, related_name='customers', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.users.first_name} {self.users.last_name}"
    

class Project(models.Model):

    title=models.CharField(max_length=255)
    description=models.TextField()
    city=models.CharField(max_length=255)
    create_user=models.OneToOneField(User, on_delete=models.CASCADE)
    address=models.CharField(max_length=500)
    current_date=models.DateField(auto_now_add=True)
    delete_status=models.CharField(max_length=2, default='0')


class Category(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Projecttable(models.Model):

    title=models.CharField(max_length=255)
    description=models.TextField()
    city=models.CharField(max_length=255)
    create_user=models.ForeignKey(User, on_delete=models.CASCADE)
    address=models.CharField(max_length=500)
    current_date=models.DateField(auto_now_add=True)
    delete_status=models.CharField(max_length=2, default='0')
    categories = models.ManyToManyField(Category)


    def __str__(self) -> str:
        return f"{self.title}"
    

class Task(models.Model):
    title=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    sdate=models.DateField()
    edate=models.DateField()
    progress=models.CharField(max_length=255)
    status=models.CharField(max_length=255)
    project=models.ForeignKey(Projecttable, on_delete=models.CASCADE)
    user=models.ManyToManyField(User)


class Comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    task=models.ForeignKey(Task, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)


class Device(models.Model):
    channel_name=models.CharField(max_length=255)
    device_id=models.CharField(max_length=255)


class Unit(models.Model):
    unit_name=models.CharField(max_length=255)
    

    def __str__(self) -> str:
        return f"{self.unit_name}"
    
class Party(models.Model):
   
    Party_name= models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Material(models.Model):
    create_date=models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now_add=True)
    material_name=models.CharField(max_length=255)
    unit=models.ForeignKey(Unit, on_delete=models.CASCADE)
    project=models.ForeignKey(Projecttable, on_delete=models.CASCADE)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    delete_status=models.CharField(max_length=2, default='0')


class MaterialPurchase(models.Model):
    create_date=models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now_add=True)
    person = models.ForeignKey(Party, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    additional_charge = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    gst = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    add_notes = models.CharField(max_length=500)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    project=models.ForeignKey(Projecttable, on_delete=models.CASCADE, default='73')
    delete_status=models.CharField(max_length=2, default='0')


class MaterialPurchaseItem(models.Model):
    create_date=models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now_add=True)
    material_purchase = models.ForeignKey(MaterialPurchase, related_name='materials', on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    unitrate = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    project=models.ForeignKey(Projecttable, on_delete=models.CASCADE, default='73')
    delete_status=models.CharField(max_length=2, default='0')

class Used(models.Model):
    create_date=models.DateField(auto_now_add=True)
    update_date=models.DateField(auto_now_add=True)
    quantity=models.PositiveBigIntegerField()
    notes=models.CharField(max_length=255,)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    materialpurchaseitem=models.ForeignKey(MaterialPurchaseItem, on_delete=models.CASCADE)
    delete_status=models.CharField(max_length=2, default='0')




