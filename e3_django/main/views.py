from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Welcome user. This is the main index")