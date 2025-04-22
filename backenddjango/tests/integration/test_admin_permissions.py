from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User
from users.permissions import IsAdmin, IsAdminOrBroker, IsAdminOrBD, IsOwnerOrAdmin


class AdminPermissionsTest(APITestCase):
    """
    Test the permission classes related to admin access
    """
    
    def setUp(self):
        """
        Set up test data
        """
        # Create users with different roles
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        self.admin_user.role = 'admin'
        self.admin_user.save()
        
        self.broker_user = User.objects.create_user(
            username='broker',
            email='broker@example.com',
            password='brokerpassword'
        )
        self.broker_user.role = 'broker'
        self.broker_user.save()
        
        self.bd_user = User.objects.create_user(
            username='bd',
            email='bd@example.com',
            password='bdpassword'
        )
        self.bd_user.role = 'bd'
        self.bd_user.save()
        
        self.client_user = User.objects.create_user(
            username='client',
            email='client@example.com',
            password='clientpassword'
        )
        self.client_user.role = 'client'
        self.client_user.save()
    
    def test_is_admin_permission(self):
        """
        Test the IsAdmin permission class
        """
        permission = IsAdmin()
        
        # Create mock requests with different users
        admin_request = type('Request', (), {'user': self.admin_user})
        broker_request = type('Request', (), {'user': self.broker_user})
        bd_request = type('Request', (), {'user': self.bd_user})
        client_request = type('Request', (), {'user': self.client_user})
        
        # Test permission checks
        self.assertTrue(permission.has_permission(admin_request, None))
        self.assertFalse(permission.has_permission(broker_request, None))
        self.assertFalse(permission.has_permission(bd_request, None))
        self.assertFalse(permission.has_permission(client_request, None))
    
    def test_is_admin_or_broker_permission(self):
        """
        Test the IsAdminOrBroker permission class
        """
        permission = IsAdminOrBroker()
        
        # Create mock requests with different users
        admin_request = type('Request', (), {'user': self.admin_user})
        broker_request = type('Request', (), {'user': self.broker_user})
        bd_request = type('Request', (), {'user': self.bd_user})
        client_request = type('Request', (), {'user': self.client_user})
        
        # Test permission checks
        self.assertTrue(permission.has_permission(admin_request, None))
        self.assertTrue(permission.has_permission(broker_request, None))
        self.assertFalse(permission.has_permission(bd_request, None))
        self.assertFalse(permission.has_permission(client_request, None))
    
    def test_is_admin_or_bd_permission(self):
        """
        Test the IsAdminOrBD permission class
        """
        permission = IsAdminOrBD()
        
        # Create mock requests with different users
        admin_request = type('Request', (), {'user': self.admin_user})
        broker_request = type('Request', (), {'user': self.broker_user})
        bd_request = type('Request', (), {'user': self.bd_user})
        client_request = type('Request', (), {'user': self.client_user})
        
        # Test permission checks
        self.assertTrue(permission.has_permission(admin_request, None))
        self.assertFalse(permission.has_permission(broker_request, None))
        self.assertTrue(permission.has_permission(bd_request, None))
        self.assertFalse(permission.has_permission(client_request, None))
    
    def test_is_owner_or_admin_permission(self):
        """
        Test the IsOwnerOrAdmin permission class
        """
        permission = IsOwnerOrAdmin()
        
        # Create mock requests with different users
        admin_request = type('Request', (), {'user': self.admin_user})
        broker_request = type('Request', (), {'user': self.broker_user})
        
        # Create mock objects with user and created_by fields
        user_obj = type('UserObject', (), {'user': self.broker_user})
        created_by_obj = type('CreatedByObject', (), {'created_by': self.broker_user})
        no_user_field_obj = type('NoUserFieldObject', (), {})
        
        # Test object permission checks for admin
        self.assertTrue(permission.has_object_permission(admin_request, None, user_obj))
        self.assertTrue(permission.has_object_permission(admin_request, None, created_by_obj))
        self.assertTrue(permission.has_object_permission(admin_request, None, no_user_field_obj))
        
        # Test object permission checks for broker (owner)
        self.assertTrue(permission.has_object_permission(broker_request, None, user_obj))
        self.assertTrue(permission.has_object_permission(broker_request, None, created_by_obj))
        self.assertFalse(permission.has_object_permission(broker_request, None, no_user_field_obj))
        
        # Test object permission checks for broker (not owner)
        other_user_obj = type('OtherUserObject', (), {'user': self.client_user})
        other_created_by_obj = type('OtherCreatedByObject', (), {'created_by': self.client_user})
        
        self.assertFalse(permission.has_object_permission(broker_request, None, other_user_obj))
        self.assertFalse(permission.has_object_permission(broker_request, None, other_created_by_obj))
