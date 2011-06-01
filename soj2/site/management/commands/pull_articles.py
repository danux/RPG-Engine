import urllib, datetime
from xml.dom import minidom

from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify

from mcnulty.news.models import NewsArticle


def read(node):
    """Reads the content of the node as a unicode object."""
    text = []
    for child in node.childNodes:
        if child.nodeType == child.TEXT_NODE or child.nodeType == child.CDATA_SECTION_NODE:
            text.append(child.data)
        elif child.nodeType == child.ELEMENT_NODE:
            text.extend(read(child))
    return u"".join(text)


def read_node(parent_node, child_name):
    return read(parent_node.getElementsByTagName(child_name)[0])


class Command(BaseCommand):
    
    help = "Output the contents of the database as a fixture of the given format."
    
    args = "[feed_id]"

    def handle(self, feed_id, **options):
        xml_data = urllib.urlopen("http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/education/rss.xml").read()
        document = minidom.parseString(xml_data)
        try:
            latest_article = NewsArticle.objects.filter(news_page__id=feed_id)[0]
        except IndexError:
            start_date = datetime.datetime(2009, 5, 28, 0, 0, 0)
        else:
            start_date = latest_article.date
            start_time = latest_article.time
            start_date = datetime.datetime(start_date.year, start_date.month, start_date.day, start_time.hour, start_time.minute, start_time.second)
        for item in document.getElementsByTagName("item"):
            title = read_node(item, "title")
            url_title = slugify(title)[:100]
            description = read_node(item, "description")
            date = datetime.datetime.strptime(read_node(item, "pubDate"), "%a, %d %b %Y %H:%M:%S %Z")
            if date > start_date:
                try:
                    NewsArticle.objects.create(news_page_id=feed_id, url_title=url_title, title=title, summary=description, date=date.date(), time=date.time())
                except:
                    pass
