from django.test import TestCase

from ..models import WikiPage


class WikiPageTest(TestCase):
    """ Test module for WikiPage model """

    def setUp(self):
        WikiPage.objects.create(
            title='Test',
            text='Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.',
            version=1,
            is_current=True
        )

    def test_title(self):
        page = WikiPage.objects.get(title='Test')
        self.assertEqual(page.title, 'Test')
        self.assertEqual(page.text,
                         'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.')
        self.assertEqual(page.version, 1)
        self.assertEqual(page.is_current, True)
