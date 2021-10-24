from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import room,question, student_answer, random_str, std_details, std_mark
from allauth.socialaccount.models import SocialAccount
# Create your views here.
from django.http import HttpResponse
import random
import string

def rand():
    source = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(source) for i in range(26)))
    return result_str

def front(request):
    if request.method=='POST':
        exam_code = request.POST.get('exam_code')
        name = request.POST.get('name')
        print(exam_code)
        ran_data = random_str.objects.filter(random_string=exam_code)
        print(ran_data)
        for i in ran_data:
            main_id = i.rel_id
            print(main_id)
        std_data = std_details(rel_id=main_id,ran_string=exam_code, std_name=name)
        std_data.save()
        return redirect('/roomview/'+str(main_id))
    return render(request,'front.html')
def index(request):
    if request.user.is_authenticated:
        name = request.user.id
        print(name)
        if request.method == 'POST':
            room_name = request.POST.get('room_name')
            noq = request.POST.get('noq')
            Room = room(room_name=room_name,no_question=noq,user_auth_id=name)
            Room.save()
            return redirect('/questions/')
        val_1 = room.objects.values('id','room_name','no_question')
        all_data = [val_1]
        val_2 = random_str.objects.values('random_string')
        i = 0
        datas = []
        for p in val_1:
            value = [val_1[i]['id'], val_1[i]['room_name'], val_1[i]['no_question'],val_2[i]['random_string']]
            datas.append(value)
            i= i+1
        params = {'params':datas}
        return render(request, 'index.html',params)
    else:
        return HttpResponseRedirect('/login')

def questions(request):
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

            question_save = question(relation=room(count), rel_id= count, ques=ques[i], option1=option1[i],option2=option2[i], option3=option3[i],
                                 option4=option4[i], answer=ans_t)
            question_save.save()
        random_save = random_str(relation=room(count),rel_id=count,random_string=rand())
        random_save.save()
        return redirect('/index')
    return render(request,'questions.html',{'range':range(1,noq+1)})


def room_view(request, myid):
    room_data = question.objects.filter(rel_id =myid)
    stud_id = std_details.objects.filter(rel_id=myid)
    for i in stud_id:
        stud_id = i.id
    print(stud_id)
    all_data = []
    for p in room_data:
        value = [p.ques, p.option1, p.option2,p.option3, p.option4, p.answer]
        all_data.append(value)
    params = {'params': all_data}
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
            data = student_answer(relation=room(myid), rel_id=myid, student_id=stud_id, std_answer=answer)
            data.save()
        return redirect('/ans_check/'+str(myid))
    return render(request, 'roomview.html',params)

def ans_check(request,myid2):
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
    mark_data = std_mark(rel_id=myid2,stud_name=name,student_id=stud_id, total_ques=len(real_answer), no_correct=count)
    mark_data.save()
    return render(request,'ans_check.html',{'params':datas, 'count':count, 'total':len(real_answer)})


def result_data(request,myid3):
    mark_data = std_mark.objects.filter(rel_id=myid3)
    list_data = []
    for i in mark_data:
        data = [i.rel_id,i.stud_name,i.student_id,i.total_ques,i.no_correct]
        list_data.append(data)
    return render(request,'result_data.html',{'params':list_data})

def view_details(request,myid4,student_id):
    real_answer = question.objects.filter(rel_id=myid4)
    stud_answer = student_answer.objects.filter(student_id=student_id)
    datas = []
    i = 0
    count = 0
    for p in real_answer:
        value = [p.ques, p.option1, p.option2, p.option3, p.option4, p.answer, stud_answer[i].std_answer]
        datas.append(value)

        if p.answer == stud_answer[i].std_answer:
            count = count + 1
        i = i + 1
    print(datas)
    return render(request, 'detailview.html', {'params': datas, 'count': count, 'total': len(real_answer)})

def login(request):
        return render(request,'login.html')






