# from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import Question, Choice

# 引入generic以使用generic view
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django import forms

from django.views.decorators.csrf import csrf_exempt
from .models import Choice, Question, User

############### 因为重新引入generic view的原因，index，detail，results不再使用，而改为generic view来使用######################
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list,}
#     return render(request, 'polls/index.html', context)
#     #引入render的快捷方式，所以不再需要HttpResponse的方法
#
# def detail(request,question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#     # 引入get_object_or_404的快捷方式，所以不再需要这种原生写法
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'polls/detail.html', {'question': question})
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


#登录注册功能参考资料1 session+python3注册功能： http://lib.csdn.net/article/python/65599?knId=184
#参考资料2   数据库query set方法：             http://code.ziqiangxuetang.com/django/django-queryset-api.html
#参考资料3   python2+登录功能：                http://blog.csdn.net/foryouslgme/article/details/51377385
#登录用的表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密__码', widget=forms.PasswordInput())

#注册用的表单
class UserAddForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密__码', widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput())

#因为view中很多时候都要检测用户的登录情况，所以需要自定义一个装饰器，每次需要判断时，都要用一下
@csrf_exempt
def checklogin(func):
    #参数中一个*表示参数的个数可以不固定，两个*表示其他的关键字参数都将被放在一个字典中传递给函数
    def checkuser(request,*args,**kwargs):
        username = request.session.get('username')
        if username:
            #返回一个带有参数的函数
            return func(request, *args, **kwargs)
        else:
            # 此处不可以用render login的页面，因为现在的路由是在regist中，只能使用重定向,同时此处重定向只能使用reverse来反推出URL
            return HttpResponseRedirect(reverse('polls:login'))
    return checkuser


@csrf_exempt
def regist(request):
    if request.method == 'POST':
        uf = UserAddForm(request.POST)
        if uf.is_valid():
            #获取表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            #添加到数据库
            registAdd = User.objects.get_or_create(username = username, password = password)[1]
            if registAdd == False:
                #此处不可以用render login的页面，因为现在的路由是在regist中，只能使用重定向,同时此处重定向只能使用reverse来反推出URL
                return HttpResponseRedirect(reverse('polls:login'))
            else:
                request.session.username = username
                latest_question_list = Question.objects.order_by('-pub_date')[:5]
                context = {'latest_question_list': latest_question_list, 'username': username}
                return render(request, 'polls/index.html', context)
    else:
        uf = UserAddForm()
        return render(request, 'polls/regist.html', {'uf': uf})
#避免跨域请求～～～
#[添加检测登录状态的装饰器之后，就不再需要判断request的方法了，即 和regist的逻辑内容不再类似，少了一步判断]方括号中是错误的
#!!!此处不可以加检测登录状态的装饰器，因为会导致无穷尽的重定向，装饰器要求执行login，执行login之前又会再次执行装饰器～～～～～～～～～
@csrf_exempt
def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #对比提交的数据与数据库中的数据
            user = User.objects.filter(username = username, password = password)
            if user:
                #用session来记录登录状态
                request.session['username']=username
                latest_question_list = Question.objects.order_by('-pub_date')[:5]
                context = {'latest_question_list': latest_question_list, 'username': username}
                return render(request,'polls/index.html',context)
            else:
                uf = UserForm()
                return render(request,'polls/login.html',{"uf": uf})
    else:
        uf = UserForm()
        return render(request, 'polls/login.html', {'uf': uf})

# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'
    # def get_queryset(self):
    #     '''Return the last five published questions.'''
    #     return Question.objects.order_by('-pub_date')[:5]
# 因为重新加入登录信息，所以不再使用默认的视图    首页视图
def index(request):
    #尝试获取session中的username，使用session必须保证设置中有session中间件，在插入的应用中也有session应用
    username = request.session.get('username')
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list, 'username':username}
    return render(request, 'polls/index.html', context)
    #引入render的快捷方式，所以不再需要HttpResponse的方法

@checklogin
def logout(request):
    del request.session['username']
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

    #添加检测登录状态的装饰器之后，不需要对session进行判断
    # username = request.session.get('username')
    # if username:
    #     del request.session['username']
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    # return render(request, 'polls/index.html', context)



#需要在逻辑中添加东西，确保在没有登录时，无法投票,所以不再使用便捷视图
# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'
def detail(request,question_id):
    #尝试获取session中的username，使用session必须保证设置中有session中间件，在插入的应用中也有session应用
    username = request.session.get('username')
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question,'username': username}
    return render(request, 'polls/detail.html', context)


@checklogin
#此处注意，一旦使用装饰器，也不能再使用简洁视图
# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'
def results(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


@checklogin
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 使用'args'来传递参数
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    #使用新的处理函数，不再使用这种没有任何方法的处理方式
    # return HttpResponse("You're voting on question %s." % question_id)