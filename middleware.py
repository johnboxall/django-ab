try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

from ab.abs import AB
from ab.models import Experiment


_thread_locals = local()
def get_current_request():
    return getattr(_thread_locals, 'request', None)


# @@@ This won't work with caching. Need to create an AB aware cache middleware.
class ABMiddleware:
    def process_request(self, request):
        """
        Puts the request object in local thread storage so we can access it in
        the template loader. If an Experiment is active then check whether we've
        reached it's goal.
        """
        _thread_locals.request = request
        
        request.ab = AB(request)
        # request.ab.run()
        # If at least one Experiment is running then check if we're at a Goal
        # @@@ All this logic seems like it could be moved into the AB class. (but does it belong there?)
        if request.ab.is_active():
            exps = Experiment.objects.all()
            for exp in exps:
                if request.ab.is_converted(exp):
                    request.ab.convert(exp)