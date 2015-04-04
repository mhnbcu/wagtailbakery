Wagtail Bakery
========================
Wagtail Bakery is a SAMPLE module for static generation with Django Bakery.

Making models available for static generation
---------
1. Add a bakery_views property to each page that will be staticly generated
2. Create a bakery_views.py file with a class for each page that will be staticly generated
3. Add BUILD_DIR and BAKERY_VIEWS settings

app/models.py

    from wagtail.wagtailcore.models import Page

    class AuthorPage(Page):
        bakery_views = ('app.bakery_views.AuthorPageStatic',)

app/bakery_views.py

    from wagtailbakery.views import BakeryView
    from app.models import AuthorPage

    class AuthorPageStatic(BakeryView):
        bakery_model = models.AuthorPage

project/settings.py

    BUILD_DIR = os.path.join(PROJECT_DIR, 'bakery_output')
    BAKERY_VIEWS = (
        'app.bakery_views.AuthorPageStatic',
    )
    ALLOW_BAKERY_AUTO_PUBLISHING = False

Automatic static generation
---------
1. Follow steps under "Making models available for static generation"
2. Modify models.py to include and use BakeryModel mixin

app/models.py

    from wagtail.wagtailcore.models import Page
    from wagtailbakery.models import BakeryModel

    class AuthorPage(Page, BakeryModel):
        bakery_views = ('app.bakery_views.AuthorPageStatic',)

Generating in the background with Celery
---------
1. Follow steps under "Automatic static generation"
2. Modify models.py to include and use the PublishingBakeryModel mixin

app/models.py

    from wagtail.wagtailcore.models import Page
    from wagtailbakery.models import PublishingBakeryModel

    class AuthorPage(Page, PublishingBakeryModel):
        bakery_views = ('app.bakery_views.AuthorPageStatic',)

Publishing to AWS 
---------
1. Follow steps under "Generating in the background with Celery"
2. Modify settings.py to enable auto publishing to AWS

project/settings.py

    BUILD_DIR = os.path.join(PROJECT_DIR, 'bakery_output')
    BAKERY_VIEWS = (
        'app.bakery_views.AuthorPageStatic',
    )
    ALLOW_BAKERY_AUTO_PUBLISHING = True


