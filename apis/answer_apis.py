from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .answer_serializers import AddAnswerSerializer, ListAllUserAnswerSerializer, \
    UpdateAnswerSerializer, AnswerDetailSerializer
from django.utils import timezone
from k12App.models import Answer

class CreateAnswer(APIView):
    """
    post:
    Create a new answer
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request.data)
        serializer = AddAnswerSerializer(data=request.data)
        if serializer.is_valid():
            if Answer.objects.filter(question=request.data.get('question'), created_by= request.user):
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'You have already answered this question',
                    }
                )

            try:
                serializer.validated_data['created_by'] = request.user
                serializer.validated_data['created_on'] =  timezone.now()
                obj = Answer.objects.create(**serializer.validated_data)
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'message': 'Answer created'
                    },status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'error': str(e)
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

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

class ListAllUserAnswers(APIView):
    """
    get:
    Return all answer list
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        queryset = Answer.objects.filter(created_by=request.user)
        serializer = ListAllUserAnswerSerializer(queryset, many=True)

        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'All answers fetched',
                'data': serializer.data,
            },status=status.HTTP_200_OK
        )

class UpdateAnswer(APIView):
    """
    Patch:
    Update an answer
    """

    permission_classes = (IsAuthenticated,)

    def patch(self, request,pk):
        question = request.data.get('question')
        if question:
            try:
                ans = Answer.objects.get(id=pk)
                if ans.question != question and ans.created_by != request.user:
                    return Response(
                        {
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'This is not your answer',
                        }
                    )

                serializer = UpdateAnswerSerializer(ans, data=request.data, partial=True)
                if serializer.is_valid():
                    try:
                        serializer.validated_data['updated_on'] = timezone.now()
                        serializer.save()
                        return Response(
                            {
                                'status': status.HTTP_200_OK,
                                'message': 'Answer updated successfully',
                            }, status=status.HTTP_200_OK
                        )
                    except Exception as e:
                        return Response(
                            {
                                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                                'error': str(e)
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

            except Answer.DoesNotExist:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'error': 'Answer not found',
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'error': str(e),
                    }, status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error' :'Question is required',
                },status=status.HTTP_400_BAD_REQUEST
            )

class AnswerDetail(APIView):
    """
    Get:
    Get answer detail
    """

    #permission_classes = (IsAuthenticated,)

    def get(self, request,pk):
        try :
            obj = Answer.objects.get(id=pk)
            serializer = AnswerDetailSerializer(obj)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Answer details fetched',
                    'data': serializer.data,
                },status=status.HTTP_200_OK
            )
        except Answer.DoesNotExist:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Answer not found',
                },status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': str(e),
                },status=status.HTTP_400_BAD_REQUEST
            )

class DeleteAnswer(APIView):
    """
    delete:
    Deete an answer
    """

    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        try:
            obj = Answer.objects.get(id=pk)
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
                    'message': 'Answer deleted'
                }, status=status.HTTP_200_OK
            )
        except Answer.DoesNotExist:
            return Response(
                {
                    'staus': status.HTTP_400_BAD_REQUEST,
                    'error': 'Answer not found',
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'staus': status.HTTP_400_BAD_REQUEST,
                    'error': str(e),
                }, status=status.HTTP_400_BAD_REQUEST
            )


