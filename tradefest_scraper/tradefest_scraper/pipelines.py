# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class TradefestImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        """
        Getting the custom name for the image file.
        """
        image_name = {'image_name': item.get('image_name')}
        media_requests = [
            Request(x, meta=image_name)
            for x in item.get(self.images_urls_field, [])
        ]
        return media_requests

    def file_path(self, request, response=None, info=None):
        """
        Setting the custom name for the image file.
        """
        image_guid = request.meta.get('image_name')
        return 'images/%s.jpg' % (image_guid)
