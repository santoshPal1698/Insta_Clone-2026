from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from social import views
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.shortcuts import render,redirect

from django.urls import path ,include ,reverse_lazy
# from loginuser import views

# from django.urls reverse_lazy


urlpatterns = [ 

    path('home/', views.HomeView.as_view(), name='home'),
    # path('about/', views.AboutView.as_view(),name='about'),
    path('register/',views.register,name='register'),
    path('activate/<uidb64>/<token>/',views.activate_account,name='activate'),
    path('confirm/',views.confirm,name='confirm'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('updateprofile/',views.updateprofile,name='updateprofile'),
    # path('contact/', views.contact, name='contact'),
    path('profile/edit/<int:pk>', views.MyProfileUpdateView.as_view(success_url="/social/home")),
    path('mypost/create/', views.MyPostCreate.as_view(success_url="/social/mypost")),
    path('mypost/delete/<int:pk>', views.MyPostDeleteView.as_view(success_url="/social/mypost")),
    path('mypost/', views.MyPostListView.as_view()),
    path('mypost/<int:pk>', views.myPostDetail),
    path('mypost/like/<int:pk>', views.like),
    path('mypost/unlike/<int:pk>', views.unlike),
    path('mypost/comment/<int:pk>', views.comment),
    path('myprofile/', views.MyProfileListView.as_view()),
    path('myprofile/<int:pk>', views.MyProfileDetailView.as_view()),
    path('myprofile/follow/<int:pk>', views.follow),
    path('myprofile/unfollow/<int:pk>', views.unfollow),

    path('', RedirectView.as_view(url="login/")),
    path('change_password/',
        auth_views.PasswordChangeView.as_view(
            template_name='reset_password/change_password.html',
            success_url = '/'
        ),
        name='change_password'
    ),  
    # passwordreset
    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name='reset_password/reset_page.html'),
    name='reset_password'),
      # Email  send success message url
    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name='reset_password/password_reset_sent.html'),
    name='password_reset_done'),
    # Link to password Reset form in email
    path('reset_password/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='reset_password/reset_password_form.html'),
    name='password_reset_confirm'),  
    # Passwrod successfully changed message
    path('reset_password_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='reset_password/reset_password_done.html'),
    name='password_reset_complete'),

    # path('mylist/', views.MyList.as_view()),
    # path('profile/edit/<int:pk>', views.ProfileUpdateView.as_view(success_url="/college/home")),

]

