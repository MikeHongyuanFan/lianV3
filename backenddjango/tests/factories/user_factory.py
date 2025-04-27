"""
Factory for creating User objects.
"""
import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """Factory for creating User objects."""

    class Meta:
        model = User
        django_get_or_create = ('email',)

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False
    is_superuser = False
    role = 'client'


class AdminUserFactory(UserFactory):
    """Factory for creating admin User objects."""

    role = 'admin'
    is_staff = True
    is_superuser = True


class StaffUserFactory(UserFactory):
    """Factory for creating staff User objects."""

    role = 'staff'
    is_staff = True


class BrokerUserFactory(UserFactory):
    """Factory for creating broker User objects."""

    role = 'broker'


class ClientUserFactory(UserFactory):
    """Factory for creating client User objects."""

    role = 'client'


class BDMUserFactory(UserFactory):
    """Factory for creating BDM User objects."""

    role = 'bd'
