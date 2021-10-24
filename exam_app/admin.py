from django.contrib import admin
from . models import room,question, student_answer, random_str, std_details,std_mark,countdown

# Register your models here.
admin.site.register(room)
admin.site.register(question)
admin.site.register(student_answer)
admin.site.register(random_str)
admin.site.register(std_details)
admin.site.register(std_mark)
admin.site.register(countdown)
