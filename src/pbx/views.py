from django.http import HttpResponse,HttpResponseForbidden
from django.shortcuts import render_to_response
from models import Users

def phonebook(request):
    html = ''
    
    for i in Users.get_phones([251, 298, 911, 256, 257, 250, 300, 240]):
        html += '%s - %s<br/>' % (i.extension, i.name)

    html = '<html><body>%s</body></html>' % html
    return render_to_response('pbx/index.html', {'phones': Users.get_phones([251, 298, 911, 256, 257, 250, 300, 240])})
