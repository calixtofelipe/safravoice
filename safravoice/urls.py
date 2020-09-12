from django.urls import include, path
from rest_framework import routers

from safravoice import views

router = routers.DefaultRouter()
#router.register(r'extrato', views.reqbuilder_list)

urlpatterns = [
    path('', include(router.urls)),
    path('send_transaction', views.send_transaction),
    path('process_voice', views.process_voice),
]
