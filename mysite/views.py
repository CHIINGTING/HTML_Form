from django.shortcuts import render


# Create your views here.
def get_example(request):
    try:
        urid = request.GET['user_id']
        urpass = request.GET['user_pass']
    except:
        urid = None

    years = range(1960, 2021 + 1)
    return render(request, 'get_example.html', locals())
