from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def transform_GET_query(context, **kwargs):
    """
    Adds extra GET parameters to current ones.
    Ref: https://stackoverflow.com/questions/46026268/pagination-and-get-parameters
    """
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()


@register.simple_tag
def get_elided_page_range(page_obj, on_each_side=3, on_ends=2):
    """
    Returns a custom elided page range based on current page number.
    Ref: https://stackoverflow.com/questions/69277936/how-to-use-get-elided-page-range-in-django-paginator
    """
    page = page_obj
    paginator = page.paginator
    return paginator.get_elided_page_range(
        number=page.number,
        on_each_side=on_each_side,
        on_ends=on_ends
    )
