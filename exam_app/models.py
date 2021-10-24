from django.db import models

# Create your models here.
class room(models.Model):
    room_name = models.CharField(max_length=20)
    no_question = models.IntegerField()
    user_auth_id = models.IntegerField()


    def __str__(self):
        return self.room_name
class question(models.Model):
    relation = models.ForeignKey(room, on_delete=models.CASCADE)
    rel_id = models.IntegerField()
    ques = models.CharField(max_length=100)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

class student_answer(models.Model):
    relation = models.ForeignKey(room,on_delete=models.CASCADE)
    rel_id = models.IntegerField()
    student_id = models.IntegerField()
    std_answer = models.CharField(max_length=100)

class random_str(models.Model):
    relation = models.ForeignKey(room,on_delete=models.CASCADE)
    rel_id = models.IntegerField()
    random_string = models.CharField(max_length=40)

class std_details(models.Model):
    relation = models.ForeignKey(room, on_delete=models.CASCADE)
    ran_string = models.CharField(max_length=40)
    rel_id = models.IntegerField()
    std_name = models.CharField(max_length=40)

class std_mark(models.Model):
    relation = models.ForeignKey(room, on_delete=models.CASCADE)
    rel_id = models.IntegerField()
    stud_name = models.CharField(max_length=40)
    student_id = models.IntegerField()
    total_ques = models.IntegerField()
    no_correct = models.IntegerField()

class countdown(models.Model):
    relation = models.ForeignKey(room, on_delete=models.CASCADE)
    rel_id = models.IntegerField()
    timer = models.TimeField()
