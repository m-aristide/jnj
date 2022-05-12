from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import RequestDataTooBig
from django.shortcuts import redirect


class CheckRequest(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            body = request.body
        except RequestDataTooBig:
            request.session['alerte'] = {'success': False, 'message': 'Fichier image trop gros !'}
            if 'update' in request.path :
                return redirect(f"/inscrits/{request.path.split('/')[2]}")
            else:
                return redirect('index')

        response = self.get_response(request)
        return response