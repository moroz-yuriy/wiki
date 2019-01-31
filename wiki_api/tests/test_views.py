import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from ..models import WikiPage
from ..serializers import WikiPageSerializer

# initialize the APIClient app
client = Client()


class GetAllPagesTest(TestCase):
    """ Test module for GET all pages API """

    def setUp(self):
        self.page1 = WikiPage.objects.create(
            title='Test1',
            text='Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.',
        )

        self.page2 = WikiPage.objects.create(
            title='Test2',
            text='Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.',
        )

        self.page3 = WikiPage.objects.create(
            title='Test3',
            text='Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.',
        )

        data = {
            'title': 'test_version',
            'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.'

        }

        self.page4 = WikiPage.objects.update(self.page3)
        serializer = WikiPageSerializer(self.page4, data=data)
        if serializer.is_valid():
            serializer.save()

    def test_get_all_pages(self):
        # get API response
        response = client.get(reverse('get_post_wiki_page'))
        # get data from db
        pages = WikiPage.objects.pages()
        serializer = WikiPageSerializer(pages, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_version(self):
        # get API response
        response = client.get(reverse('get_page_versions', kwargs={'uuid': self.page3.uuid}))
        # get data from db
        pages = WikiPage.objects.filter(uuid=self.page4.uuid).order_by('-version')
        serializer = WikiPageSerializer(pages, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_version(self):
        # get API response
        response = client.get(
            reverse('get_version', kwargs={'uuid': self.page3.uuid, 'version': self.page4.version}))
        # get data from db
        page = WikiPage.objects.pages_version(uuid=self.page4.uuid, version=self.page4.version)
        serializer = WikiPageSerializer(page, )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['uuid'], serializer.data['uuid'])
        self.assertEqual(response.data['version'], serializer.data['version'])

    def test_get_current_version(self):
        # get API response
        response = client.get(
            reverse('get_current_version', kwargs={'uuid': self.page4.uuid}))
        # get data from db
        page = WikiPage.objects.pages_current_version(uuid=self.page4.uuid)
        serializer = WikiPageSerializer(page, )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['uuid'], serializer.data['uuid'])
        self.assertEqual(response.data['version'], serializer.data['version'])
        self.assertEqual(response.data['is_current'], serializer.data['is_current'])


class GetSinglePageTest(TestCase):
    """ Test module for GET single Page API """

    def setUp(self):
        self.page1 = WikiPage.objects.create(
            title='Test1',
            text='Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.',
        )

        self.page2 = WikiPage.objects.create(
            title='Test2',
            text='Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.',
        )

        self.page3 = WikiPage.objects.create(
            title='Test3',
            text='Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.',
        )

    def test_get_valid_single_page(self):
        response = client.get(reverse('get_delete_update_wiki_page', kwargs={'pk': self.page1.pk}))
        page = WikiPage.objects.get(pk=self.page1.pk)
        serializer = WikiPageSerializer(page)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_page(self):
        response = client.get(
            reverse('get_delete_update_wiki_page', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreatePageTest(TestCase):
    """ Test module for create page """

    def setUp(self):
        self.valid_payload = {
            'title': 'Test1',
            'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.',
        }
        self.invalid_payload = {
            'title': '',
            'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.',
        }

    def test_create_valid_page(self):
        response = client.post(
            reverse('get_post_wiki_page'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.valid_payload['title'])
        self.assertEqual(response.data['version'], 1)
        self.assertEqual(response.data['is_current'], True)

    def test_create_invalid_page(self):
        response = client.post(
            reverse('get_post_wiki_page'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSinglePageTest(TestCase):
    """ Test module for deleting an existing page record """

    def setUp(self):
        self.page = WikiPage.objects.create(
            title='Test1',
            text='Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.',
        )

    def test_valid_delete_page(self):
        response = client.delete(
            reverse('get_delete_update_wiki_page', kwargs={'pk': self.page.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_page(self):
        response = client.delete(
            reverse('get_delete_update_wiki_page', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateSinglePageTest(TestCase):
    """ Test module for update an existing page record """

    def setUp(self):
        self.page = WikiPage.objects.create(
            title='Test1',
            text='Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.',
        )

        self.page.save()

    def test_valid_update_page(self):
        data = {
            'title': 'New',
            'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.'
        }

        response = client.put(
            reverse('get_delete_update_wiki_page', kwargs={'pk': self.page.pk}),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['title'], 'New')
        self.assertEqual(response.data['version'], 2)
        self.assertEqual(response.data['is_current'], True)


class UpdatePageToCurrentTest(TestCase):
    """ Test module for set page record as current """

    def setUp(self):
        self.page1 = WikiPage.objects.create(
            title='Test3',
            text='Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.',
        )

        data = {
            'title': 'test_version',
            'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.'

        }

        self.page2 = WikiPage.objects.update(self.page1)
        serializer = WikiPageSerializer(self.page1, data=data)
        if serializer.is_valid():
            serializer.save()

    def test_set_page_as_current(self):
        # get API good response
        response = client.patch(
            reverse('set_current_version', kwargs={'uuid': self.page1.uuid, 'version': self.page1.version})
        )
        # get data from db
        page = WikiPage.objects.pages_version(uuid=self.page1.uuid, version=self.page1.version)
        serializer = WikiPageSerializer(page, )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['is_current'], True)
        self.assertEqual(response.data['is_current'], serializer.data['is_current'])


        # get API bad response
        response = client.patch(
            reverse('set_current_version', kwargs={'uuid': self.page1.uuid, 'version': 1000})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
