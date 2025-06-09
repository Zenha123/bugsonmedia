
from django.contrib.auth.models import User
from django.db import models



class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    prize = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = [
        ('MC', 'Multiple Choice'),
        ('YN', 'Yes/No'),
        ('IMG', 'Image Recognition'),
        ('TEXT', 'Short Answer'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=4, choices=QUESTION_TYPES)
    text = models.TextField()
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)
    order = models.PositiveIntegerField()
    points = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    

class UserResponse(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='user_answer')
    answer_text = models.TextField(
        blank=True, null=True
    )
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE
    )
    selected_choice = models.ForeignKey(
        Choice, 
        on_delete=models.CASCADE, 
        blank=True, null=True, 
        related_name='user_choice'
    )
    image_upload = models.ImageField(
        upload_to='user_uploads/', 
        blank=True, null=True
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    is_correct = models.BooleanField(default=False)
    points_earned = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s response to {self.question}"


class QuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    total_score = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'quiz')
        ordering = ['-total_score', 'completed_at']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}: {self.total_score} points"