from rest_framework import serializers
from k12App.models import Question, Answer
from .answer_serializers import ListAllUserAnswerSerializer

class CreateQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'

    def validate(self, data):
        if len(data['title']) >255:
            raise serializers.ValidationError('Question too long')
        return data

class ListAllQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'created_on', 'updated_on']

class QuestionDetailSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = '__all__'

    def get_answer(self, obj):
        answers = Answer.objects.filter(question=obj)
        serializer = ListAllUserAnswerSerializer(answers, many=True)
        return serializer.data



class QuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    def validate(self,data):
        if not data.get('title'):
            raise serializers.ValidationError('Please provide question title')
        elif len(data['title']) >255:
            raise serializers.ValidationError('Question too long')

        return data