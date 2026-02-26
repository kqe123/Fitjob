from django.contrib import admin
from .models import Question, Answer, Report

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Report)
# Register your models here.
