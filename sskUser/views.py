from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm
from io import BytesIO
from django.core.cache import cache
from utils.captcha.xfzcaptcha import Captcha


# 登录
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return HttpResponse("账号或密码输入有误。请重新输入~")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'user/login2.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


# 注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect(reverse('index'))
        else:
            return HttpResponse('注册表单输入有误。请重新输入~')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'user/register.html', context)
    else:
        return HttpResponse('请使用GET或POST请求数据')


# 注销
def user_logout(request):
    logout(request)
    return redirect("sskUser:login")


# 删除
def user_delete(request):
    pass


# TODO
# 信息编辑

# 修改密码

# 找回密码
def user_resetpwd(request):
    return render(request, 'user/resetpwd.html')


# 图形验证码
def img_captcha(request):
    text, image = Captcha.gene_code()
    # BytesIO：相当于一个管道，用来存储图片的流数据
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out, 'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    # 从BytesIO的管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()

    # 12Df：12Df.lower()
    cache.set(text.lower(), text.lower(), 5 * 60)

    return response


# 用户中心
def user_info(request):
    return render(request,'user/index.html')
