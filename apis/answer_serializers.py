from rest_framework import serializers
from k12App.models import Answer, Question


class AddAnswerSerializer(serializers.ModelSerializer):
    question = serializers.IntegerField(required=True)
    ans = serializers.CharField(required=True)

    class Meta:
        model = Answer
        fields = '__all__'

    def validate_question(self, question):
        if not question:
            raise serializers.ValidationError('Que is a required field.')
        else:
            try:
                que = Question.objects.get(id=question)
            except Question.DoesNotExist:
                raise serializers.ValidationError('Invalid Question')
        return que

    def validate_ans(self, ans):
        if not ans:
            raise serializers.ValidationError('Ans is a required field.')

        return ans

class ListAllUserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class UpdateAnswerSerializer(serializers.ModelSerializer):
    ans = serializers.CharField(required=True)

    class Meta:
        model = Answer
        fields = '__all__'

    def validate_ans(self, ans):
        if not ans:
            raise serializers.ValidationError('Answer field is required')

        return ans

class AnswerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
