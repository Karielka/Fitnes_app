from django import template
import re

register = template.Library()

@register.filter
def youtube_embed(url):
    match = re.search(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})', url)
    if match:
        return match.group(6)
    return None
