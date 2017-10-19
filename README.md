# Django-regist-login
<h2>该实例是在已有的Django官网的实例的基础上进行的更改，主要实现了以下的功能：</h2>
<p>1.主页个详情页可以随意查看
<p>2.主要可以登录注册
<p>3.必须在登录状态下才可以投票或者查看投票结果
<h2>与官网实例的不同之处概括如下：</h2>
<p>1.models.py中添加一个User类，包含三个字段
<p>2.url.py和view.py中添加regis和login的相关逻辑  且get和post方法都是写在一个函数中，返回get的网页或者是处理post的数据，只需一个判断即可解决
<p>3.需要在view中引入forms模块，表单在模版中需要单独渲染
<p>4.添加防跨域的装饰器，解决跨域问题，包括form的模版中也要添加
<p>5.自己封装一个装饰器，用于检测用户的登录状态，在后面直接用于装饰各种类