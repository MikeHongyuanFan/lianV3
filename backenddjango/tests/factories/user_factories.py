"""
Factories for user models.
"""
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """Factory for User model."""
    
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = factory.Iterator(['client', 'broker', 'bd', 'admin'])
    is_active = True
    date_joined = factory.LazyFunction(timezone.now)


class AdminUserFactory(UserFactory):
    """Factory for admin users."""
    
    role = 'admin'
    is_staff = True
    is_superuser = True
