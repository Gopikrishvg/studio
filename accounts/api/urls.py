from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from .views import UserListCreateView, UserLoginView, UserLogoutView

urlpatterns = [
    url(r'^obtaintoken/', obtain_jwt_token, name='token'),
    url(r'^refreshtoken/', refresh_jwt_token, name='token'),
    url(r'^verifytoken/', verify_jwt_token, name='token'),
    url(r'^user/', UserListCreateView.as_view(), name='user'),
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^logout/$', UserLogoutView.as_view(), name='logout'),
]
