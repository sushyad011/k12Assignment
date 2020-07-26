from rest_framework import serializers
from k12App.models import Upvote

class UpVoteAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Upvote
        fields = '__all__'