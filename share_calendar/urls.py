# -*- coding: utf-8 -*-
from django.urls import path
from share_calendar import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


app_name = "share_calendar"
urlpatterns =[
        path('top_page/', views.top_page, name="top_page"),
        path('', views.share_calendar, name="calendar"),
        path('<int:year>/<int:month>/', views.share_calendar, name="calendar_year_month"),
        path('schedule_form/<str:num1>/<str:num2>/<str:num3>/', views.schedule_form, name='schedule_form'),
        path('member_form/', views.member_form, name="member_form"),
        path('sch_detail/<int:num4>/', views.sch_detail, name="sch_detail"),
        path('balloon/', views.balloon, name="balloon"),
        path('today_form/', views.today_form, name="today_form"),
        path('today_form/image/<int:num>/', views.today_image_form, name="today_image_form"),
        path('today_post/<str:num>/', views.today_post, name="today_post"),
        path('memory/', views.memory, name="memory"),
        path('memory_pic/<int:num>/', views.memory_pic, name="memory_pic"),
        path('look_pic/<int:num>/<int:ind1>/<int:ind2>/', views.look_pic, name="look_pic"),
        path('talk/', views.talk, name="talk"),
        path('talk_form/', views.talk_form, name="talk_form"),
        path('account/<int:pk>/<int:num>/', views.account, name="account"),
        path('profile_edit/<int:prof_pk>/', views.profile_edit, name="profile_edit"),
        path('follow/<int:pk>/', views.follow, name="follow"),
        path('follower/<int:pk>/', views.follower, name="follower"),
        path('talk_content/<int:num>/', views.talk_content, name="talk_content"),
        path('setting/<int:num>/', views.setting, name="setting"),
        path('login/', auth_views.LoginView.as_view(template_name='share_calendar/login.html'),\
             name='login'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
        path('a/', views.a, name="a"),
        path('add_user/', views.add_user, name="add_user"),
        ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
