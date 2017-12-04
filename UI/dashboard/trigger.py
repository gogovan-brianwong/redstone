# -*- coding: utf-8 -*-
import json

import redis
import time
from channels import Group
from django.conf import settings

from Infrastructure.public import JsonCustomSerializer
from UI.dashboard import const
from UI.dashboard.views import get_top_restart_pod, list_resources


# logger = logging.getLogger(__name__)


class WSTrigger():
    """
    Command to start blogging worker from command line.
    """
    help = 'Fetch and parse RSS feed and send over channel'

    def handler(self, *args, **options):
        rc = redis.Redis(host=settings.REDIS_OPTIONS['HOST'],
                         port=settings.REDIS_OPTIONS['PORT'],
                         db=settings.REDIS_OPTIONS['DB'])
        rc.delete(const.GROUP_NAME)
        # flush live blogs
        # while True:
        #     feed = feedparser.parse(const.IFANR_FEED_URL)
        #     for entry in feed.get('entries')[::-1]:
        #         if not rc.hexists(const.GROUP_NAME, entry.get('id')):
        #             Group(const.GROUP_NAME).send({'text': json.dumps(entry)})
        #             rc.hset(const.GROUP_NAME, entry.get('id'), json.dumps(entry))
        #             logger.debug('send a message %s ' % entry.get('title'))
        #             time.sleep(5)
        while True:
            # now_time = time.time()
            Group(const.GROUP_NAME).send({"text": json.dumps({'data1': get_top_restart_pod(),'data2':list_resources()},cls=JsonCustomSerializer)})
            time.sleep(15)