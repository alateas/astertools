from django.http import HttpResponse,HttpResponseForbidden 
from models import Fax

def fax_pdf(request, id):
    fax = Fax.objects.get(id=int(id))

    user = request.user
    if user.is_superuser or fax.fax_dev.has_access(user):
        response = HttpResponse()
        url = '/protected_media/faxes/%d.pdf' % fax.id # this will obviously be different for every ressource
        response['Content-Type']=""
        response['X-Accel-Redirect'] = url
        return response
    
    return HttpResponseForbidden()
