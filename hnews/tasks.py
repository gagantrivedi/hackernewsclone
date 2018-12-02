import requests
from bs4 import BeautifulSoup
from celery import shared_task
from dateparser import parse

from django.utils import timezone
import pytz
from django.contrib.contenttypes.models import ContentType
from django_comments.models import Comment
from hnews.models import Post
user_type = ContentType.objects.get(app_label='hnews', model='post')

timezone.activate(pytz.timezone("Asia/Kolkata"))


def has_class_but_no_id(tag):
    return tag.name == 'a' and 'item' in tag.attrs['href'] and 'comments' in tag.text


@shared_task
def fetch_posts():
    # just to make the ordering same as hacker news
    Post.objects.filter().update(rank_is_expired=True)
    home_page = requests.get('https://news.ycombinator.com/')
    if home_page.status_code == 200:
        soup = BeautifulSoup(home_page.text, 'html.parser')
        link_list = soup.find_all("a", {"class": "storylink"})
        points_list = soup.find_all("span", {"class": "score"})
        created_time_list = soup.find_all("span", {"class": "age"})
        hn_id_list = soup.find_all("tr", {"class": "athing"})
        total_comments_list = soup.find_all(has_class_but_no_id)

        for i, (link, points, created_time, hn_id, comment) in enumerate(
                zip(link_list, points_list, created_time_list, hn_id_list, total_comments_list)):
            print(i)

            post = Post.objects.update_or_create(
                hn_post_id=int(hn_id.attrs['id']),
                defaults={'title': link.text,
                          'url': link.get('href'),
                          'total_votes': points.text.split(' ')[0],
                          'created_at': pytz.timezone("Asia/Kolkata").localize(parse(created_time.text)),
                          'hn_rank': i + 1,
                          'total_comments': int(
                              comment.text.encode('ascii', 'ignore').decode('ascii').replace('comments', ''))
                          },
            )
            url = 'https://news.ycombinator.com/' + comment.attrs['href']
            comment_page = requests.get(url)
            if comment_page.status_code == 200:
                comment_soup = BeautifulSoup(comment_page.text)
                comment_list = comment_soup.find_all("span", {"class": "commtext c00"})
                for comment in comment_list:
                    print post[0]
                    Comment.objects.create(content_type=user_type, site_id=1, content_object=post[0],
                                                     object_pk=post[0].id,
                                                     comment=comment.text)



