import os
 
from django.conf import settings
from django.test import TestCase

from ab.models import Test, Experiment


class ABTests(TestCase):
    urls = "ab.tests.test_urls"
    fixtures = ["test_data"]
    template_dirs = [
        os.path.join(os.path.dirname(__file__), 'templates'),
    ]
    
    def setUp(self):
        self.old_template_dir = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = self.template_dirs    
        
    def tearDown(self):
        settings.TEMPLATE_DIRS = self.old_template_dir
        
    def test_ab(self):
        # Careful here, response.template doesn't know where we are.
    
        # It always looks like we loaded the original.
        response = self.client.get("/test/")        
        self.assertTrue(response.template.name, "original.html")

        # But we really just loaded one of the tests (template_name is the response content)
        test = Test.objects.get(template_name=response.content)
        test_id = test.id
        self.assertEquals(test.hits, 1)
        self.assertEquals(test.conversions, 0)

        # Tests are sticky.
        for _ in range(9):
            responsex = self.client.get("/test/")        
        self.assertEquals(response.content, responsex.content)

        # @@@ Do we need to keep querying to make sure this is up to date?

        # Only one hit per unique view.
        test = Test.objects.get(pk=test_id)
        self.assertEquals(test.hits, 1)

        # Going to another page doesn't effect anything.
        response = self.client.get("/other/")
        test = Test.objects.get(pk=test_id)
        self.assertEquals(response.template.name, response.content)      
        self.assertEquals(test.hits, 1)
        self.assertEquals(test.conversions, 0)
        
        # Going to the goal results in a conversion.
        response = self.client.get("/goal/")
        test = Test.objects.get(pk=test_id)        
        self.assertEquals(response.template.name, response.content)      
        self.assertEquals(test.hits, 1)
        self.assertEquals(test.conversions, 1)
        
        
        
