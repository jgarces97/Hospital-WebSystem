from django.test import TestCase
from .models import PatientModel
from .models import User


# Create your tests here.
# no


class PatientTestCase(TestCase):
    def setUp(self):
        p = PatientModel()
        p.city = "nope"
        p.state = "dungbeetle"
        p.user_id = 1
        p.save()

    def test_user_creation(self):
        test_user = PatientModel.objects.get(city="nope")
        self.assertEqual(test_user.state, "dungbeetle")


class InsuranceNumTest(TestCase):
    def setUp(self):
        User.objects.all()
