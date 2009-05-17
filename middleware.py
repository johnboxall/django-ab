try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

from ab.models import Experiment, Test


_thread_locals = local()
def get_current_request():
    return getattr(_thread_locals, 'request', None)

"""
Things to keep in mind:
* Only record goal conversions when a Experiment is active
* Can only record a conversion once

what about only running a test X times and then defaulting to the best performer?


!!! the session junk should be abstracted to some kind of model thing. SessionBackend.is_active etc.

"""


# @@@ How will caching effect all this???
class ABMiddleware:
    def process_request(self, request):
        """
        Puts the request object in local thread storage.
        Also checks whether we've reached a A/B test goal.
        """
        _thread_locals.request = request
        
        # We can only do this if a Experiment is active.
        
        
        print request.session.keys()
        
        if "ab_active" in request.session:
            experiments = Experiment.objects.all()
            for experiment in experiments:
            
                print request.path
                print experiment.goal
            
                if request.path == experiment.goal:
                
                    print 'yes'
                    
                    # @@@ Also 


                    key = "ab_%s" % experiment.template_name
                    if key in request.session and "converted" not in request.session[key]:
                        print request.session[key]
                        test_id = request.session[key]["id"]
                        test = Test.objects.get(pk=test_id)
                        test.conversions = test.conversions + 1
                        test.save()
                        
                        request.session[key]["converted"] = 1
                        request.session.modified = True
                        print request.session[key]
                    
                
            
            
    
    
    
    
