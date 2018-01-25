from django.test import TestCase
from sign.models import Event, Guest


# Create your tests here.
class ModelTest(TestCase):

    def setUp(self):
        Event.objects.create(id=1, name="1+3 event", status=True, limit=200, address='shenzhen',
                             start_time='2018-01-18 02:38:51')
        Guest.objects.create(id=1, event_id=1, realname='alen', phone='13711001101', email='alen@mail.com', sign=False)

    def test_event_models(self):
        result = Event.objects.get(name="1+3 event")
        self.assertEqual(result.address, "shenzhen")
        self.assertEqual(result.address, "shenzhen1")
        self.assertEqual(result.status, True)

    def test_guest_models(self):
        result = Guest.objects.get(phone='13711001101')
        self.assertEqual(result.realname, "alen")
        self.assertEqual(result.sign, False)

