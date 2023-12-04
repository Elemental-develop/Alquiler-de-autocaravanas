from django.test import Client, TestCase

class TestReclamacion(TestCase):
    def setUp(self):
        self.client = Client()
        pass
    
    
    def test_reclamacion(self):
        response = self.client.get('/reclamaciones/')
        
        self.assertEqual(response.status_code, 200)