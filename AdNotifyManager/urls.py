from django.urls import path

from AdNotifyManager.views import TokenView, QueryLinkView
from AdNotifyManager.views.goods_view import GoodsView

app_name = "AdNotifyManager"

# app_name will help us do a reverse look-up latter.
urlpatterns = [

    path('token/', TokenView.as_view()),
    path('goods/', GoodsView.as_view()),
    path('link/', QueryLinkView.as_view()),
]
