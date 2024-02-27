from django.urls import path
from . import views

app_name = "computer_parts"
urlpatterns =[
    path("", views.home, name="home"),
    path("signup/",views.signup,name="signup"),
    path("signin/",views.signin,name="signin"),
    path("signout",views.signout,name="signout"),
    path("search/",views.search_page,name="search"),
    path("otp_verification/",views.otp_verification,name="otp_verification"),

]