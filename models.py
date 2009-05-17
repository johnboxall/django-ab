from django.db import models


# @@@ How to remember tests are active???
    

class Experiment(models.Model):
    """
    
    """
    # @@@ unique=True ??? Does that make sense???
    name = models.CharField(max_length=255, unique=True)
    template_name = models.CharField(max_length=255, unique=True,
        help_text="Example: 'registration/signup.html'. The template to replaced.")
    goal = models.CharField(max_length=255, unique=True,
        help_text="Example: '/signup/complete/'. The path where the goal is converted.")
    
    def __unicode__(self):
        return self.name
    
    def get_session_key(self):
        return "ab_%s" % self.template_name
    
    def get_test_template_for_request(self, request):
        """
        Given a request return one of the templates from it's Tests.
        Tests are sticky - if a viewer saw a Test before, they should
        see the same test.
        """
        key = self.get_session_key()
        if key in request.session:
            return request.session[key]["template"]
        
        # Pick a Test to show.
        tests = self.test_set.all()
        # @@@ This hash will probably make the django pony cry.
        test = tests[request.session.accessed % len(tests)]

        # Record this unique hit to the Test.
        test.hits = test.hits + 1
        test.save()

        # Make the Test sticky.
        if key not in request.session:
            print 'here'
            request.session[key] = {"id": test.id, "template": test.template_name}
        

        request.session["ab_active"] = True
        
        
        return test.template_name


class Test(models.Model):
    """
    
    """
    experiment = models.ForeignKey(Experiment)
    template_name = models.CharField(max_length=255,
        help_text="Example: 'registration/signup_1.html'. The template to be tested.")
    hits = models.IntegerField(blank=True, default=0)
    conversions = models.IntegerField(blank=True, default=0)
    
    def __unicode__(self):
        return self.template_name