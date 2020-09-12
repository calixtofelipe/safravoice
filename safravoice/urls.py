from django.urls import include, path
from rest_framework import routers

from safravoice import views
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
#router.register(r'reqbuilder', views.ReqBuilderViewSet, basename='ReqBuilder')

urlpatterns = [
    path('', include(router.urls)),
    path('get_token', obtain_auth_token),
    #path('reqbuilder_list', views.reqbuilder_list),
    path('send_transaction', views.send_transaction),
]
