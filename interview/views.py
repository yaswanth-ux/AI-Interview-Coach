from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from resume.models import Resume
from django.http import HttpResponse
from resume.utils import extract_resume_data
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Answer, InterviewQuestion
from django.db import models
from .utils import generate_interview_questions
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.generics import ListAPIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .serializers import AnswerSerializer
from .utils import get_resume_data
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Sum
from django.contrib.auth import get_user_model
import uuid
from django.utils.timezone import now

User = get_user_model()

def home_page(request):
    return render(request, "home.html")

class InterviewQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        round_type = request.query_params.get("round", "technical")
        job_role = request.query_params.get("job_role", "Software Developer")

        try:
            parsed_data = get_resume_data(request.user)
            questions = generate_interview_questions(parsed_data, round_type, job_role)
            return Response({
                "round": round_type,
                "job_role": job_role,
                "questions": questions
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)

@login_required
def interview_page(request):
    round_type = request.GET.get("round", "Technical")
    job_role = request.GET.get("job_role", "Software Developer")

    refresh = RefreshToken.for_user(request.user)
    return render(request, "interview.html", {
        "token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "round": round_type,
        "job_role": job_role,
        "username": request.user.username
    })


class SubmitAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        answer_text = request.data.get("answer", "").strip()

        # ❌ Block blank answers
        if not answer_text:
            return Response({"error": "You must provide an answer."}, status=400)

        data = {
            "user": request.user.id,
            "question": request.data.get("question"),
            "answer": answer_text,
            "round_type": request.data.get("round_type"),
            "job_role": request.data.get("job_role"),
            "score": request.data.get("score", 10)
        }

        serializer = AnswerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Answer saved!"})
        return Response(serializer.errors, status=400)



def select_role_page(request):
    return render(request, "select_role.html")

class UserAnswerListView(ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Answer.objects.filter(user=self.request.user).order_by('-created_at')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("🟡 Username:", username)
        print("🟡 Password:", password)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("🟢 Authenticated:", user)
            login(request, user)
            return redirect('mainpage')
        else:
            print("🔴 Authentication failed")
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

@login_required
def main_page(request):
    return render(request, 'mainpage.html')

def get_resume_data(user):
    resume = Resume.objects.filter(user=user).last()
    if not resume or not resume.extracted_text:
        raise ValueError("No resume data found")
    return extract_resume_data(resume.extracted_text)

@login_required
def dashboard_view(request):
    user = request.user
    user_answers = Answer.objects.filter(user=user).order_by('created_at')

    total_points = user_answers.aggregate(Sum('score'))['score__sum'] or 0
    progress_percent = min(100, total_points)

    score_labels = [a.created_at.strftime("%b %d") for a in user_answers]
    score_data = [a.score for a in user_answers]

    leaderboard_qs = (
        User.objects.annotate(points=Sum('answer__score'))
        .filter(points__gt=0)
        .order_by('-points')
    )

    user_rank = next(
        (i + 1 for i, entry in enumerate(leaderboard_qs) if entry.username == user.username),
        None
    )

    context = {
        "progress_percent": progress_percent,
        "total_points": total_points,
        "user_rank": user_rank,
        "score_labels": score_labels,
        "score_data": score_data,
        "leaderboard": leaderboard_qs,
    }

    return render(request, "dashboard.html", context)



@login_required
def performance_analysis_view(request):
    user = request.user
    submitted_after = request.GET.get('submitted_after')

    if submitted_after:
        try:
            submitted_after_cleaned = submitted_after.split('.')[0]  # Remove milliseconds
            dt = parse_datetime(submitted_after_cleaned)
            if dt is None:
                return HttpResponse("Invalid timestamp", status=400)
            submitted_after_dt = make_aware(dt)
            answers = Answer.objects.filter(user=user, created_at__gte=submitted_after_dt)
        except Exception as e:
            return HttpResponse(f"Timestamp parse error: {e}", status=400)
    else:
        answers = Answer.objects.filter(user=user)

    total = answers.count()
    total_score = sum(answer.score for answer in answers)

    suggestions = []
    if total == 0:
        suggestions.append("You didn’t answer any questions.")
    elif total_score / total < 6:
        suggestions.append("Work on your weak areas.")
    else:
        suggestions.append("Good job! Keep practicing.")

    return render(request, "performance_analysis.html", {
        "total": total,
        "score": total_score,
        "suggestions": suggestions
    })

@login_required
def user_answers_view(request):
    answers = Answer.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_answers.html', {"answers": answers})

@login_required
def my_answers_view(request):
    user_answers = Answer.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_answers.html', {'answers': user_answers})


def generate_session_id():
    return str(uuid.uuid4())