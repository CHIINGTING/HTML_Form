from django.shortcuts import render
from django.http import HttpResponse
from mysite import models


# Create your views here.
def get_example(request):
    try:
        urid = request.GET['user_id']
        urpass = request.GET['user_pass']
        se_byear = request.GET['byear']
        urfcolor = request.GET.getlist('fcolor')
        loveMovie = request.GET['movie']
        if urid != None and urpass == "12345":
            verified = True
        else:
            verified = False
    except:
        urid = None
    years = range(1960, 2021 + 1)
    return render(request, 'get_example.html', locals())


def index(request, pid=None, del_pass=None):
    posts = models.Post.objects.filter(enabled=False).order_by('-pub_time')[:30]
    moods = models.Mood.objects.all()
    try:
        user_id = request.GET['user_id']
        user_pass = request.GET['user_pass']
        user_post = request.GET['user_post']
        user_mood = request.GET['mood']
    except:
        user_id = None
        message = '張貼每一則訊息,每個欄位都要填'
    if user_id is not None:
        mood = models.Mood.objects.get(status=user_mood)
        post = models.Post.objects.create(mood=mood, nickname=user_id, del_pass=user_pass, message=user_post)
        post.save()
        message = '儲存成功!記得編輯你的密碼[{}],之後才會顯示'.format(user_pass)
        posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:150]

    if del_pass and pid:
        try:
            post = models.Post.objects.get(id=pid)
        except:
            post = None
        if post.del_pass == del_pass:
            post.delete()
            message = "資料刪除成功"
        else:
            message = "密碼錯誤"

    return render(request, 'index.html', locals())
