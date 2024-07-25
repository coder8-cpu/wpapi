from django.urls import path
from api_wp.views import *
obj = EstablishConnection()

urlpatterns = [
    # path('qr-code/', display_qr_code, name='qr_code'),
    path('qr-code/', obj.render_qr,),
    path('send-message/<phonenumber>/<message>/', obj.send_message,),
]
