import uuid

from django.db import models


class WikiPageManager(models.Manager):
    @staticmethod
    def pages():
        return WikiPage.objects.filter(is_current=True).all()

    @staticmethod
    def pages_version(uuid, version):
        return WikiPage.objects.get(uuid=uuid, version=version)

    @staticmethod
    def pages_current_version(uuid):
        return WikiPage.objects.get(uuid=uuid, is_current=True)

    @staticmethod
    def update(page):
        new_page = WikiPage.objects.create()
        new_page.uuid = page.uuid
        new_page.version = page.version + 1
        new_page.is_current = True
        page.is_current = False
        page.save()
        return new_page

    def create(self, **obj_data):
        obj_data['is_current'] = True
        obj_data['version'] = 1
        obj_data['uuid'] = uuid.uuid4()
        return super().create(**obj_data)



class WikiPage(models.Model):
    """
    WikiPage model
    Defines the attributes of WikiPage
    """

    title = models.CharField(max_length=255)
    text = models.TextField()
    uuid = models.CharField(max_length=255, null=True)
    is_current = models.BooleanField(null=True)
    version = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = WikiPageManager()
