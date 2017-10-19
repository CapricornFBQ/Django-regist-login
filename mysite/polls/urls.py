from django.conf.urls import url

from . import views

#添加命名空间
app_name = 'polls'
urlpatterns = [
    # 因为要使用generic views 所以这些都不再使用了------因为使用装饰器等原因，使用原生的方法
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    #第三个参数主要是用于模板中的href属性
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    # url(r'^$', views.index, name='index'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # #第三个参数主要是用于模板中的href属性
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    #添加注册登录功能
    url(r'^login/$', views.login, name='login'),
    url(r'^regist/$', views.regist, name='regist'),
    url(r'^logout/$', views.logout, name='logout')
]
