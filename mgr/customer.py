from django.http import JsonResponse
import json

from common.models import Customer


# 定义一个函数来出来customer的get、post等请求
def customer_deal(request):
    # 将参数统一放入params中，方便后续处理
    # GET请求
    if request.method == 'GET':
        request.params = request.GET
    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        request.params = json.loads(request.body)

    # 根据不同的action分配不同的函数进行处理
    action = request.params['action']
    if action == 'list_customer':
        return list_customers(request)
    elif action == 'add_customer':
        return add_customer(request)
    elif action == 'modify_customer':
        return modify_customer(request)
    elif action == 'del_customer':
        return delete_customer(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def list_customers(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    query_set = Customer.objects.values()

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(query_set)

    return JsonResponse({'status': 0, 'retlist': retlist})


def add_customer(request):
    info = request.params['data']

    # 从请求消息中 获取要添加客户的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    record = Customer.objects.create(name=info['name'],
                                     phone=info['phone'],
                                     address=info['address'])

    return JsonResponse({'status': 0, 'id': record.id})

# 修改客户数据
def modify_customer(request):
    # 从请求消息中 获取修改客户的信息
    # 找到该客户，并且进行修改操作

    customer_id = request.params['id']
    new_data = request.params['new_data']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{customer_id}`的客户不存在'
        }

    if 'name' in new_data:
        customer.name = new_data['name']
    if 'phone' in new_data:
        customer.phone = new_data['phone']
    if 'address' in new_data:
        customer.address = new_data['address']

    # 注意，一定要执行save才能将修改信息保存到数据库
    customer.save()

    return JsonResponse({'status': 0})


# 删除客户
def delete_customer(request):
    customer_id = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{customer_id}`的客户不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    customer.delete()
    return JsonResponse({'status': 0})
