from django.shortcuts import redirect, render

from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login

def logout(request):
    auth_logout(request)
    return redirect('index')

def connexion(request):
    alerte = request.session.get('alerte', None)
    if alerte :
        del request.session['alerte']
    return render(request, 'login.html', context={'alerte': alerte})

def login(request) :
    print(request.POST.get('username'))
    print(request.POST.get('password'))
    user = authenticate(username = request.POST.get('username'), password = request.POST.get('password'))
    print(user)

    if user is not None:
        auth_login(request, user)
        return redirect('index')
    else:
        request.session['alerte'] = True
        return redirect('connexion')