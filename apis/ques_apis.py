from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from k12App.models import Question
from .question_serializers import CreateQuestionSerializer, ListAllQuestionSerializer,\
    QuestionUpdateSerializer, QuestionDetailSerializer
from django.utils import timezone

class AddQuestion(APIView):
    """
    post:
    Create a Question
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        que = request.data.get('title',None)
        if que:
            query = Question.objects.filter(created_by=request.user, title=que)
            if query:
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'message': 'This Question is already being asked by you.'
                    }, status=status.HTTP_200_OK
                )
            serializer = CreateQuestionSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.validated_data['created_by'] = request.user
                    serializer.validated_data['created_on'] = timezone.now()
                    new_que = Question.objects.create(**serializer.validated_data)

                    return Response(
                        {
                            'status': status.HTTP_200_OK,
                            'message': 'Question created successfully',
                        },status=status.HTTP_200_OK
                    )

                except Exception as e:
                    print(e)
                    return Response(
                        {
                            'message': 'Server error',
                            'error_message': str(e),
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            else:
                error_msg = ''
                for key, value in serializer.errors.items():
                    error = {'field': key, 'message': value}
                    error_msg = str(key) + ':' + str(value[0]) + ' '

                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'error': error_msg,
                    }, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {
                'status': status.HTTP_400_BAD_REQUEST,
                'error': 'Please provide Question'
            },status=status.HTTP_400_BAD_REQUEST
        )

class ListAllUserQuestions(APIView):
    """
    Get:
    Return list of all questions asked by a user
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        data = Question.objects.filter(created_by=request.user)
        serializer = ListAllQuestionSerializer(data, many=True)

        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'Questions fetched',
                'data': serializer.data,
            },status=status.HTTP_200_OK
        )


class QuestionDetail(APIView):
    """
    get:
    Return a question detail
    """

    def get(self, request,pk):

        try:
            query = Question.objects.get(id=pk)
            serializer = QuestionDetailSerializer(query)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Question details fetched',
                    'data': serializer.data,
                },status=status.HTTP_200_OK
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


class QuestionUpdate(APIView):
    """
    patch:
    Update question
    """

    permission_classes = (IsAuthenticated,)

    def patch(self, request,pk):
        try:
            data = Question.objects.get(id=pk)
            if data.created_by != request.user:
                return Response(
                    {
                        'status': status.HTTP_401_UNAUTHORIZED,
                        'message': 'This Question is not created by you.'
                    }, status=status.HTTP_401_UNAUTHORIZED
                )

            serializer = QuestionUpdateSerializer(data, data=request.data, partial=True)
            if serializer.is_valid():
                try:
                    serializer.validated_data['updated_on']  = timezone.now()
                    serializer.save()
                    return  Response(
                        {
                            'status': status.HTTP_200_OK,
                            'message': 'Question updated successfully',
                        }, status=status.HTTP_200_OK
                    )
                except Exception as e:
                    return Response(
                        {
                            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                            'error': str(e)
                        },status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                error_msg = ''
                for key, value in serializer.errors.items():
                    error = {'field': key, 'message': value}
                    error_msg = str(key) + ':' + str(value[0]) + ' '

                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'error': error_msg,
                    }, status=status.HTTP_400_BAD_REQUEST
                )

        except Question.DoesNotExist:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error' : 'Question not found',
                },status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': str(e),
                }, status=status.HTTP_400_BAD_REQUEST
            )



class QuestionDelete(APIView):
    """
    delete:
    Delete a Question
    """
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        try:
            obj = Question.objects.get(id=pk)
            if obj.created_by != request.user:
                return Response(
                    {
                        'statu': status.HTTP_401_UNAUTHORIZED,
                        'message': 'You cannot delete this answer',
                    }
                )
            obj.delete()
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Question deleted'
                }, status=status.HTTP_200_OK
            )
        except Question.DoesNotExist:
            return Response(
                {
                    'staus': status.HTTP_400_BAD_REQUEST,
                    'error': 'Question not found',
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'staus': status.HTTP_400_BAD_REQUEST,
                    'error': str(e),
                },status=status.HTTP_400_BAD_REQUEST
            )


