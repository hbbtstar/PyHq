from django.shortcuts import render

# Create your views here.
def get_skills(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        skills = []
        return

def skillplanner(request):
    return render(request, 'skillplanner.html')

