from django.template import TemplateDoesNotExist
from ab.models import Experiment, Test


# @@@ The interface to this is shazbot. Rethink is in order.
class AB(object):
    """
    Uses request session to track Experiment state.
        - Whether an Experiment/Test is active
        - Whether an Experiment/Test has been converted   
    """

    def __init__(self, request):
        self.request = request

    def is_active(self):
        """True if at least one Experiment is running on this request."""
        return "ab_active" in self.request.session
        
    def is_converted(self, exp):
        """
        True if request location is the Goal of Experiment and this request
        hasn't already been converted.
        """
        return self.is_experiment_active(exp) and not self.is_experiment_converted(exp) \
            and exp.goal in self.request.path
        
    def is_experiment_active(self, exp):
        """True if this Experiment is active."""
        return self.get_experiment_key(exp) in self.request.session
        
    def is_experiment_converted(self, exp):
        """True if this Experiment has been converted."""
        return "converted" in self.request.session[self.get_experiment_key(exp)]
    
    def get_test(self, exp):
        """Returns a random Test for this Experiment"""
        tests = exp.test_set.all()
        return tests[self.request.session.session_key.__hash__() % len(tests)]

    def get_experiment_key(self, exp):
        return "ab_exp_%s" % exp.name

    def get_experiment(self, template_name):
        try:
            return Experiment.objects.get(template_name=template_name)
        except Experiment.DoesNotExist:
            raise TemplateDoesNotExist, template_name
        
    def run(self, template_name):
        """
        Searches for an Experiment running on template_name. If none are found
        raises a TemplateDoesNotExist otherwise activates a Test for that
        Experiment unless one is already running and returns the Test 
        template_name.
        """
        exp = self.get_experiment(template_name)

        # If this Experiment is active, return the template to show.
        key = self.get_experiment_key(exp)
        if self.is_experiment_active(exp):
            return self.request.session[key]["template"]

        # Otherwise Experiment isn't active so start one of its Tests.
        test = self.get_test(exp)
        self.activate(test, key)

        return test.template_name

    def activate(self, test, key):
        # Record this hit.
        test.hits = test.hits + 1
        test.save()

        # Activate this experiment/test on the request.
        self.request.session[key] = {"id": test.id, "template": test.template_name}
        
        # Mark that there is at least one A/B test running.
        self.request.session["ab_active"] = True
        
    def convert(self, exp):
        """Update the test active on the request for this experiment."""
        key = self.get_experiment_key(exp)
        test_id = self.request.session[key]["id"]
        test = Test.objects.get(pk=test_id)
        test.conversions = test.conversions + 1
        test.save()
        
        self.request.session[key]["converted"] = 1
        self.request.session.modified = True