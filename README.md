About
=====

Create simple A/B tests in Django by dynamically switching templates. Records unique hits and conversions to tests.

Usage
=====

 1. Update your `settings.py`:
 
        # Add `ab` to `INSTALLED_APPS`
        INSTALLED_APPS = (
            ...
            'ab',
            )
            
        # Add `ab.middleware.ABMiddleware` to `MIDDLEWARE_CLASSES`
        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            ...
            'ab.middleware.ABMiddleware',
        )

        # Add `ab.loaders.load_template_source` as your _FIRST_ `TEMPLATE_LOADERS`.
        TEMPLATE_LOADERS = (
            'ab.loaders.load_template_source',
            'django.template.loaders.filesystem.load_template_source',
            ...
        )
 
 2. Run `python manage.py sync_db` to create the testing tables.

 3. Create some tests in the Django admin (or like this from the command line)!

        from ab.models import Experiment, Test
        
        # Create an Experiment who's Goal is to get to the signup page!
        exp = Experiment.objects.create(name="Homepage Test", template_name="index.html", goal="/signup/")
        
        # Create three variations of the homepage.
        
        # One Test for the original template
        Test.objects.create(template_name="index.html",)
        
        # Two variations
        Test.objects.create(template_name="index_1.html", experiment=exp)
        Test.objects.create(template_name="index_2.html", experiment=exp)

 5. Profit.
 
 
Advanced
========

  1. Manually run an A/B test on a view:
  
        def view(request, template_name="original.html"):
        
            try:
                ab_template_name = request.ab.run(template_name)
            except TemplateDoesNotExist:
                ab_template_name = template_name
            
            return render_to_response(template_name)
    
Tips
----

Decide ahead of time what you are A/B testing - introductions of new designs are a great time to run your first test. Plan ahead of time and duplicate your templates / css / js / images so you don't have to hunt through version control to find the right ones later.


Notes
-----

 1. The current implementation uses a thread locals to stash the request object for use in places it isn't normally available.

 2. The current implementation is not compatible with Django's built in caching.

 3. The current implementation requires you to use Django Sessions.


ToDo
----

 1. Add A/B aware CacheMiddleware
 2. Rethink ab.abs.AB interface.
 3. De-couple AB from request/session object? Would be interesting to run it on e-mails etc.
 4. Add a way to force the display of specific templates (for designers etc.)
 5. What if a browser has disabled cookies? What's the fallback?
 6. Add some way to ignore hits and conversions (eg. internal/logged in etc.)
 7. Expanded conversion maybe to a regex? or something else that account for variations of pages