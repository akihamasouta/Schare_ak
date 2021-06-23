from django.shortcuts import render, redirect
import calendar
import datetime, re
from share_calendar.models import User, Schedule, Today, Talk, TalkContents, Member, Friend, Profile, Favorite, Today_Image, Comment, Balloon
from share_calendar.forms import Schedule_Form, Today_Form, Member_Form, Talk_Form, Goot_Form, Comment_Form
from share_calendar.forms import Talk_Content_Form, Today_Image_Form, Year_Month_Form, Profile_Form, User_Form
from share_calendar.forms import Formset
from django import forms
from functools import reduce
from django.core.validators import ValidationError
from datetime import timedelta
import itertools
from django.db.models import Q
from django.contrib.auth.models import User
# Create your views here.

def daterange(value, arg):
    date_list = []
    for n in range((arg - value).days):
        date_list.append(value + timedelta(n))
    if not date_list:
        return None
    return date_list

def make_nest(list_name, num):
    data_list = []
    data_nest = []       
    if list_name:
        count2 = 0
        for item in list_name:
            data_list.append(item)
            count2 += 1
            if count2 == num:
                data_nest.append(data_list)
                data_list = []
                count2 = 0
            elif item == list_name[-1]:
                data_nest.append(data_list)
    return data_nest

def get_month_dates(year, month):
    c = calendar.Calendar()
    days = c.monthdatescalendar(year, month)
    list_days = list(itertools.chain.from_iterable(days))
    month_dates = []
    for item in list_days:
        if item.month == month:
            month_dates.append(item)
    return month_dates

def get_schedule_list(request):
    login_user = request.user
    my_schedule = Schedule.objects.filter(author=login_user)
    friends = Friend.objects.filter(my_account=login_user)
    friends_sch = []
    my_sch = []
    
    for item in friends:    #kueriwosonomamaappenddekinakattanodenikainiwaketa
        friends_schedule = Schedule.objects.filter(author=item.friend)
        for item2 in friends_schedule:
            friends_sch.append(item2)
    for item in my_schedule:
        my_sch.append(item)
    
    month_schedule_list = my_sch + friends_sch    
    return month_schedule_list

def share_calendar(request, year=0  , month=0):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        
        bal_list = []
        if Schedule.objects.filter(author=request.user):
            for item in Schedule.objects.filter(author=request.user):
                if item.balloon_set.all():
                    balloon = item.balloon_set.all()
                    for bal in balloon:
                        bal_list.append(bal)
                        
        
        today = datetime.date.today()
        if year==0 and month==0:
            get_year = today.year
            get_month = today.month
            month_dates = get_month_dates(get_year, get_month)
        else:
            get_year = year
            get_month = month
            month_dates = get_month_dates(get_year, get_month)
        
        form = Year_Month_Form(request.POST or None, initial={"year":get_year, "month":get_month})
        
        display_sch = get_schedule_list(request)
        
        if request.method=="POST":
            if form.is_valid() and 'search' in request.POST:
                year = int(request.POST['year'])
                month = int(request.POST['month'])
                return redirect(to=str(year)+"/"+str(month)+"/")
            
            pk_list = [item.pk for item in display_sch]
            for pk in pk_list:
                if str(pk) in request.POST:
                    schedule = Schedule.objects.get(pk=pk)
                    bal = Balloon(schedule=schedule, join_user=request.user)
                    bal.save()
                    if request.path == '/share_calendar/':
                        return redirect(to='share_calendar:calendar')
                        
                    else:
                        return redirect(to='../../'+str(year)+"/"+str(month)+"/")
        
        ballooned = Balloon.objects.filter(join_user=request.user)
        today_new = today.strftime("%Y-%m-%d")
        num = year
        day_of_the_week = ["(日)","(月)","(火)","(水)","(木)","(金)","(土)"]
        params = {
            "data":month_dates,
            "share_sch":display_sch,
            "login_user":request.user,
            "form":form,
            "num": num,
            "month":get_month,
            "today": today_new,
            "ori_today":today,
            "balloon": bal_list,
            "ballooned": ballooned,
            "week":day_of_the_week,
            }
        
    return render(request, "share_calendar/index.html", params)

def memory(request,year=0,month=0):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        today = datetime.date.today()
            
        display_sch = get_schedule_list(request)
    
        data = []
        count = 0
        for item in display_sch:
            if Today.objects.filter(sc_title=item):
                data.append(Today.objects.get(sc_title=item))
                count += 1
        change = True
        while change:
            change = False
            for i in range(len(data) - 1):
                if data[i].sc_title.selected_date < data[i + 1].sc_title.selected_date:
                    data[i], data[i + 1] = data[i + 1], data[i]
                    change = True
            
        display_today_sch = []
        for what_day in data:
            try:                
                for date in daterange(what_day.sc_title.selected_date,what_day.sc_title.end_day):
                    if date == today:
                        display_today_sch.append(what_day)
            except:
                if what_day.sc_title.selected_date == today:
                    display_today_sch.append(what_day)
                continue
            if what_day.sc_title.end_day == today:
                display_today_sch.append(what_day)
             
        display_today = []
        for item in display_today_sch:
            if Today.objects.filter(sc_title=item.sc_title):
                display_today.append(Today.objects.get(sc_title=item.sc_title))
        
        data_nest = make_nest(data, 4)
        mobile_data_nest = make_nest(data,3)
        today_new = today.strftime("%Y/%m/%d")
        
       
            
                    
        params = {
                "login_user":request.user,
                "data_nest":data_nest,
                "display_sch": display_sch,
                "display_today": display_today,
                "today":today_new,
                "mobile_data_nest":mobile_data_nest,
                }
    return render(request, 'share_calendar/index_memory.html', params)

def memory_pic(request, num):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        main_pic = Today.objects.get(pk=num)
        schedule = main_pic.sc_title
        pictures_objcts = main_pic.today_image_set.all()
        pictures = [ picture_obj for picture_obj in pictures_objcts]
        pictures_nest = make_nest(pictures, 4)
        
        params = {
                "request":request,
                "schedule":schedule,
                "pictures":pictures_nest,
                "main_pic": main_pic,
                "num":num,
                }
    return render(request, 'share_calendar/memory_pic.html', params)

def look_pic(request, num, ind1=0, ind2=0):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        main_pic = Today.objects.get(pk=num)
        schedule = main_pic.sc_title
        pictures_objcts = main_pic.today_image_set.all()
        pictures = [ picture_obj for picture_obj in pictures_objcts]
        pictures_nest = make_nest(pictures, 4)
        
        if pictures_nest[ind1][ind2] == pictures_nest[-1][-1]:
            end_ind = True
        else:
            end_ind = False
        
        params = {
                "schedule":schedule,
                "pictures":pictures,
                "picture":pictures_nest[ind1][ind2],
                "main_pic": main_pic,
                "num":num,
                "ind1":ind1, 
                "ind2": ind2,
                "end_ind":end_ind,
                }
    
    return render(request, 'share_calendar/look_pic.html', params)

def top_page(request):
    return render(request, 'share_calendar/top_page.html')



def schedule_form(request, num1, num2, num3):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        form = Schedule_Form(request.POST or None, initial={
                "selected_date":str(num1)+"-"+str(num2)+"-"+str(num3),
                "end_day":str(num1)+"-"+str(num2)+"-"+str(num3),
                "author":request.user.id})
        params = {
                "form":form,
                "day_error":"",
                "time_error":"",
                "num1":num1,
                "num2":num2,
                  }
        if request.method == "POST":
            s_year = int(request.POST['selected_date_year'])
            s_month = int(request.POST['selected_date_month'])
            s_day = int(request.POST['selected_date_day'])
            e_year = int(request.POST['end_day_year'])
            e_month = int(request.POST['end_day_month'])
            e_day = int(request.POST['end_day_day'])
            start_time = str(request.POST['start_time'])
            end_time = str(request.POST['end_time'])
            striped_time = start_time.replace(':', '0')
            striped_end_time = end_time.replace(':', '0')
            try:
                selected_date = datetime.date(s_year, s_month, s_day)
                end_day = datetime.date(e_year,  e_month, e_day)
                
                if  selected_date > end_day:
                    params["day_error"] = "正しい日付を入力してください"
                elif selected_date == end_day:
                    if striped_time and striped_end_time:
                        if int(striped_time) >= int(striped_end_time) or len(striped_time) != 5 or len(striped_end_time) != 5:
                            params["time_error"] = "正しい時間を入力してください"
                        else:
                            schedule = form.save(commit=False)
                            schedule.author = request.user
                            schedule.save()
                            return redirect(to="share_calendar:member_form")
                    elif form.is_valid():
                        schedule = form.save(commit=False)
                        schedule.author = request.user
                        schedule.save()
                        return redirect(to="share_calendar:member_form")
                        
                elif form.is_valid():
                    schedule = form.save(commit=False)
                    schedule.author = request.user
                    schedule.save()
                    return redirect(to="share_calendar:member_form")
            except:
                params['day_error'] = "存在しない日付日時です"
    return render(request, 'share_calendar/schedule_form.html', params)
            
        

def member_form(request):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        user = request.user
        obj = Member()
        friends = Friend.objects.filter(my_account=user)
        friends_name_list = [item.friend for item in friends]
        user_select = User.objects.filter(username__in=friends_name_list) #リストを渡すための__in
        latest_schedule = Schedule.objects.filter(author=user).first()
        form = Member_Form(request.POST or None, initial={
                "schedule":latest_schedule}, instance=obj
            )
        
        form.fields['member'].widget = forms.CheckboxSelectMultiple()
        form.fields['member'].queryset = user_select#donokuerisetwowidgetnosenntakusinisuruka
        if request.method == "POST" and form.is_valid():
            form.save()
            return redirect(to="share_calendar:calendar")
            
        params = {
                'form':form,
                "ta":"ka",
                }
    return render(request, 'share_calendar/member_form.html', params)


def sch_detail(request, num4):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        num4 = int(num4)
        data = Schedule.objects.get(pk=num4)
        obj = Favorite()
        comment_obj = Comment()
        user = User.objects.get(username=request.user)
        form = Goot_Form(request.POST or None, instance=obj, \
                         initial={"schedule":data, "good":True, "user":user})
        comment_form = Comment_Form(request.POST or None, instance=comment_obj,\
                                    initial={"author":request.user, "schedule":data})
        
        comment = Comment.objects.filter(schedule=data)
        if Favorite.objects.filter(user=user,schedule=data): #getは値がないことを許さないからあえてfilter
           favorite = Favorite.objects.get(user=user,schedule=data)
        else:
            favorite = False
            
        if request.method=="POST":
            if 'heart_button' in request.POST and form.is_valid():
                if favorite:
                    favorite.delete()
                    favorite = False
                else:
                    form.save()
                    favorite = True
                return redirect(to='../../sch_detail/'+str(num4))
            if 'comment_button' in request.POST and comment_form.is_valid():
                comment_form.save()
                return redirect(to='../../sch_detail/'+str(num4))
                
        try:
            member = data.member_sch
            members = member.member.all()
        except:
            members = ""
        count = Favorite.objects.filter(schedule=data).count()
        params={
                "data":data,
                "comment":comment,
                "member": members,
                "form": form,
                "favorite":favorite,
                "count":count,
                "comment_form":comment_form,
                }
    return render(request, 'share_calendar/sch_detail.html', params)

def balloon(request):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        bal_list = []
        if Schedule.objects.filter(author=request.user):
            for item in Schedule.objects.filter(author=request.user):
                if item.balloon_set.all():
                    balloon = item.balloon_set.all()
                    for bal in balloon:
                        bal_list.append(bal)
                        
        if bal_list:  
            if request.method == "POST":
                pk_list =[item.pk for item in bal_list]
                for pk in pk_list:
                    if 'delete'+str(pk) in request.POST:
                        balloon = Balloon.objects.get(pk=pk)
                        balloon.delete()
                        return redirect(to="../balloon/")
                    
                    elif 'ok'+str(pk) in request.POST:
                        join_user = Balloon.objects.get(pk=pk).join_user
                        schedule = Balloon.objects.get(pk=pk).schedule
                        balloon = Balloon.objects.get(pk=pk)
    
                        if Member.objects.filter(schedule=schedule):
                            member_obj = Member.objects.get(schedule=schedule)
                            member_obj.member.add(join_user)
                            balloon.delete()
                            return redirect(to="../balloon/")
                        else:
                            cre_member = Member(schedule=schedule)
                            cre_member.save()
                            cre_member.member.add(join_user)
                            balloon.delete()
                            return redirect(to="../balloon/")
                        
    
            
        params = {
                "bal_list":bal_list,
                }
    return render(request, 'share_calendar/balloon.html', params)

def today_form(request):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        obj = Today()
        today = datetime.date.today()
        user1 = User.objects.get(username=request.user) 
        today_form = Today_Form(request.POST or None, request.FILES or None, instance=obj)
        can_select = user1.author
        today_form.fields['sc_title'].queryset = can_select
        
        params = {
                "data":Today.objects.all(),
                "form":today_form,
                "login_user":request.user,
                "sch_user":user1.author.filter(selected_date=today),
                "error":""
                }
        if request.method == "POST":
            if today_form.is_valid():
                today_form.save()
                num = Today.objects.get(sc_title=request.POST['sc_title']).pk
                return redirect(to="image/"+str(num)+"/")
            elif Today.objects.filter(sc_title=request.POST['sc_title']):
                params['error'] = "既に存在します"
            else:
                params['error'] = "入力された値が正しくないです"
            

    return render(request, "share_calendar/today_form.html", params)

def today_image_form(request, num):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        instance = Today_Image()
        form = Today_Image_Form(request.POST or None ,request.FILES or None, instance=instance, initial={'today':Today.objects.get(pk=num)})
        params = {
                "form": form,
                }
        if request.method == "POST":
            images = request.FILES.getlist('image', False)
            today = int(request.POST['today'])
            if len(images) <= 100:
                if form.is_valid():
                    for image in images:
                        images_instance = Today_Image(image=image, today=Today.objects.get(pk=today))
                        images_instance.save()
                return redirect(to="share_calendar:memory")
            else:
                params = {
                    "form": form,
                    "error":"写真枚数が100枚を超えています"
                        }
                return redirect(to=request.build_absolute_uri())
                    
                
    return render(request, 'share_calendar/today_image_form.html', params)

def today_post(request,num):
    params = {
            }
    return render(request, 'share_calendar/today_post.html', params)

def talk(request):
    user1 = User.objects.get(username=request.user)
    member_obj = user1.member_set.all()
    for_data1 = [Schedule.objects.get(title=item.schedule) for item in member_obj]
    data1 = [item for item in for_data1]
    author_sch = Schedule.objects.filter(author=user1)
    data2 = [item for item in author_sch]
    data3 = data1 + data2
    data = Talk.objects.filter(schedule__in=data3)
    params = {
            'talk_title':data,
            "login_user":request.user,
            "f":User.objects.get(id=1).id,
            "b": User.objects.filter(id=1),
            }
    return render(request, "share_calendar/talk.html", params)

def talk_form(request):
    join_sch = Schedule.objects.filter(author=request.user)
    obj = Talk()
    form = Talk_Form(request.POST or None,request.FILES or None, instance=obj)
    form.fields['schedule'].queryset = join_sch
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(to="../talk")
    params = {
            "form":form,
            }
    return render(request, 'share_calendar/talk_form.html', params)

def talk_content(request, num):
    talk1 = Talk.objects.get(id=num)
    talk_contents = talk1.talkcontents_set.all() #逆参照
    obj = TalkContents()
    form = Talk_Content_Form(request.POST or None, initial={
            "talk":talk1, "author":request.user}, instance=obj)
    if request.method=="POST" and form.is_valid():
        form.save()
        return redirect(to="../"+str(num)+"/")
    params = {
            "data":talk_contents,
            "talk":talk1,
            "login_user":request.user.username, 
            "form":form,
            }  
 
    return render(request, "share_calendar/talk_content.html", params)


def account(request, pk=0, num=0):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        datetime_list = []
        new_datetime_list = []
        can_follow = False
        mobile_data = []
        if pk != 0:
            visit_user = User.objects.get(pk=pk)
            visit_user_profile = Profile.objects.filter(user=visit_user)
            follow = visit_user.my_account.all()
            follower = visit_user.for_friend.all()
            if not request.user.my_account.filter(friend=visit_user):
                can_follow = True
            if num == 0:
                schedule = visit_user.author.all().order_by('selected_date').reverse()
                display_list = []
                for item in schedule:
                    if Today.objects.filter(sc_title=item):
                        display_list.append(Today.objects.get(sc_title=item))
                data = make_nest(display_list, 4)
                mobile_data = make_nest(display_list,3)
            elif num == 1:
                data = Schedule.objects.filter(author=visit_user).order_by('selected_date').reverse()
                for item in data:
                    if item.end_day and item.selected_date!=item.end_day:
                        for time in daterange(item.selected_date, item.end_day):
                            datetime_list.append(time)
                    datetime_list.append(item.selected_date)
                    datetime_list.append(item.end_day)
                new_datetime_list = sorted(list(set(datetime_list)), reverse=True)
            elif num == 2:
                favorite = visit_user.favorite_set.all()
                data = [item.schedule for item in favorite]
                for item in data:
                    if item.end_day and item.selected_date!=item.end_day:
                        for time in daterange(item.selected_date, item.end_day):
                            datetime_list.append(time)
                    datetime_list.append(item.selected_date)
                    datetime_list.append(item.end_day)
                new_datetime_list = sorted(list(set(datetime_list)), reverse=True)
        else:
            visit_user = request.user
            visit_user_profile = Profile.objects.filter(user=visit_user)
            follow = visit_user.my_account.all()
            follower = visit_user.for_friend.all()
            if num == 0:
                schedule = visit_user.author.all().order_by('selected_date').reverse()
                display_list = []
                for item in schedule:
                    if Today.objects.filter(sc_title=item):
                        display_list.append(Today.objects.get(sc_title=item))
                data =make_nest(display_list, 4)
                mobile_data = make_nest(display_list,3)
            elif num == 1:
                data = Schedule.objects.filter(author=visit_user).order_by('selected_date')
                for item in data:
                    if item.end_day and item.selected_date!=item.end_day:
                        for time in daterange(item.selected_date, item.end_day):
                            datetime_list.append(time)
                    datetime_list.append(item.selected_date)
                    datetime_list.append(item.end_day)
                new_datetime_list = sorted(list(set(datetime_list)), reverse=True)
            elif num == 2:
                favorite = visit_user.favorite_set.all()
                data = [item.schedule for item in favorite]
                for item in data:
                    if item.end_day and item.selected_date!=item.end_day:
                        for time in daterange(item.selected_date, item.end_day):
                            datetime_list.append(time)
                    datetime_list.append(item.selected_date)
                    datetime_list.append(item.end_day)
                new_datetime_list = sorted(list(set(datetime_list)), reverse=True)
                
        ballooned = Balloon.objects.filter(join_user=request.user)
        day_of_the_week = ["(日)","(月)","(火)","(水)","(木)","(金)","(土)"]
    
        
        if request.method == "POST":
            if 'follow' in request.POST:
                if not request.user.my_account.filter(friend=visit_user):
                    obj = Friend(my_account=request.user, friend=visit_user)
                    obj.save()
                    return redirect(to="../"+str(num)+"/")
                else:
                    obj = Friend.objects.get(my_account=request.user, friend=visit_user)
                    obj.delete()
                    return redirect(to="../"+str(num)+"/")
            else:
                pk_list = [item.pk for item in data]
                for pk in pk_list:
                    if str(pk) in request.POST:
                        schedule = Schedule.objects.get(pk=pk)
                        bal = Balloon(schedule=schedule, join_user=request.user)
                        bal.save()
                        return redirect(to="../"+str(num)+"/")
        
                
        params = {
                "visit_user":visit_user,
                "visit_user_profile":visit_user_profile,
                "follow": follow,
                "follower": follower,
                "data": data,
                "pk": pk,
                "num": num,
                "datetime_list": new_datetime_list,
                "can_follow": can_follow,
                "ori_today": datetime.date.today(),
                "share_sch":get_schedule_list(request),
                "login_user":request.user,
                "ballooned": ballooned,
                "week":day_of_the_week,
                "mobile_data":mobile_data,
                }
    return render(request, "share_calendar/account.html", params)

def profile_edit(request,prof_pk):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        if prof_pk == 0:
            obj = Profile()
            form = Profile_Form(request.POST or None, request.FILES or None,initial={'user':request.user},instance=obj)
        else:
                
            obj = Profile.objects.get(pk=prof_pk)
            form = Profile_Form(request.POST or None,request.FILES or None, initial={'user':request.user}, instance=obj)  
            
        if request.method == "POST" and form.is_valid():
            form.save()
            return redirect(to="../../account/0/0/")
        params = {
                "form":form,
                "pk": prof_pk,
                }
    return render(request, 'share_calendar/profile_edit.html', params)

def follow(request, pk):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        visit_user = User.objects.get(pk=pk)
        follow = visit_user.my_account.all()
        params = {
                "follow":follow,
                "pk":pk,
                "visit_user": visit_user,
                }
    return render(request, 'share_calendar/follow.html', params)

def add_user(request):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        obj = User()
        form = User_Form(request.POST or None,instance=obj)
        if request.method == "POST" and form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
        
            #  Use set_password here
            user.set_password(password)
            user.save()
            return redirect(to="share_calendar:login")
        
        params = {
                "form":form,
                }
        
    return render(request, 'share_calendar/add_user.html', params)

def setting(request,num):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        params = {"user_names":"",
                  }
        if request.method=="POST":
            user_name = request.POST['user_name']
            if User.objects.filter(username=user_name):
                params["user_names"] = User.objects.filter(username=user_name)
            else:
                params["user_names"] = None
                    
                    
        
    
    return render(request, 'share_calendar/setting.html', params)
def follower(request, pk):
    params = {}
    if request.user.is_active and request.user.is_authenticated:
        visit_user = User.objects.get(pk=pk)
        follower = visit_user.for_friend.all()
        
            
            
        params = {
                "follower":follower,
                "pk":pk,
                "visit_user": visit_user,
                "request_user": request.user,
                }
    return render(request, 'share_calendar/follower.html',params)

from django.shortcuts import resolve_url

def a(request):
    top_page = resolve_url('share_calendar:calendar')
    referer = request.environ.get('HTTP_REFERER')  #前ページのURL
    host_url =  "{0}://{1}".format(request.scheme, request.get_host())
    now_page_url = request.build_absolute_uri()
    
    
    memory_pic_url = resolve_url('share_calendar:memory_pic'+'/'+'0')
    num_list = re.findall(r'\d+', now_page_url)
    memory_pic_num = str(num_list[-1])
    memory_pic_url = "{0}://{1}/{2}/{3}/".format(request.scheme, request.get_host(),'share_calendar/memory_pic',memory_pic_num)
    
    num2_list = re.findall(r'\d+', str(referer)) 
    look_pic_url = False
    if len(num2_list) >=3:
        look_pic_num1 = str(num2_list[-1])
        look_pic_num2 = str(num2_list[-2])
        look_pic_num3 = str(num2_list[-3])
        look_pic_url = "{0}://{1}/{2}/{3}/{4}/{5}/".format(request.scheme, request.get_host(),'share_calendar/memory_pic',look_pic_num1,look_pic_num2,look_pic_num3)
    
    params = {
            "request":request,
            "a":str(referer),
            "b":referer,
            "c":str(now_page_url),
            "d":str(look_pic_url),
            }
    return render(request, "share_calendar/a.html", params)