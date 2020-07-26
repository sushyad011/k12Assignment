from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from k12App.models import Answer, Question, Upvote
from .question_serializers import QuestionDetailSerializer
from .common_serializers import UpVoteAnswerSerializer

class UpVoteAnswer(APIView):
    """
    post:
    Like an answer
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request,pk):
        try:
            obj = Upvote.objects.get(user=request.user, answer = pk).delete()
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'error': 'Upvote reverted',
                }, status=status.HTTP_200_OK
            )

        except Upvote.DoesNotExist:
            try:
                ans = Answer.objects.get(id=pk)
            except Exception as e:
                return Response(
                    {
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'error': str(e),
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            obj = Upvote.objects.create(user=request.user, answer = ans, created_on = timezone.now())
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'error': 'Upvoted',
                }, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'error': str(e),
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FeedAPi(APIView):
    """
    get:
    Return a question detail
    """

    def get(self, request):

        try:
            query = Question.objects.all()
            serializer = QuestionDetailSerializer(query,many=True)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Question details fetched',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK
            )
        except Question.DoesNotExist:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Question not found',
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'error': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class VotesOfAnAnswer(APIView):
    """
    get:
    Return Votes of an answer
    """
    def get(self, request,pk):
        votes = Upvote.objects.filter(answer=pk)
        serializer =  UpVoteAnswerSerializer(votes,many=True)
        vote_count = votes.count()
        return Response (
            {
                'status': status.HTTP_200_OK,
                'message': 'Upvotes fetched',
                'data': serializer.data,
                'count': vote_count,
            },status=status.HTTP_200_OK
        )

class VotesQuestion(APIView):
    """
    get:
    Return Votes of an answer
    """

    def get(self, request, pk):
        ans = Answer.objects.filter(question=pk)
        votes = 0
        for q in ans:
            votes += Upvote.objects.filter(answer=q).count()
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'Upvotes fetched for a question',
                'data': votes
            }, status=status.HTTP_200_OK
        )

class UpVotesBYUser(APIView):
    """
    get:
    Return Votes of an answer
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request,):
        votes = Upvote.objects.filter(user=request.user).count()
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'Upvotes fetched by user',
                'data': votes
            }, status=status.HTTP_200_OK
        )
