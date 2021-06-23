from django.contrib import admin
from django import forms
from .models import Tag, Schedule, Friend, Talk, TalkContents, Today, Member
from .models import Groupe, Favorite, Profile, Today, Today_Image, Balloon, Comment
#Register your models here.
 
class ReviewInline(admin.StackedInline):
    model = Member
    
class Schedule_Admin(admin.ModelAdmin):
    inlines = [
            ReviewInline,
            ]
    

    

admin.site.register(Tag)
admin.site.register(Schedule)
admin.site.register(Friend)
admin.site.register(Talk)
admin.site.register(TalkContents)
admin.site.register(Today)
admin.site.register(Groupe)
admin.site.register(Favorite)
admin.site.register(Member)
admin.site.register(Profile)
admin.site.register(Today_Image)
admin.site.register(Comment)
admin.site.register(Balloon)