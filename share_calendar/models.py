from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here

class Tag(models.Model):
    name = models.CharField(max_length=15)
    tag_color = models.IntegerField()

    def __str__(self):
        return self.name


class Schedule(models.Model):
    title = models.CharField(max_length=25)
    date = models.DateTimeField(auto_now_add=True)
    selected_date = models.DateField(null=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT,\
related_name="author") #onetooneだと違うscheduleに同じauthorを登録できない
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL,\
                                  null=True, blank=True)
    good_count = models.IntegerField(default=0,null=False, blank=False)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    end_day = models.DateField(null=True, blank=True)
    
    

    def __str__(self):
        return str(self.title)
   
    class Meta:
        ordering = ('-date',)



class Friend(models.Model):
    my_account = models.ForeignKey(User, on_delete=models.CASCADE,\
                                   related_name="my_account")
    friend = models.ForeignKey(User, on_delete=models.CASCADE,\
                              related_name="for_friend")
    
    def __str__(self):
        return str(self.friend)+"_____"+str(self.my_account)

class Member(models.Model):
    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE, related_name="member_sch")
    member = models.ManyToManyField(User, blank=True)
    
    def __str__(self):
        return str(self.member)
    
    
class Talk(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="talk_icon", default="")
    def __str__(self):
        return str(self.schedule)


class TalkContents(models.Model):
    talk = models.ForeignKey(Talk, on_delete=models.CASCADE)
    talk_content = models.TextField(max_length=1000, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,\
                               null=True)


    def __str__(self):
        return str(self.talk_content)
   
    class Meta:
        ordering = ('date_time',)

class Today(models.Model):
    main_pic = models.ImageField(upload_to='photos')
    sc_title = models.OneToOneField(Schedule, on_delete=models.CASCADE,null=True\
                                 ,blank=True)

    def __str__(self):
        return str(self.sc_title)

class Today_Image(models.Model):
    image = models.ImageField(upload_to='photos')
    today = models.ForeignKey(Today, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.today)

class Groupe(models.Model):
    name = models.CharField(max_length=15)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='photos')

    def __str__(self):
        return

class Favorite(models.Model):
    good = models.BooleanField(default=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='icon')
    prof = models.TextField(max_length=200, null=True, blank=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=500)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    

class Balloon(models.Model):
    join_user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

class Visibillity(models.Model):
    groupe_name = models.CharField(max_length=20)
    author = models.ForeignKey(User,related_name="visibillity_author",on_delete=models.CASCADE)
    visible_user = models.ManyToManyField(User, related_name="visibillity_user")
    
    


