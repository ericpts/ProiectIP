from django.test import TestCase
from social.models import Rating, Comment
from accounts.models import User
from images.models import ImageConversion

class RatingTestCase(TestCase):
    def setUp(self):
        # create users
        self.user_andrei = User.objects.create(username='andrei', password='gogo1234')
        self.user_ali = User.objects.create(username='alisagis', password='gogo1234')

        # create uploads
        self.image_first = ImageConversion.objects.create(author=self.user_andrei, title='first')
        self.image_second = ImageConversion.objects.create(author=self.user_ali, title='second')

        # create ratings
        Rating.objects.create(author=self.user_andrei, image=self.image_first, rating=2)
        Rating.objects.create(author=self.user_ali, image=self.image_first, rating=3)
        Rating.objects.create(author=self.user_andrei, image=self.image_second, rating=5)
        Rating.objects.create(author=self.user_ali, image=self.image_second, rating=2)

    def testRatingAreCreated(self):
        self.assertTrue(len(Rating.objects.filter(author=self.user_andrei)) == 2,
                        'user_andrei rated 2 photos')
        self.assertTrue(len(Rating.objects.filter(author=self.user_ali)) == 2,
                        'user_ali rated 2 photos')

class CommentTestCase(TestCase):
    def setUp(self):
        # create users
        self.user_andrei = User.objects.create(username='andrei', password='gogo1234')
        self.user_ali = User.objects.create(username='alisagis', password='gogo1234')
        self.user_babi = User.objects.create(username='babi', password='gogo1234')

        # create uploads
        self.image_first = ImageConversion.objects.create(author=self.user_andrei, title='first')
        self.image_second = ImageConversion.objects.create(author=self.user_ali, title='second')

        # create comments
        Comment.objects.create(author=self.user_andrei, image=self.image_first, text='salut')
        Comment.objects.create(author=self.user_ali, image=self.image_first, text='skraaaa')
        Comment.objects.create(author=self.user_andrei, image=self.image_second, text='skipitupapa')

    def testCommentsAreCreated(self):
        self.assertTrue(len(Comment.objects.filter(author=self.user_andrei)) == 2,
                        'user_andrei created 2 comments')
        self.assertTrue(len(Comment.objects.filter(author=self.user_ali)) == 1,
                        'user_ali created 1 comments')
        self.assertTrue(len(Comment.objects.filter(author=self.user_babi)) == 0,
                        'user_babi created 0 comments')

