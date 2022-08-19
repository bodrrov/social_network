from django.shortcuts import render
from cms.models import CmsSlider
# Create your views here.

def slider(request):
    slider_list = CmsSlider.objects.all()
    return render(request, './index.html', {'slider_list2': slider_list}, )
