from django import forms
import datetime
from django.contrib.auth.models import User
from share_calendar.models import Schedule, Member, Today, Tag, Talk, Favorite, TalkContents, Today_Image, Comment, Profile
# -*- coding: utf-8 -*-

class User_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
    
 

class Schedule_Form(forms.ModelForm):
    today_year = datetime.date.today().year
    selected_date = forms.DateField(widget=forms.SelectDateWidget(
                    years = {today_year-1:today_year-1, today_year:today_year, today_year+1: today_year +1},
                    months ={ 1: '1', 2: '2', 3: '3', 4: '4',
                             5: '5', 6: '6', 7: '7', 8: '8',
                             9: '9', 10: '10', 11: '11', 12: '12'}))
    end_day= forms.DateField(widget=forms.SelectDateWidget(
                    years = {today_year-1:today_year-1, today_year:today_year, today_year+1: today_year +1},
                    months ={ 1: '1', 2: '2', 3: '3', 4: '4',
                             5: '5', 6: '6', 7: '7', 8: '8',
                             9: '9', 10: '10', 11: '11', 12: '12'}))
    
        
    class Meta:
        model = Schedule
        fields =("title", "selected_date", "tag", "start_time", "end_day", "end_time")
    

class Member_Form(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('member',"schedule")
    
        
class Today_Form(forms.ModelForm):
    sc_title = forms.ModelChoiceField(label="sc_title",queryset=Schedule.objects.all())
    class Meta:
        model = Today
        fields = "__all__"
        
class Today_Image_Form(forms.ModelForm):
    image = forms.ImageField(
    widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )
    class Meta:
        model = Today_Image
        fields = "__all__"
        
class Talk_Form(forms.ModelForm):
    schedule = forms.ModelChoiceField(queryset=Schedule.objects.none())
    class Meta:
        model = Talk
        fields = "__all__"
    

class Goot_Form(forms.ModelForm):
    good = forms.BooleanField(required=False) 
    class Meta:
        model = Favorite
        fields = ("schedule", "user", "good")
    
    
class Talk_Content_Form(forms.ModelForm):
    class Meta:
        model = TalkContents
        fields = "__all__"
    
class Year_Month_Form(forms.Form):
    today_year = datetime.date.today().year
    year = forms.ChoiceField(choices=[(today_year-1, today_year-1),(today_year, today_year),(today_year+1, today_year+1)])
    month = forms.ChoiceField(choices=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)],\
                                       initial={})
    
class Comment_Form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
    
class Profile_Form(forms.ModelForm):
    icon = forms.ImageField(widget=forms.FileInput,  required=False)
    class Meta:
        model = Profile
        fields = "__all__"
    
    
        
    
Formset = forms.inlineformset_factory(Schedule, Member, fields='__all__', \
                                      extra=10,)    