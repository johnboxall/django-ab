from django.db import models

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