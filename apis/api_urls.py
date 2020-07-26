from django.urls import path, include

from .user_apis import UserRegister,LogInUser
from .ques_apis import AddQuestion, ListAllUserQuestions, QuestionUpdate, QuestionDelete, QuestionDetail
from .answer_apis import CreateAnswer, ListAllUserAnswers, UpdateAnswer, DeleteAnswer, AnswerDetail
from .common_apis import UpVoteAnswer, FeedAPi, VotesOfAnAnswer, VotesQuestion, UpVotesBYUser

urlpatterns = [
    path('register/', UserRegister.as_view(), name = 'register'),
    path('login/', LogInUser.as_view(), name = 'login'),

    path('add-question/', AddQuestion.as_view(), name = 'add-question'),
    path('list-user-questions/', ListAllUserQuestions.as_view(), name='list-user-questions'),
    path('update-question/<str:pk>/', QuestionUpdate.as_view(), name= ' update-question'),
    path('delete-question/<str:pk>/', QuestionDelete.as_view(), name= 'delete-question' ),
    path('question-detail/<str:pk>/', QuestionDetail.as_view(), name= 'question-detail'),

    path('add-answer/',CreateAnswer.as_view(), name='add-answer' ),
    path('list-user-answers/', ListAllUserAnswers.as_view(), name = 'list-user-answers'),
    path('update-answer/<str:pk>/', UpdateAnswer.as_view(),name='update-answer'),
    path('delete-answer/<str:pk>/', DeleteAnswer.as_view(), name= 'delete-answer'),
    path('answer-detail/<str:pk>/', AnswerDetail.as_view(), name= 'answer-detail'),

    path('upvote-answer/<str:pk>/', UpVoteAnswer.as_view(), name = 'upvote-answer'),
    path('feedapi/', FeedAPi.as_view(), name='feed-api'),
    path('votes-answer/<str:pk>/', VotesOfAnAnswer.as_view(), name='votes-answer'),
    path('votes-question/<str:pk>/', VotesQuestion.as_view(), name= 'votes=question'),
    path('votes-user/', UpVotesBYUser.as_view(), name = 'votes-user'),

]