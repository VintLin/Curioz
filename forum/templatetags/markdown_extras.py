from django import template
from django.template.defaultfilters import stringfilter
from ..utils import convert_markdown_to_html

register = template.Library()

@register.filter
@stringfilter
def markdown(value):
    """将Markdown文本转换为安全的HTML"""
    return convert_markdown_to_html(value)
