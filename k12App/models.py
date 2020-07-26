from django.db import models
from django.contrib.auth.models import AbstractUser
from k12Assignment import settings
# Create your models here.

class User(AbstractUser):
    """
    Extending abstract user
    """
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True,default='Female',choices=gender_choices)
    dob = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True,upload_to=settings.CUSTOM_DIR['USER_PROFILE_PIC']+'/')
    mobile = models.CharField(max_length=255, null=True, blank=True)

    REQUIRED_FIELDS = ['email',]

    class Meta:
        # db_table = 'auth_user'

        default_permissions = ()
        permissions = (
            ('view_user', 'Can view users'),
            ('list_user', 'Can list users'),
            ('add_user', 'Can add users'),
            ('edit_user', 'Can edit users'),
            ('delete_user', 'Can delete users'),

        )

    def __repr__(self):
        """
        Return object representation
        :return: String
        """

        return '<User(id: %d, username:%s, email: %s)>' %(self.id, self.username, self.email)


class Question(models.Model):
    """
    Model to store Question
    """

    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT,null=True)
    created_on = models.DateTimeField(null=True, blank=True)
    updated_on = models.DateTimeField(null=True, blank=True)



    def __repr__(self):
        """
        Return objetc representation
        :return: String
        """

        return '<Question(id: %d, title: %s)>' %(self.id, self.title)


class Answer(models.Model):
    """
    Model to store answer
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    ans = models.TextField(max_length=4096, null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    created_on = models.DateTimeField(null=True, blank=True)
    updated_on = models.DateTimeField(null=True, blank=True)

    def __repr__(self):
        """
        Return object representation
        :return: String
        """

        return '<Answer(id: %d, ans %s)>' %(self.id, self.ans)


class Upvote(models.Model):
    """
    Model to store votes
    """

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(null=True, blank=True)

    def __repr__(self):
        """
        Return object representation
        :return: String
        """

        return '<Votes(id: %d, user: %s, answer: %s>' %(self.id, self.user, self.answer)
