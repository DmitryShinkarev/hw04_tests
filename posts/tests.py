from django.core import mail
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from .models import Post
from .forms import PostForm

User = get_user_model()

# Create your tests here.
class UserTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user", email="mail@mail.com", password="qaz123"
        )
        self.post = Post.objects.create(
            text="First post from test system",
            author=self.user, pub_date='17.04.2020')

    def test_send_email(self):
        ''' Пользователь регистрируется и ему отправляется письмо с подтверждением регистрации
         Метод send_mail отправляет email сообщения. '''
        mail.send_mail(
            'Theme mail', 'Text mail.',
            'mail@mail.net', ['tomail@mail.com'],
            fail_silently=False,  # выводить описание ошибок
        )
        # Проверяем, что письмо лежит в исходящих
        self.assertEqual(len(mail.outbox), 1)
        # Проверяем, что тема первого письма правильная.
        self.assertEqual(mail.outbox[0].subject, 'Theme mail')

    def test_profile(self):
        ''' После регистрации пользователя создается его персональная страница (profile) '''
        response = self.client.get("/test_user/")
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        ''' Авторизованный пользователь может опубликовать пост (new) '''
        self.client.login(username='test_user', password='qaz123')
        response = self.client.post('/new/', {'text': 'create test post'})
        self.assertEqual(response.status_code, 302)
        response1 = self.client.get('/')
        self.assertContains(response1, text='create test post')

    def test_redirect(self):
        ''' Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа) '''
        response = self.client.get('/new/')
        self.assertRedirects(response, '/auth/login/?next=/new/', status_code=302,
                             target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_accept_post(self):
        ''' После публикации поста новая запись появляется на главной странице сайта (index),
         на персональной странице пользователя (profile), и на отдельной странице поста (post) '''
        self.client.login(username='test_user', password='qaz123')
        post_text = "Test text"
        self.post = Post.objects.create(text=post_text, author=self.user)
        post_id = self.post.pk
        response = self.client.get('/')  # проверка для главной страницы
        self.assertContains(response, post_text)
        response1 = self.client.get('/test_user/')  # проверка на профиле
        self.assertContains(response1, post_text)
        response2 = self.client.get(f'/test_user/{post_id}/')  # проверка для страницы поста
        self.assertContains(response2, post_text)

    def test_edit_post(self):
        ''' Авторизованный пользователь может отредактировать свой пост и его содержимое
         изменится на всех связанных страницах '''
        self.client.login(username='test_user', password='qaz123')
        post_text = "edit test text"
        post_id = self.post.pk
        self.post = Post.objects.create(text=post_text, author=self.user)
        response = self.client.post(f'/test_user/{post_id}/edit/', {'text': 'edit test text'})
        self.assertEqual(response.status_code, 302)
        response1 = self.client.get('/')  # на главной странице
        self.assertContains(response1, text='edit test text')
        response2 = self.client.get('/test_user/')  # проверка на профиле
        self.assertContains(response2, text='edit test text')
        response3 = self.client.get(f'/test_user/{post_id}/')  # проверка для страницы поста
        self.assertContains(response3, text='edit test text')

