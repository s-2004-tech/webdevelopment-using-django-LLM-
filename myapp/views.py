from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm, UploadFileForm, QuestionForm
from .models import UploadedFile, QuestionAnswerHistory
from .qa_utils import answer_document_question


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard_view')
    return render(request, 'home.html')


@login_required
def dashboard_view(request):
    uploaded_files = UploadedFile.objects.filter(user=request.user).order_by('-upload_date')
    return render(request, 'dashboard.html', {'uploaded_files': uploaded_files})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Send greeting email
            subject = "Welcome to Smart Document Q&A"
            message = f"""
Hello {user.username},

Thank you for registering with Smart Document Q&A!
You can now upload documents and ask intelligent questions.

Best regards,
SmartDoc Team
""".strip()

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            return redirect('upload')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('upload')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def upload_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.save(commit=False)
            uploaded.user = request.user
            uploaded.save()
            return redirect('ask_question_view', uploaded.id)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


@login_required
def ask_question_view(request, file_id):
    uploaded_files = UploadedFile.objects.filter(user=request.user).order_by('-upload_date')
    file = UploadedFile.objects.get(id=file_id, user=request.user)
    answer = None

    if request.method == 'POST':
        form = QuestionForm(request.POST, user=request.user)
        if form.is_valid():
            selected_file = form.cleaned_data['file_id']
            question = form.cleaned_data['question']
            answer = answer_document_question(selected_file.file.path, question)

            QuestionAnswerHistory.objects.create(
                user=request.user,
                uploaded_file=selected_file,
                question=question,
                answer=answer
            )
            file = selected_file
    else:
        form = QuestionForm(user=request.user, initial={'file_id': file.id})

    return render(request, 'ask.html', {
        'form': form,
        'file': file,
        'uploaded_files': uploaded_files,
        'answer': answer
    })


@login_required
def history_view(request):
    history = QuestionAnswerHistory.objects.filter(user=request.user).order_by('-asked_at')
    return render(request, 'history.html', {'history': history})
