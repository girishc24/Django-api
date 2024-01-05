from django.shortcuts import render
from django.http import HttpResponse
from members.models import Category, Projecttable



def projectadd(request):
    data = Category.objects.all()
    context = {'data': data}
    return render(request, 'project.html', context)


def Categoryadd(request):
    return render(request, 'category.html')


def CategorySave(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        en=Category.objects.create(name=name)
    return render(request, 'category.html')

def addproject(request):
    if request.method == 'POST':
        
        title=request.POST.get('title')
        description=request.POST.get('description')
        city=request.POST.get('city')
        address=request.POST.get('address')
        category_ids=request.POST.getlist('category')
        project = Projecttable.objects.create(title=title, description=description, city=city, address=address)
        categories = Category.objects.filter(id__in=category_ids)
        project.category.set(categories)
        return render(request, 'success.html') 
    else:
        return('project.html')
        