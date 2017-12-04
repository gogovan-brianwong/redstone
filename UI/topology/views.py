# Create your views here.
from Infrastructure.public import *

@check_login
def index(request):
    return render(request, 'topology_index.html')


