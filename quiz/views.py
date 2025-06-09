
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from .models import *
from .forms import SignUpForm, LoginForm
from django.db.models import Sum
from django.contrib.auth import login as auth_login
from django.contrib.auth.backends import ModelBackend
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
import hashlib
from hashlib import md5
from urllib.parse import urlencode


@csrf_exempt
@csrf_protect
# def login(request):
#     # Redirect if already logged in
#     if request.user.is_authenticated:
#         return redirect('home')
#     return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            #login(request, user)
            auth_login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
               #login(request, user)
                auth_login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

"""@login_required
def home(request):
    try:
        user = request.user
        social_auth = user.social_auth.get(provider='instagram')
        access_token = social_auth.extra_data['access_token']
        
        # Add Instagram profile data to context
        profile_data = {
            'username': social_auth.extra_data.get('username'),
            'profile_pic': social_auth.extra_data.get('profile_picture')
        }
        
        return render(request, 'home.html', {
            'user': user,
            'profile': profile_data
        })
        
    except Exception as e:
        messages.error(request, "Failed to fetch Instagram data")
        return redirect('login')"""
    
def home(request):
    return render(request,'home.html')

# def logout(request):
#     auth_logout(request)
#     return redirect('login')

@csrf_exempt
def weekly_quiz(request):
    if request.method == 'GET':
        # Get most recent active quiz
        quiz = Quiz.objects.filter(is_active=True).order_by('-start_date').first()
        
        if not quiz:
            return redirect('home')
        
        questions = quiz.questions.all()
        
        # Check if user already completed THIS quiz
        if QuizScore.objects.filter(user=request.user, quiz=quiz).exists():
            return redirect('quiz_complete')
        
        return render(
            request, 
            'weekly.html', 
            {
            'quiz': quiz,
            'questions': questions
            }
        )

    else:
        # Get most recent active quiz
        quiz = Quiz.objects.filter(is_active=True).order_by('-start_date').first()
        
        if not quiz:
            return render(request, 'no_quiz.html')
        
        questions = quiz.questions.all()
        total_score = 0
        
        # Process form submission
        for question in questions:
            if question.question_type in ['MC', 'YN']:
                choice_id = request.POST.get(f'question_{question.id}')
                if choice_id:
                    choice = Choice.objects.get(id=choice_id)
                    is_correct = choice.is_correct
                    points = getattr(question, 'points', 1) if is_correct else 0
                    #points = question.points if is_correct else 0
                    total_score += points
                    
                    UserResponse.objects.create(
                        user=request.user,
                        question=question,
                        selected_choice=choice,
                        is_correct=is_correct,
                        points_earned=points
                    )
            elif question.question_type == 'TEXT':
                answer = request.POST.get(f'question_{question.id}')
                if answer:
                    UserResponse.objects.create(
                        user=request.user,
                        question=question,
                        answer_text=answer
                    )
            elif question.question_type == 'IMG':
                image = request.FILES.get(f'question_{question.id}')
                if image:
                    # For image answers, you might need manual grading
                    UserResponse.objects.create(
                        user=request.user,
                        question=question,
                        image_upload=image
                    )
        
        # Create or update the quiz score
        QuizScore.objects.create(
            user=request.user,
            quiz=quiz,
            total_score=total_score
        )
        
        return render(request, 'quizcomplete.html', {
            'quiz': quiz,
            'score': total_score,
            'position': None
        })


@login_required
def quiz_complete(request):
    quiz = Quiz.objects.filter(is_active=True).first()
    
    if not quiz or not QuizScore.objects.filter(user=request.user, quiz=quiz).exists():
        return redirect('weekly_quiz')
    
    # Get user's score and position
    user_score = QuizScore.objects.get(user=request.user, quiz=quiz)
    
    # Get leaderboard position
    leaderboard = QuizScore.objects.filter(quiz=quiz).order_by('-total_score', 'completed_at')
    position = list(leaderboard.values_list('id', flat=True)).index(user_score.id) + 1
    
    return render(request, 'quizcomplete.html', {
        'quiz': quiz,
        'score': user_score,
        'position': position
    })

# @login_required
# def leaderboard(request):
#     active_quiz = Quiz.objects.filter(is_active=True).first()
    
#     if not active_quiz:
#         return redirect('home')
    
#     # Get top 20 scores for this quiz
#     leaderboard = QuizScore.objects.filter(
#         quiz=active_quiz
#     ).select_related('user').order_by('-total_score', 'completed_at')[:20]
    
#     # Annotate with rank
#     ranked_leaderboard = []
#     for rank, score in enumerate(leaderboard, start=1):
#         ranked_leaderboard.append({
#             'rank': rank,
#             'user': score.user,
#             'score': score.total_score,
#             'completed_at': score.completed_at
#         })
    
#     # Get current user's position if they participated
#     user_position = None
#     user_score = None
#     if QuizScore.objects.filter(user=request.user, quiz=active_quiz).exists():
#         all_scores = QuizScore.objects.filter(quiz=active_quiz).order_by('-total_score', 'completed_at')
#         user_score = QuizScore.objects.get(user=request.user, quiz=active_quiz)
#         user_position = list(all_scores.values_list('id', flat=True)).index(user_score.id) + 1
    
#     return render(request, 'leaderboard.html', {
#         'quiz': active_quiz,
#         'leaderboard': ranked_leaderboard,
#         'user_position': user_position,
#         'user_score': user_score
#     })





def get_gravatar_url(email, size=40):
    """Safe Gravatar URL generator with fallbacks"""
    try:
        email = (email or "default@example.com").strip().lower()
        return f"https://www.gravatar.com/avatar/{md5(email.encode('utf-8')).hexdigest()}?{urlencode({'d':'mp', 's':size})}"
    except:
        return "https://www.gravatar.com/avatar/default?d=mp&s=40"






# @login_required
# def leaderboard(request):
#     try:
#         # FIX 1: More precise quiz filtering
#         from django.utils import timezone
#         active_quiz = Quiz.objects.filter(
#             is_active=True,
#             start_date__lte=timezone.now(),
#             end_date__gte=timezone.now()
#         ).first()
        
#         if not active_quiz:
#             return render(request, 'leaderboard.html', {
#                 'error': 'No currently active quiz'
#             })

#         # FIX 2: Get all scores in proper order
#         scores = QuizScore.objects.filter(
#             quiz=active_quiz
#         ).select_related('user').order_by('-total_score', 'completed_at')

#         # FIX 3: Build leaderboard with proper ranking (handling ties)
#         leaderboard_data = []
#         current_rank = 0
#         prev_score = None
        
#         for index, score in enumerate(scores, start=1):
#             if score.total_score != prev_score:
#                 current_rank = index
#             leaderboard_data.append({
#                 'rank': current_rank,
#                 'user': score.user,
#                 'username': score.user.username,
#                 'profile_pic': get_gravatar_url(score.user.email),
#                 'score': score.total_score,
#                 'completed_at': score.completed_at
#             })
#             prev_score = score.total_score

#         # FIX 4: More reliable user position detection
#         user_position = None
#         user_score = None
        
#         if request.user.is_authenticated:
#             try:
#                 user_score = QuizScore.objects.get(
#                     user=request.user,
#                     quiz=active_quiz
#                 )
#                 # Find position in the properly ranked list
#                 user_position = next(
#                     (entry['rank'] for entry in leaderboard_data 
#                      if entry['user'].id == request.user.id),
#                     None
#                 )
#             except QuizScore.DoesNotExist:
#                 pass

#         return render(request, 'leaderboard.html', {
#             'quiz': active_quiz,
#             'leaderboard': leaderboard_data,
#             'user_position': user_position,
#             'user_score': user_score.total_score if user_score else None
#         })

#     except Exception as e:
#         # Log error in production: logger.error(f"Leaderboard error: {str(e)}")
#         return render(request, 'leaderboard.html', {
#             'error': 'Could not load leaderboard'
#         })



@login_required
def leaderboard(request):
    try:
        # Get latest quiz instead of filtering by date
        active_quiz = Quiz.objects.order_by('-start_date').first()

        if not active_quiz:
            return render(request, 'leaderboard.html', {
                'error': 'No quiz found.'
            })

        # Fetch all scores for the quiz
        scores = QuizScore.objects.filter(
            quiz=active_quiz
        ).select_related('user').order_by('-total_score', 'completed_at')

        leaderboard_data = []
        current_rank = 0
        prev_score = None

        for index, score in enumerate(scores, start=1):
            if score.total_score != prev_score:
                current_rank = index
            leaderboard_data.append({
                'rank': current_rank,
                'user': score.user,
                'username': score.user.username,
                'profile_pic': get_gravatar_url(score.user.email),
                'score': score.total_score,
                'completed_at': score.completed_at
            })
            prev_score = score.total_score

        context = {
            'quiz': active_quiz,
            'leaderboard': leaderboard_data,
            'error': None
        }

        if request.user.is_authenticated:
            try:
                user_score = QuizScore.objects.get(
                    user=request.user,
                    quiz=active_quiz
                )
                user_position = next(
                    (entry['rank'] for entry in leaderboard_data 
                     if entry['user'].id == request.user.id),
                    None
                )
                context.update({
                    'user_position': user_position,
                    'user_score': user_score.total_score
                })
            except QuizScore.DoesNotExist:
                pass

        return render(request, 'leaderboard.html', context)

    except Exception as e:
        # In production: log this error
        return render(request, 'leaderboard.html', {
            'error': 'Could not load leaderboard'
        })




@login_required
def quiz_history(request):
    quiz_scores = QuizScore.objects.filter(user=request.user).order_by('-completed_at')
    return render(request, 'history.html', {'quiz_scores': quiz_scores})
