from django.http import HttpResponse

from common.models import Customer


def listorders(request):
    return HttpResponse("下面是系统中所有的订单信息。。。")

def listcustomers(request):
    '''
    返回一个QuerySet对象，包含所有的表记录
    每条记录都是一个dict对象
    key是字段名，value是字段值
    '''
    query_set = Customer.objects.values()

    # 根据条件筛选，例如get中是否有url条件
    phone = request.GET.get('phone',None)

    # 如果有符合条件的内容就过滤内容，没有的话就返回全部
    if phone:
        query_set = query_set.filter(phone=phone)

    # 定义返回字符串
    res_str = ''
    for cumtomer in query_set:
        for name,value, in cumtomer.items():
            res_str += f'{name}:{value}     |'
        # br换行
        res_str += '</br>'
    return HttpResponse(res_str)