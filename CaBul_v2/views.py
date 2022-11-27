from django.shortcuts import render


def account(request):
    if request.method == 'GET':
        return render(request, 'account.html')