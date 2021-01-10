# coding=utf-8
import jinja2


FIXED_IMAGE_HEIGHT = 34

_source = """
<div class="main">
<div id="news_top">
  <h1 class="news_title">{{ title|safe }}</h1>
  <div class="news_source">
    {%if source.pic%}
    <div class="source_pic">
      <img src="{{ source.pic }}" width="{{ source.icon_width }}" height="{{ source.icon_height }}"/>
    </div>
    {%endif%}
    <div class="source_name">{{ source.name }}</div>
    <div class="source_time">
      <span class="news_date">{{ published_at.strftime('%Y-%m-%d') }}</span>
      <span class="news_time">{{ published_at.strftime('%H:%M:%S') }}</span>
    </div>
  </div>
</div>
<div id="news_body">{{ content|safe }}</div>
</div>
"""


tpl = jinja2.Template(_source)


def scale_bound(w, h, fixed_h=FIXED_IMAGE_HEIGHT):
    if w <= 0 or h <= 0:
        return fixed_h, fixed_h
    _w = w * (fixed_h / float(h))
    return int(_w), fixed_h


def render_article(title, published_at, content, source):
    """
    渲染文章数据到客户端/h5可以使用的文本
    source: name, pic, icon_width, icon_height
    :type title: str | unicode
    :type published_at: datetime.datetime
    :type content: unicode
    :type source: dict
    """
    w = source['icon_width']
    h = source['icon_height']
    _w, _h = scale_bound(w, h)
    source['icon_height'] = _h
    source['icon_width'] = _w
    return tpl.render(
        title=title, published_at=published_at, content=content, source=source)
