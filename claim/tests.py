from django.test import Client, TestCase

# Create your tests here.
class TestClaim(TestCase):
    def setUp(self):
        self.client = Client()
        pass
    
    
    def test_claim(self):
        response = self.client.get('/reclamaciones/')
        
        self.assertEqual(response.status_code, 200)