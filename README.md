About
=====

Create simple A/B tests in Django by dynamically switching templates. Records unique hits and conversions to tests.

Usage
=====

1. Add `ab` to your `INSTALLED_APPS` in `settings.py`.

2. Add `ab.middleware.ABMiddleware` to your `MIDDLEWARE_CLASSES` in `settings.py`.

3. Run `python manage.py sync_db` to create the testing tables.

4. Create some tests in the Django admin!

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


Notes
=====

1. The current implementation uses a thread locals to stash the request object for use in places it isn't normally available.

2. The current implementation is not compatible with Django's built in caching.

3. The current implementation requires you to use Django Sessions.