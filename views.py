from bakery.views import BuildableDetailView

from wagtail.wagtailcore.views import serve
from wagtail.wagtailcore.middleware import SiteMiddleware

class BakeryView(BuildableDetailView):
    """
    An abstract class that can be inherited to create a buildable view that can be 
    added to BAKERY_VIEWS setting. An inheriting class should define a bakery_model 
    property pointing to a Wagtail Page model.

    Example:

        # File: app/models.py

        from wagtail.wagtailcore.pages import Page

        class AuthorPage(Page):
            bakery_views = ('app.bakery_views.AuthorPage',)
            ...

        # File: app/bakery_views.py

        from wagtail.wagtailbakery.views import BakeryView
        from . import models

        class AuthorPage(BakeryView):
            bakery_model = models.AuthorPage

        # File: project/settings.py:

        BAKERY_VIEWS = (
            'app.bakery_views.AuthorPage',
            ...
        )

        BUILD_DIR = os.path.join(PROJECT_ROOT, 'baked')

    Build command:

        python manage.py build app.bakery_views.AuthorPage

    """

    bakery_model = None

    def get_queryset(self):
        """
        Defines get_queryset() for BuildableDetailView to return a 
        QuerySet containing all live Wagtail Page models
        """
        return self.bakery_model.objects.live()

    def get(self, request):
        """
        Overrides DetailView's get() to return TemplateResponse from serve() 
        after passing request through Wagtail SiteMiddleware
        """
        smw = SiteMiddleware()
        smw.process_request(request)
        response = serve(request, request.path)
        return response

    def get_url(self, obj):
        """
        Overrides BuildableDetailView's get_url() to return a url from the
        Page model url property
        """
        return obj.url

    class Meta:
        abstract = True

