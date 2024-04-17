'''
Django中有个内置app 名为 django.contrib.auth ，缺省包含在项目Installed App设置中。
这个app 的 models 定义中包含了一张 用户表，名为 auth_user 。
django.contrib.auth 这个app 已经 为我们做好了登录验证功能。
我们只需要使用这个app库里面的方法就可以了。
Django的文档就给出了登录和登出代码范例，我们稍微修改一下。
'''

from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
def signin(request):
    # 从post中获取用户密码
    user_username = request.POST.get('username')
    user_password = request.POST.get('password')

    # 使用Django auth库中的方法校用户名、密码
    user = authenticate(username=user_username,password=user_password)

    # 如果找得到账号，并且密码正确
    if user is not None:
        if user.is_active:
            if user.is_superuser:
                login(request, user)
                # 在session中存入用户类型
                request.session['usertype'] = 'mgr'

                return JsonResponse({'ret': 0})
            else:
                return JsonResponse({'ret': 1, 'msg': '请使用管理员账户登录'})
        else:
            return JsonResponse({'ret': 0, 'msg': '用户已经被禁用'})

        # 否则就是用户名、密码有误
    else:
        return JsonResponse({'ret': 1, 'msg': '用户名或者密码错误'})

# 登出处理
def signout( request):
    # 使用登出方法
    logout(request)
    return JsonResponse({'ret': 0})