from django.urls import path

from . import views

urlpatterns = [

    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('changepass/', views.user_change_pass, name='changepass'),
    path('userprofile/', views.user_profile, name='profile'),
    path('detail/<int:id>/', views.user_detail, name='detail'),
    # path('staff/', views.staff, name='stafff'),
]
