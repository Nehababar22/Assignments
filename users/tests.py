from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Interest
from .forms import RegisterForm
from channels.testing import WebsocketCommunicator
from chat_system.asgi import application


class UserRegistrationTests(TestCase):
    # Registration test cases 

    def test_user_registration_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())

    def test_user_registration_failure(self):
        get_user_model().objects.create_user(username='testuser', password='securepassword123')
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, 'Username already exists.')


class UserLoginTests(TestCase):
    # login test cases 

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='securepassword123')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'securepassword123'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, '/api/users/')

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password.') 

class InterestTests(TestCase):
    # Interest Test cases.

    def setUp(self):
        self.sender = get_user_model().objects.create_user(username='sender', password='password123')
        self.receiver = get_user_model().objects.create_user(username='receiver', password='password123')
        self.client.login(username='sender', password='password123')

    def test_send_interest_success(self):
        response = self.client.post(reverse('send-interest', args=[self.receiver.id]), {
            'message': 'Hello, I am interested in connecting!'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Interest.objects.filter(sender=self.sender, receiver=self.receiver).exists())

    def test_send_interest_failure(self):
        response = self.client.post(reverse('send-interest', args=[self.receiver.id]), {
            'message': ''
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, 'This field is required.')


class InterestViewTests(TestCase):
    # View interest test cases

    def setUp(self):
        self.sender = get_user_model().objects.create_user(username='sender', password='password123')
        self.receiver = get_user_model().objects.create_user(username='receiver', password='password123')
        self.interest = Interest.objects.create(sender=self.sender, receiver=self.receiver, message='Hello!')
        self.client.login(username='receiver', password='password123')

    def test_handle_interest_accept(self):
        response = self.client.get(reverse('handle-interest', args=[self.interest.id, 'accept']))
        self.assertEqual(response.status_code, 302) 


class FormTests(TestCase):
    # Form test cases
    
    def test_register_form_valid(self):
        form = RegisterForm(data={
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertFalse(form.is_valid())

    def test_register_form_invalid(self):
        get_user_model().objects.create_user(username='existinguser', password='password123')
        form = RegisterForm(data={
            'username': 'existinguser', 
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Username already exists.', form.errors['username'])
