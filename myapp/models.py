from django.db import models
from django.contrib.auth.models import User


class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='uploaded_files/')
    upload_date = models.DateTimeField(auto_now_add=True)
    original_filename = models.CharField(max_length=255, default="uploaded_file")
    file_type = models.CharField(max_length=20, default="txt")  # Default to 'txt'

    def __str__(self):
        return self.file.name.split('/')[-1]


class QuestionAnswerHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    question = models.TextField(default="No question provided")
    answer = models.TextField(default="Answer not generated yet")
    asked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q: {self.question[:30]}... A: {self.answer[:30]}..."
