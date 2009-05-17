from django.template.loaders.filesystem import load_template_source as default_template_loader
from django.template import TemplateDoesNotExist

from ab.middleware import get_current_request
from ab.models import Experiment

def load_template_source(template_name, template_dirs=None, 
    template_loader=default_template_loader):
    """If an Experiment exists for this template use template_loader to load it."""
    try:
        # @@@ This (c|sh)ould be a cached call.
        experiment = Experiment.objects.get(template_name=template_name)
    except Experiment.DoesNotExist:
        raise TemplateDoesNotExist, template_name
    
    request = get_current_request()
    test_template_name = experiment.get_test_template_for_request(request)

    return default_template_loader(test_template_name, 
        template_dirs=template_dirs)
load_template_source.is_usable = True
        
        