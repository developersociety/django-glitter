from django import template

from glitter.pages.models import Page
from glitter.pages.utils import resolve_page

register = template.Library()


@register.assignment_tag
def get_active_page(current_url):
    return resolve_page(current_url)


@register.assignment_tag
def get_root_pages(current_page=None):
    current_page = resolve_page(current_page)
    page_list = []

    # Find the root page so the template can highlight it
    if current_page:
        root_page = current_page.get_root()
    else:
        root_page = None

    page_qs = Page.objects.root_nodes().filter(
        show_in_navigation=True, published=True).exclude(current_version=None)

    for i in page_qs:
        page_list.append((i, i == root_page))

    return page_list


@register.assignment_tag
def get_pages_at_level(current_page, level=1):
    current_page = resolve_page(current_page)

    if not current_page:
        return []

    page_and_ancestors = list(current_page.get_ancestors(include_self=True))

    # Page isn't deep enough to show this level of navigation
    if level > current_page.level + 1:
        return []

    parent_page = page_and_ancestors[level - 1]
    page_list = []

    page_qs = parent_page.get_children().filter(
        show_in_navigation=True, published=True).exclude(current_version=None)

    for i in page_qs:
        page_list.append((i, i in page_and_ancestors))

    return page_list


@register.assignment_tag
def tree_from_root(current_page=None):
    current_page = resolve_page(current_page)
    tree = None

    if current_page:
        root_page = current_page.get_root()
        tree = root_page.get_descendants()

    return tree


@register.assignment_tag
def get_page_ancestor_ids(current_page=None):
    current_page = resolve_page(current_page)
    ancestors = []

    if current_page:
        ancestors = current_page.get_ancestors(include_self=True).values_list('id', flat=True)

    return ancestors


@register.inclusion_tag('glitter/navigation/level.html')
def primary_navigation(current_page=None, css_class='primary'):
    """ Render a list of primary level pages. """
    return {
        'page_list': get_root_pages(current_page=current_page),
        'css_class': css_class,
    }


@register.inclusion_tag('glitter/navigation/level.html')
def navigation_at_level(current_page=None, level=1, css_class=None):
    """
    Render a list of pages at a specific navigation level.

    This is an inclusion tag mostly used by secondary_navigation and
    tertiary_navigation - however it exists here incase additional levels of
    navigation are needed.

    At this point it's recommended that you might want to use a page tree for
    navigation instead.
    """
    # Use the level number if this isn't a named navigation level
    if css_class is None:
        css_class = 'level-{}'.format(level)

    return {
        'page_list': get_pages_at_level(current_page=current_page, level=level),
        'css_class': css_class,
    }


@register.inclusion_tag('glitter/navigation/level.html')
def secondary_navigation(current_page=None, css_class='secondary'):
    """ Render a list of secondary level pages. """
    return navigation_at_level(current_page=current_page, css_class='secondary')


@register.inclusion_tag('glitter/navigation/level.html')
def tertiary_navigation(current_page=None, css_class='tertiary'):
    """ Render a list of tertiary level pages. """
    return navigation_at_level(current_page=current_page, level=2, css_class='tertiary')
