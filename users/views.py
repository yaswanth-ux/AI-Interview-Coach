from django.shortcuts import render, redirect
from rest_framework import generics
from .models import CustomUser
from .serializers import RegisterSerializer
from django.contrib.auth.decorators import login_required
import requests
from interview.models import Answer
from django.db.models import Sum
from .models import UserProfile
from interview.models import Answer
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.db.models import Count
from users.forms import CustomUserCreationForm 

def test(request):
    return JsonResponse({"message": "Users app working!"})


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

def register_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # optional: auto login
            return redirect('mainpage')  # use named URL
    else:
        form = CustomUserCreationForm()
        print("✅ Registration form submitted")
    return render(request, 'register.html', {'form': form})



@login_required
def profile_view(request):
    return render(request, "profile.html", {"user": request.user})


@login_required
def delete_account(request):
    user = request.user
    user.delete()
    return redirect('home')

class CustomLogoutView(LogoutView):
    template_name = 'logout_confirm.html'

def logout_confirm_view(request):
    return render(request, 'logout_confirm.html')


@login_required
def dashboard_view(request):
    user = request.user
    answers = Answer.objects.filter(user=request.user)

    # Calculate stats
    answer_count = answers.count()
    total_points = sum(a.score for a in answers)
    progress_percent = min(int((answer_count / 10) * 100), 100)

    job_role = answers.last().job_role if answer_count else 'N/A'
    round_type = answers.last().round_type if answer_count else 'N/A'

    # Leaderboard (top 5 users by points)
    leaderboard = (
    CustomUser.objects.annotate(points=Sum('answer__score'))
    .order_by('-points')[:5]
    )

    # Current user rank
    all_users = list(
    CustomUser.objects.annotate(total_points=Sum('answer__score'))
    .order_by('-total_points')
    )
    user_rank = next(
    (i + 1 for i, u in enumerate(all_users) if u.id == request.user.id),
    None
    )

    # Sample chart data
    score_data = [a.score for a in answers.order_by('created_at')]
    score_labels = [a.created_at.strftime('%b %d') for a in answers.order_by('created_at')]

    # Badges (you can customize logic)
    badges = []
    if total_points >= 50:
        badges.append('Sharp Thinker')
    if answer_count >= 10:
        badges.append('Consistent Performer')

    return render(request, 'dashboard.html', {
        'job_role': job_role,
        'round_type': round_type,
        'answer_count': answer_count,
        'total_points': total_points,
        'progress_percent': progress_percent,
        'user_rank': user_rank,
        'badges': badges,
        'score_data': score_data,
        'score_labels': score_labels,
        'leaderboard': leaderboard
    })



