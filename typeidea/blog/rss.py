from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from .models import Post


class ExtendedRSSFed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFed, self).add_item_elements(handler, item)
        handler.addQuickElement('content:html', item['content_html'])


class LatestPostFeed(Feed):
    # feed_type = ExtendedRSSFed
    title = 'Typeidea Blog System'
    link = '/'
    description = 'typeidea is blog system power by django'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:2]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_link(self, item):
        return reverse('post-detail', args=[item.pk, ])
