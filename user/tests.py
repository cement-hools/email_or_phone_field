from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class UserTestCase(APITestCase):
    def setUp(self):
        self.user_admin = User.objects.create_superuser(login='admin')
        self.user_1 = User.objects.create(login='user_1',
                                          password=make_password('E4CYR9ffmU'))

        self.client_admin = self.client_class()
        self.client_not_auth = self.client_class()

        self.client_admin.force_authenticate(self.user_admin)
        self.client.force_authenticate(self.user_1)

    def test_registration_all_fields(self):
        """Регистрация пользователя все рекомендованные поля."""
        self.assertEqual(2, User.objects.all().count(),
                         'Начальное количество пользователей')
        url = reverse('adduser')
        data = {
            "name": "Sekachev Maxim Sergeevich",
            "date_of_birth": "09.02.1988",
            "phone": 9555666000,
            "email": "cement@ya.ru",
            "login": "cement"
        }

        response = self.client_not_auth.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code,
                         'Неверный статус ответа')
        self.assertEqual(3, User.objects.all().count(),
                         'Неверное количество пользователей после создания')
        user_login = response.data.get('login')
        user_password = response.data.get('password')
        new_user = User.objects.all().last()
        self.assertIsNotNone(user_login, 'user_login не содержится в ответе')
        self.assertIsNotNone(user_password,
                             'user_password не содержится в ответе')
        self.assertEqual("cement", user_login,
                         'В ответе неверное значение login')
        self.assertEqual(user_login, new_user.login,
                         'Неверное значение login у созданного пользователя')
        self.assertEqual(9555666000, new_user.phone,
                         'Неверное значение phone у созданного пользователя')
        self.assertEqual('cement@ya.ru', new_user.email,
                         'Неверное значение email у созданного пользователя')
        user_date_of_birth = new_user.date_of_birth
        self.assertEqual("09.02.1988", user_date_of_birth.strftime('%d.%m.%Y'),
                         'Неверное значение date_of_birth '
                         'у созданного пользователя')
        self.assertEqual('Sekachev Maxim Sergeevich', new_user.name,
                         'Неверное значение name у созданного пользователя')

    def test_registration_non_phone_field(self):
        """Регистрация пользователя без поля phone."""
        self.assertEqual(2, User.objects.all().count(),
                         'Начальное количество пользователей')
        url = reverse('adduser')
        data = {
            "name": "Sekachev Maxim Sergeevich",
            "date_of_birth": "09.02.1988",
            "email": "cement@ya.ru",
            "login": "cement"
        }

        response = self.client_not_auth.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code,
                         'Неверный статус ответа')
        self.assertEqual(3, User.objects.all().count(),
                         'Неверное количество пользователей после создания')
        user_login = response.data.get('login')
        user_password = response.data.get('password')
        new_user = User.objects.all().last()
        self.assertIsNotNone(user_login, 'user_login не содержится в ответе')
        self.assertIsNotNone(user_password,
                             'user_password не содержится в ответе')
        self.assertEqual("cement", user_login,
                         'В ответе неверное значение login')
        self.assertEqual(user_login, new_user.login,
                         'Неверное значение login у созданного пользователя')
        self.assertIsNone(new_user.phone,
                          'Значение phone не None у созданного пользователя')
        self.assertEqual('cement@ya.ru', new_user.email,
                         'Неверное значение email у созданного пользователя')
        user_date_of_birth = new_user.date_of_birth
        self.assertEqual("09.02.1988", user_date_of_birth.strftime('%d.%m.%Y'),
                         'Неверное значение date_of_birth '
                         'у созданного пользователя')
        self.assertEqual('Sekachev Maxim Sergeevich', new_user.name,
                         'Неверное значение name у созданного пользователя')

    def test_registration_none_email_field(self):
        """Регистрация пользователя без поля email."""
        self.assertEqual(2, User.objects.all().count(),
                         'Начальное количество пользователей')
        url = reverse('adduser')
        data = {
            "name": "Sekachev Maxim Sergeevich",
            "date_of_birth": "09.02.1988",
            "phone": 9555666000,
            "login": "cement"
        }

        response = self.client_not_auth.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code,
                         'Неверный статус ответа')
        self.assertEqual(3, User.objects.all().count(),
                         'Неверное количество пользователей после создания')
        user_login = response.data.get('login')
        user_password = response.data.get('password')
        new_user = User.objects.all().last()
        self.assertIsNotNone(user_login, 'user_login не содержится в ответе')
        self.assertIsNotNone(user_password,
                             'user_password не содержится в ответе')
        self.assertEqual("cement", user_login,
                         'В ответе неверное значение login')
        self.assertEqual(user_login, new_user.login,
                         'Неверное значение login у созданного пользователя')
        self.assertEqual(9555666000, new_user.phone,
                         'Неверное значение phone у созданного пользователя')
        self.assertIsNone(new_user.email,
                          'Значение email не None у созданного пользователя')
        user_date_of_birth = new_user.date_of_birth
        self.assertEqual("09.02.1988", user_date_of_birth.strftime('%d.%m.%Y'),
                         'Неверное значение date_of_birth '
                         'у созданного пользователя')
        self.assertEqual('Sekachev Maxim Sergeevich', new_user.name,
                         'Неверное значение name у созданного пользователя')

    def test_registration_none_date_field(self):
        """Регистрация пользователя без поля date_of_birth."""
        self.assertEqual(2, User.objects.all().count(),
                         'Начальное количество пользователей')
        url = reverse('adduser')
        data = {
            "name": "Sekachev Maxim Sergeevich",
            "phone": 9555666000,
            "email": "cement@ya.ru",
            "login": "cement"
        }

        response = self.client_not_auth.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code,
                         'Неверный статус ответа')
        self.assertEqual(3, User.objects.all().count(),
                         'Неверное количество пользователей после создания')
        user_login = response.data.get('login')
        user_password = response.data.get('password')
        new_user = User.objects.all().last()
        self.assertIsNotNone(user_login, 'user_login не содержится в ответе')
        self.assertIsNotNone(user_password,
                             'user_password не содержится в ответе')
        self.assertEqual("cement", user_login,
                         'В ответе неверное значение login')
        self.assertEqual(user_login, new_user.login,
                         'Неверное значение login у созданного пользователя')
        self.assertEqual(9555666000, new_user.phone,
                         'Неверное значение phone у созданного пользователя')
        self.assertEqual('cement@ya.ru', new_user.email,
                         'Неверное значение email у созданного пользователя')
        user_date_of_birth = new_user.date_of_birth
        self.assertIsNone(user_date_of_birth, 'Значение date_of_birth не None')
        self.assertEqual('Sekachev Maxim Sergeevich', new_user.name,
                         'Неверное значение name у созданного пользователя')

    def test_registration_none_email_and_phone_field(self):
        """Регистрация пользователя без поля email и phone."""
        self.assertEqual(2, User.objects.all().count(),
                         'Начальное количество пользователей')
        url = reverse('adduser')
        data = {
            "name": "Sekachev Maxim Sergeevich",
            "date_of_birth": "09.02.1988",
            "login": "cement"
        }

        response = self.client_not_auth.post(url, data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code,
                         'Неверный статус ответа')
        self.assertEqual(2, User.objects.all().count(),
                         'Неверное количество пользователей после создания')
        self.assertIn('email or phone', response.data,
                      'В ответе нет ключа "email or phone"')
        code = response.data.get('email or phone')[0].code
        self.assertEqual('required', code, 'Неверный код ошибки')

    def test_registration_none_name_field(self):
        """Регистрация пользователя без поля name."""
        self.assertEqual(2, User.objects.all().count(),
                         'Начальное количество пользователей')
        url = reverse('adduser')

        data = {
            "date_of_birth": "09.02.1988",
            "phone": 9555666000,
            "email": "cement@ya.ru",
            "login": "cement"
        }

        response = self.client_not_auth.post(url, data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code,
                         'Неверный статус ответа')
        self.assertEqual(2, User.objects.all().count(),
                         'Неверное количество пользователей после создания')

        self.assertIn('name', response.data, 'В ответе нет ключа "name"')
        code = response.data.get('name')[0].code
        self.assertEqual('required', code, 'Неверный код ошибки')

    def test_registration_none_login_field(self):
        """Регистрация пользователя без поля login."""
        self.assertEqual(2, User.objects.all().count(),
                         'Начальное количество пользователей')
        url = reverse('adduser')
        data = {
            "name": "Sekachev Maxim Sergeevich",
            "date_of_birth": "09.02.1988",
            "phone": 9555666000,
            "email": "cement@ya.ru",
        }

        response = self.client_not_auth.post(url, data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code,
                         'Неверный статус ответа')
        self.assertEqual(2, User.objects.all().count(),
                         'Неверное количество пользователей после создания')
        self.assertIn('login', response.data,
                      'В ответе нет ключа "login"')
        code = response.data.get('login')[0].code
        self.assertEqual('required', code, 'Неверный код ошибки')

    def test_login_user(self):
        """Аутентификация пользователя."""
        url = reverse('login')

        data = {
            "login": "user_1",
            "password": "E4CYR9ffmU"
        }
        response = self.client_not_auth.post(url, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code,
                         'Неверный статус ответа')

    def test_login_user_invalid_login_and_password(self):
        """Аутентификация пользователя, с неверным логином и паролем."""
        url = reverse('login')

        data_1 = {
            "login": "user_2",
            "password": "E4CYR9ffmU"
        }
        response = self.client_not_auth.post(url, data=data_1)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code,
                         'Неверный статус ответа')

        data_2 = {
            "login": "user_1",
            "password": "E4CYR9ffm1"
        }
        response = self.client_not_auth.post(url, data=data_2)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code,
                         'Неверный статус ответа')

    def test_logout_user(self):
        """ВЫход из системы пользователя."""
        url = reverse('logout')

        response = self.client_admin.post(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code,
                         'Неверный статус ответа')
        self.assertIn('ok', response.data)
        self.assertEqual(f'пользователь {self.user_admin.login} '
                         f'вышел из системы', response.data.get('ok'))

    def test_logout_non_auth_user(self):
        """ВЫход из системы не аутентифицированного пользователя."""
        url = reverse('logout')

        response = self.client_not_auth.post(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code,
                         'Неверный статус ответа')

