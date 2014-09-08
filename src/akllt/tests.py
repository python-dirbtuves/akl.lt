from django.test.testcases import TransactionTestCase


class SmokeTest(TransactionTestCase):

    def test_nothing(self):
        self.client.get('/')
