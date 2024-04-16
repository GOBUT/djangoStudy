




from django.urls import path

from mgr import customer

urlpatterns = [
    # 就表示 凡是 API 请求url为 /api/mgr/customers 的，都交由 我们上面定义的dispatch函数进行分派处理
    path('customers', customer.customer_deal),
]