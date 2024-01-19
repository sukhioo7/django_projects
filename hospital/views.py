from django.shortcuts import render

static_pages = ['about','contact','services']

def home(request):
    return render(request,'home.html')

def static_view(request,page_name):
    if page_name in static_pages:
        return render(request,f'{page_name}.html')
    else:
        return render(request,'404.html')

