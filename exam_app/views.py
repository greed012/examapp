import requests
from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import room,question, student_answer, random_str, std_details, std_mark, countdown
from django.contrib.auth.decorators import login_required,permission_required
from allauth.socialaccount.models import SocialAccount
# Create your views here.
from django.http import HttpResponse
import random
import string
import datetime
from django.views.decorators.cache import never_cache
from django.views.generic import UpdateView




def rand():
    source = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(source) for i in range(26)))
    return result_str

@never_cache
def front(request):
    request.session['phase1'] = False
    request.session['phase2'] = False

    if request.session.get('phase2_reached') == True:
        request.session['phase2_reached'] = False
        stud_data_del = std_details.objects.all()
        for i in stud_data_del:
            pass
        i.delete()

    if request.method=='POST':
        exam_code = request.POST.get('exam_code')
        name = request.POST.get('name')
        if exam_code == '' or name == '':
            return HttpResponse('<h1> You bypassed the input element validator in frontend and skipped here ha .But it is worth nothing</h1>')
        else:
            try:
                ran_data = random_str.objects.filter(random_string=exam_code)
                for i in ran_data:
                    main_id = i.rel_id

                if std_details.objects.filter(relation=room(main_id),rel_id=main_id,ran_string=exam_code, std_name=name).exists():
                    pass
                else:
                    std_data = std_details(relation=room(main_id),rel_id=main_id, ran_string=exam_code, std_name=name)
                    std_data.save()
                request.session['phase1'] = True
                return redirect('/roomview/'+str(main_id))
            except:
                return HttpResponse('<h1>You have entered some wrong room code. Please check once and try again </h1>')
    return render(request,'front.html')

@login_required(login_url='/login')
@never_cache
def index(request):
    request.session['room_data_entered'] = False
    request.session['question_entered'] = True
    if request.user.is_authenticated:
        name = request.user.id
        if request.method == 'POST':
            room_name = request.POST.get('room_name')
            noq = request.POST.get('noq')
            if room_name == '' or noq == '':
                return HttpResponse('<h1> You bypassed the input element validator in frontend and skipped here ha .But it is worth nothing</h1>')
            else:
                Room = room(room_name=room_name,no_question=noq,user_auth_id=name)
                Room.save()
                request.session['room_data_entered'] = True
                request.session['question_entered'] = False
                return redirect('/questions/')
        data2 = []
        fil_data = room.objects.filter(user_auth_id=name)

        for k in fil_data:
            if filt_data(k.id) == 0:
                k.delete()
            else:
                va = [k.id, k.room_name, k.no_question,filt_data(k.id)]
                data2.append(va)
        params = {'params':data2}
        return render(request, 'index.html',params)


def filt_data(id):
    try:
        filt = random_str.objects.filter(rel_id=id)
        for m in filt:
            pass
        return m.random_string
    except:
        return 0

@login_required(login_url='/login')
@never_cache
def questions(request):
    if request.session.get('room_data_entered') == True and request.session.get('question_entered') == False:
        value =room.objects.values('id','no_question')

        for i in value:
            pass
        noq = i['no_question']
        count = i['id']
        if request.method == 'POST':
            all = request.POST
            ques = all.getlist('question')
            option1 = all.getlist('option1')
            option2 = all.getlist('option2')
            option3 = all.getlist('option3')
            option4 = all.getlist('option4')
            answer = all.getlist('answer')
            hour = all.getlist('select1')
            minutes = all.getlist('select2')
            seconds = all.getlist('select3')
            for i in range(0,noq):
                ans_t =''
                ans = answer[i]
                if ans == '1':
                    ans_t = option1[i]
                elif ans == '2':
                    ans_t = option2[i]
                elif ans == '3':
                    ans_t = option3[i]
                elif ans == '4':
                    ans_t = option4[i]

                if ques[i] == '' or option1[i] == '' or option2 == '' or option3 == '' or option4 == '':
                    return HttpResponse(
                        '<h1> You bypassed the input element validator in frontend and skipped here ha .But it is worth nothing</h1>')
                else:

                    if question.objects.filter(relation=room(count), rel_id= count, ques=ques[i], option1=option1[i],option2=option2[i], option3=option3[i],
                                             option4=option4[i], answer=ans_t).exists():
                        pass
                    else:
                        question_save = question(relation=room(count), rel_id=count, ques=ques[i], option1=option1[i],option2=option2[i], option3=option3[i],
                                                 option4=option4[i], answer=ans_t)
                        question_save.save()

                    if random_str.objects.filter(relation=room(count),rel_id=count,random_string=rand()).exists():
                        pass
                    else:
                        random_save = random_str(relation=room(count), rel_id=count, random_string=rand())
                        random_save.save()

            d = datetime.time(int(hour[0]), int(minutes[0]), int(seconds[0]))
            d_save = countdown(relation=room(count),rel_id=count, timer=d)
            d_save.save()

            return redirect('/index')
        return render(request,'questions.html',{'range':range(1,noq+1),'hour':range(0,11),'seconds':range(0,60)})
    else:
        return HttpResponse('<h1>Hey we got a mischevious one here ha </h1>')



#FAq4l45rB0CkEOIXunQiyT5LON
@never_cache
def room_view(request, myid):
    if request.session.get('phase1') == True:
        request.session['phase2_reached'] = True
        room_data = question.objects.filter(rel_id =myid)
        stud_id = std_details.objects.filter(rel_id=myid)
        timer_data = countdown.objects.filter(rel_id= myid)
        if timer_data:
            for j in timer_data:
                hour = j.timer.hour
                minute = j.timer.minute
                second = j.timer.second
        else:
            hour = 0
            minute = 0
            second = 0
        for i in stud_id:
            stud_id = i.id
        all_data = []
        for p in room_data:
            value = [p.ques, p.option1, p.option2,p.option3, p.option4, p.answer]
            all_data.append(value)

        params = {'params': all_data, 'hour': hour,'minute': minute,'second': second}
        if request.method == 'POST':
            ans = request.POST
            count = 0
            for i in ans.getlist('answer'):
                answer = ''
                if i =='1':
                    answer = all_data[count][1]
                elif i =='2':
                    answer = all_data[count][2]
                elif i == '3':
                    answer = all_data[count][3]
                elif i =='4':
                    answer = all_data[count][4]
                count = count + 1

                if student_answer.objects.filter(relation=room(myid), rel_id=myid, student_id=stud_id, std_answer=answer).exists():
                    print("already exists")
                else:
                    data = student_answer(relation=room(myid), rel_id=myid, student_id=stud_id, std_answer=answer)
                    data.save()

                request.session['phase2'] = True
                request.session['phase2_reached'] = False
            return redirect('/ans_check/'+str(myid))
        return render(request, 'roomview.html',params)
    else:
        return render(request,'studenterror.html')

@never_cache
def ans_check(request,myid2):
    if request.session.get('phase2') == True:
        real_answer = question.objects.filter(rel_id=myid2)
        stud_id = std_details.objects.filter(rel_id=myid2)
        for i in stud_id:
            stud_id = i.id
        stud_answer = student_answer.objects.filter(student_id = stud_id)
        datas = []
        i = 0
        count = 0
        for p in real_answer:
            value = [p.ques, p.option1, p.option2, p.option3, p.option4, p.answer,stud_answer[i].std_answer]
            datas.append(value)

            if p.answer == stud_answer[i].std_answer:
                count = count+1
            i = i+1
        student_detail =std_details.objects.filter(rel_id=myid2)
        for i in student_detail:
            name = i.std_name

        if std_mark.objects.filter(relation=room(myid2),rel_id=myid2,stud_name=name,student_id=stud_id, total_ques=len(real_answer), no_correct=count).exists():
            pass
        else:
            mark_data = std_mark(relation=room(myid2), rel_id=myid2, stud_name=name, student_id=stud_id, total_ques=len(real_answer),no_correct=count)
            mark_data.save()
        request.session['phase1'] = False
        return render(request,'ans_check.html',{'params':datas, 'count':count, 'total':len(real_answer)})
    else:
        return render(request,'studenterror.html')

@login_required(login_url='/login')
@never_cache
def result_data(request,myid3):
    if request.user.id == fil_room_id(myid3):
        mark_data = std_mark.objects.filter(rel_id=myid3)
        list_data = []
        for i in mark_data:
            data = [i.rel_id,i.stud_name,i.student_id,i.total_ques,i.no_correct]
            list_data.append(data)
        return render(request,'result_data.html',{'params':list_data})
    else:
        return HttpResponse("<h1>Horizontal Privilege Escaltaion ha Better try next time bish ")

@login_required(login_url='/login')
@never_cache
def view_details(request,myid4,student_id):
    if request.user.id == fil_room_id(myid4):
        real_answer = question.objects.filter(rel_id=myid4)
        stud_answer = student_answer.objects.filter(student_id=student_id)
        stud_name = std_mark.objects.filter(student_id=student_id)
        for k in stud_name:
            s_name = k.stud_name
        datas = []
        i = 0
        count = 0
        for p in real_answer:

            value = [p.ques, p.option1, p.option2, p.option3, p.option4, p.answer, stud_answer[i].std_answer]
            datas.append(value)

            if p.answer == stud_answer[i].std_answer:
                count = count + 1
            i = i + 1

        return render(request, 'detailview.html', {'params': datas, 'count': count, 'total': len(real_answer),'name': s_name})
    else:
        return HttpResponse("<h1>Horizontal Privilege Escaltaion ha Better try next time bish ")

@never_cache
def login(request):
        return render(request,'login.html')


def fil_room_id(kid):
    a = room.objects.filter(id=kid)
    try:
        for i in a:
            b = i.user_auth_id
        return b
    except:
        return 0

def questions1(request):
    return render(request,'asdasd.html')


@login_required(login_url='/login')
@never_cache
def delete_room(request,room_id):
    room_data = room.objects.filter(id=room_id)
    for i in room_data:
        room_name = i.room_name
    if not fil_room_id(room_id) == 0:
        if request.user.id == fil_room_id(room_id):
            if request.method == 'POST':
                room_data.delete()
                return HttpResponseRedirect('/index')
        else:
            return HttpResponse('<h1>This is not your room to delete</h1>' )
    else:
        return HttpResponse('<h1>The page you are trying no longer exist</h1>')
    return render(request,'confirmdelete.html',{'name':room_name})


@login_required(login_url='/login')
@never_cache
def Editroom(request,pk):

    if request.user.id == fil_room_id(pk):
        time = countdown.objects.filter(rel_id=pk)
        for l in time:
            s_hour = l.timer.hour
            s_minute = l.timer.minute
            s_second = l.timer.second

        question_data = question.objects.filter(rel_id=pk)
        noq_data = room.objects.filter(id=pk)
        for m in noq_data:
            noq = m.no_question
        data = []
        for p in question_data:
            if p.asnwer == p.option1:
                ans = 1
            elif p.answer == p.option2:
                ans = 2
            elif p.answer == p.option3:
                ans = 3
            else:
                ans = 4

            value = [p.ques, p.option1, p.option2, p.option3, p.option4, ans]
            data.append(value)

        if request.method == 'POST':
            all = request.POST
            ques = all.getlist('question')
            option1 = all.getlist('option1')
            option2 = all.getlist('option2')
            option3 = all.getlist('option3')
            option4 = all.getlist('option4')
            answer = all.getlist('answer')
            hour = all.getlist('select1')
            minutes = all.getlist('select2')
            seconds = all.getlist('select3')

            for i in range(0, noq):
                ans_t = ''
                ans = answer[i]
                if ans == '1':
                    ans_t = option1[i]
                elif ans == '2':
                    ans_t = option2[i]
                elif ans == '3':
                    ans_t = option3[i]
                elif ans == '4':
                    ans_t = option4[i]

                if ques[i] == '' or option1[i] == '' or option2 == '' or option3 == '' or option4 == '':
                    return HttpResponse(
                        '<h1> You bypassed the input element validator in frontend and skipped here ha .But it is worth nothing</h1>')
                else:

                    if question.objects.filter(relation=room(pk), rel_id=pk, ques=ques[i], option1=option1[i],
                                               option2=option2[i], option3=option3[i],
                                               option4=option4[i], answer=ans_t).exists():
                        pass
                    else:
                        p = question_data[i]
                        p.ques = ques[i]
                        p.option1 = option1[i]
                        p.option2 = option2[i]
                        p.option3 = option3[i]
                        p.option4 = option4[i]
                        p.answer = ans_t
                        p.save()
            print(time[0])
            d = datetime.time(int(hour[0]), int(minutes[0]), int(seconds[0]))
            time[0].timer= d
            time[0].save()

            return HttpResponseRedirect('/index')
        return render(request,'update.html',{'params':data,'range':range(1,noq+1),'hour':range(0,11),'seconds':range(0,60),'s_hour':s_hour,'s_min':s_minute, 's_sec':s_second})
    else:
        return HttpResponse('<h1>You are not allowed to edit this page </h1>')
