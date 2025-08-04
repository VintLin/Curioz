import markdown
import bleach
from bleach.sanitizer import ALLOWED_TAGS, ALLOWED_ATTRIBUTES

def convert_markdown_to_html(text):
    """将Markdown文本转换为安全的HTML"""
    if not text:
        return ""
        
    # 允许的HTML标签
    allowed_tags = list(ALLOWED_TAGS) + ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'img', 
                                         'pre', 'code', 'blockquote', 'hr', 'table', 'thead', 
                                         'tbody', 'tr', 'th', 'td', 'ul', 'ol', 'li', 'span']
    
    # 允许的属性
    allowed_attrs = dict(ALLOWED_ATTRIBUTES)
    allowed_attrs['img'] = ['src', 'alt', 'title', 'width', 'height']
    allowed_attrs['a'] = ['href', 'title', 'target']
    allowed_attrs['code'] = ['class']
    allowed_attrs['span'] = ['class']
    
    # 转换Markdown为HTML
    html = markdown.markdown(
        text,
        extensions=[
            'markdown.extensions.fenced_code',  # 支持```代码块
            'markdown.extensions.tables',       # 支持表格
            'markdown.extensions.nl2br',        # 支持换行
            'markdown.extensions.sane_lists',   # 更好的列表支持
        ]
    )
    
    # 清理HTML，防止XSS攻击
    clean_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )
    
    return clean_html
