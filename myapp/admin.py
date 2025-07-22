from django.contrib import admin
from .models import UploadedFile, QuestionAnswerHistory

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_filename', 'file_type', 'upload_date', 'user')

@admin.register(QuestionAnswerHistory)
class QuestionAnswerHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'uploaded_file', 'question', 'answer', 'asked_at')
