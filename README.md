# 一、准备和URL路由

## Django相关命令

```python
# 安装
pip install django
# 查看版本
python -m django --version
# 创建项目
django-admin startproject 项目名称
# 运行web服务
python manage.py runserver 0.0.0.0:8000
```

## 设置Django为中文：

```python
# 项目文件夹下的setting.py
LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
```

## 路由：

```python
# 添加如下的路由记录
# 都根据 sales.urls 里面的 子路由表进行路由
path('sales/', include('sales.sales.urls')),
```

## 子路由：

```python
# 主路由中添加以下记录
path('orders/', views.listorders),
# 子路由中添加的一样
    # 添加如下的路由记录
    path('orders/', views.listorders),
    path('customers/', views.listcustomers),
```





# 二、数据和表

## 创建数据库和表

我们使用命令创建的项目， 缺省就是使用 sqlite。 而且对于的数据库文件，缺省的文件名是 `db.sqlite3` ， 就在项目的根目录下面


首先我们需要创建数据库，执行如下命令

```
python manage.py migrate
```

就会在 项目的根目录下面 生成一个配置文件中指定的数据库文件 `db.sqlite3`。

关于SQLite管理工具，可以使用SQLiteStudio，https://sqlitestudio.pl/

### 创建数据库具体步骤

#### 1、定义所需要的表



```python
from django.db import models

class Customer(models.Model):
    # 客户名称
    name = models.CharField(max_length=200)
    # 联系电话
    phonenumber = models.CharField(max_length=200)

    # 地址
    address = models.CharField(max_length=200)
```

#### 2、 INSTALLED_APPS 配置项 加入如下内容

 在项目的配置文件 `settings.py` 中， INSTALLED_APPS 配置项 加入如下内容



```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 加入下面这行
    'common.apps.CommonConfig',
]
```

#### 3、执行迁移命令

```python
python manage.py makemigrations
python manage.py migrate
```



## ORM(对象关系映射)

Django 让开发者 通过 类 和 实例的操作 来对应 数据库 表 和记录的操作。

这样，开发者对数据库的访问，从原来的使用底层的 sql 语句，变成 面向对象的开发，通过一系列对象的类定义 和方法调用就可以 操作数据库。



## Django Admin 管理数据

Django提供了一个管理员操作界面可以方便的 添加、修改、删除你定义的 model 表数据。

首先，我们需要创建 一个超级管理员账号。

进入到项目的根目录，执行如下命令，依次输入你要创建的管理员的 登录名、email、密码。

```
python manage.py createsuperuser
```

然后在相应的文件下的admin.py注册

```
admin.site.register(Customer)
```

创建后访问

http://127.0.0.1/admin/



如果想使用中文的Admin界面，修改： `settings.py` 中 `MIDDLEWARE` 最后加入如下配置：

```
# admin界面语言本地化
'django.middleware.locale.LocaleMiddleware',
```





# 三、读取数据库数据

### 1、基本查询

Customer.objects.values() 就会返回一个 QuerySet 对象，这个对象是Django 定义的，在这里它包含所有的Customer 表记录。

```python
# 导入 Customer 对象定义
from  common.models import  Customer

def listcustomers(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    # 每条表记录都是是一个dict对象，
    # key 是字段名，value 是 字段值
    qs = Customer.objects.values()

    # 定义返回字符串
    retStr = ''
    for customer in  qs:
        for name,value in customer.items():
            retStr += f'{name} : {value} | '

        # <br> 表示换行
        retStr += '<br>'

    return HttpResponse(retStr)
```

QuerySet 对象 可以使用 for 循环遍历取出里面所有的元素。每个元素 对应 一条表记录。

每条表记录元素都是一个dict对象，其中 每个元素的 key 是表字段名，value 是 该记录的字段值

上面的代码就可以将 每条记录的信息存储到字符串中 返回给 前端浏览器。

我们还需要修改路由表， 加上对 `sales/customers/` url请求的 路由。

### 2、过滤条件

精确筛选

```python
  # 根据条件筛选，例如get中是否有url条件
  phone = request.GET.get('phone',None)

  # 如果有符合条件的内容就过滤内容，没有的话就返回全部
  if phone:
      query_set = query_set.filter(phone=phone)
```



# 四、对资源的增删改查

### 1、创建 mgr应用目录

```
python manage.py startapp mgr
```

### 2、添加处理请求模块 和 url 路由

都用这个views.py 就会让这个文件非常的庞大， 不好维护。所以，我们可以用不同的 py 文件处理不同类型的http请求。

比如，这里我们可以新增一个文件 customer.py， 专门处理 客户端对 customer 数据的操作。

```python
def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST','PUT','DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)


    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_customer':
        return listcustomers(request)
    elif action == 'add_customer':
        return addcustomer(request)
    elif action == 'modify_customer':
        return modifycustomer(request)
    elif action == 'del_customer':
        return deletecustomer(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})
```

mgr下urls路由中添加

```
path('customers', customer.dispatcher),
```

### 3、增删改查函数编写

### 4、测试

```
http://localhost/api/mgr/customers?action=list_customer
```

# 五、实现登录

Django中有个内置app 名为 `django.contrib.auth` ，缺省包含在项目Installed App设置中。

这个app 的 models 定义中包含了一张 用户表，名为 `auth_user`

我们在 mgr 目录下面， 创建一个 `sign_in_out.py` 文件。

### 1、view函数实现

```python
from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout

# 登录处理
def signin( request):
    # 从 HTTP POST 请求中获取用户名、密码参数
    userName = request.POST.get('username')
    passWord = request.POST.get('password')

    # 使用 Django auth 库里面的 方法校验用户名、密码
    user = authenticate(username=userName, password=passWord)

    # 如果能找到用户，并且密码正确
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
```

### 2、创建路由

子路由中添加记录

```python
from django.urls import path
from mgr import sign_in_out

urlpatterns = [

    path('signin', sign_in_out.signin),
    path('signout', sign_in_out.signout),

]
```

### 3、测试代码

创建个test.py

```python
import  requests,pprint

payload = {
    'username': 'byhy',
    'password': '88888888'
}

response = requests.post('http://localhost:8000/api/mgr/signin',
              data=payload)

pprint.pprint(response.json())
```

# 六、session、cookie、token

session：会话，保存在服务器中

使用session机制验证用户请求的合法性 的主要缺点有两个

- 性能问题

因为，验证请求是根据sessionid 到数据库中查找session表的，而数据库操作是服务端常见的性能瓶颈，尤其是当用户量比较大的时候。

- 扩展性问题

当系统用户特别多的时候，后端处理请求的服务端通常由多个，部署在多个节点上。 但是多个节点都要访问session表，这样就要求数据库服务能够被多个节点访问，不方便切分数据库以提高性能。

最近比较流行的一种token机制可以比较好的解决这些问题。

