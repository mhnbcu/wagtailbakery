from wagtail.wagtailcore.signals import page_published, page_unpublished

def rebuild_parents(instance):
    page = instance.get_parent()
    if page:
        page = page.specific
    while page and page.live and (not page.is_root()):
        if hasattr(page, 'build'):
            page.build()
        page = page.get_parent()
        if page:
            page = page.specific

def handle_publish(sender, instance, **kwargs):
    """
    Receives page_published signal to build page
    """
    if hasattr(instance, 'build'):
        instance.build()
        num_revisions = instance.revisions.count()
        if (num_revisions > 1) and (not instance.is_root()):
            prior_page = instance.revisions.order_by('-id')[1].as_page_object().specific
            if instance.slug != prior_page.slug:
                    prior_page.unbuild()
    rebuild_parents(instance)

def handle_unpublish(sender, instance, **kwargs):
    """
    Receives page_unpublished signal to unbuild page
    """
    if hasattr(instance, 'unbuild'):
        instance.unbuild()
    rebuild_parents(instance)

def register_signal_handlers():
    """
    Connect handlers to page publish signals
    """
    page_published.connect(handle_publish, dispatch_uid='wagtailbakery_page_published') 
    page_unpublished.connect(handle_unpublish, dispatch_uid='wagtailbakery_page_unpublished') 
