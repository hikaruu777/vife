from datetime import datetime
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse


from .models import Category, Post


class CategoryTests(TestCase):

    @patch('django.utils.timezone.now', return_value=datetime(2020, 1, 1, 0, 0, 0))
    def setUp(self, _mock_now):
        self.category1 = Category.objects.create(
            name='band T',
            slug='band_t',
        )
        self.post1 = Post.objects.create(
            title='the cure',
            category=self.category1,
            is_public=True,
        )

        _mock_now.return_value = datetime(2020, 1, 1, 1, 1, 1)

        self.category2 = Category.objects.create(
            name='anime T',
            slug='anime_t',
        )
        self.post2 = Post.objects.create(
            title='party',
            category=self.category2,
            is_public=True,
        )
        self.post3 = Post.objects.create(
            title='metallica',
            category=self.category1,
            is_public=True,
        )

    def test_timestamp_with_mock(self):
        self.assertEqual(self.category1.timestamp, datetime(2020, 1, 1, 0, 0, 0))
        self.assertEqual(self.category2.timestamp, datetime(2020, 1, 1, 1, 1, 1))

    def test_category_list_view(self):
        response = self.client.get(reverse('posts:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'band T (2)')
        self.assertContains(response, 'anime T (1)')
        self.assertTemplateUsed(response, 'posts/category_list.html')

    def test_category_post_view(self):
        response = self.client.get(reverse('posts:category_post', kwargs={'category_slug': self.category1.slug}))
        no_response = self.client.get(reverse('posts:category_post', kwargs={'category_slug': '1500'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, '"band T" POSTS LIST')
        self.assertContains(response, 'the cure')
        self.assertContains(response, 'metallica')
        self.assertTemplateUsed(response, 'posts/category_post.html')


class PostTests(TestCase):

    @patch('django.utils.timezone.now', return_value=datetime(2020, 1, 1, 0, 0, 0))
    def setUp(self, _mock_now):

        self.category1 = Category.objects.create(
            name='band T',
            slug='band_t',
        )
        self.post1 = Post.objects.create(
            title='the cure',
            category=self.category1,
            is_public=True,
        )

        _mock_now.return_value = datetime(2020, 1, 1, 1, 1, 1)

        self.category2 = Category.objects.create(
            name='anime T',
            slug='anime_t',
        )
        self.post2 = Post.objects.create(
            title='party',
            category=self.category2,
            is_public=True,
        )

        _mock_now.return_value = datetime(2020, 1, 1, 7, 7, 7)

        self.post1.save()

        self.post3 = Post.objects.create(
            title='metallica',
            category=self.category1,
            is_public=False,
        )

        _mock_now.return_value = datetime(2020, 1, 1, 11, 11, 11)

        self.post4 = Post.objects.create(
            title='peach',
            category=self.category2,
            is_public=True,
        )

    def test_created_at_with_mock(self):
        self.assertEqual(self.post1.created_at, datetime(2020, 1, 1, 0, 0, 0))
        self.assertEqual(self.post2.created_at, datetime(2020, 1, 1, 1, 1, 1))

    def test_updated_at_with_mock(self):
        self.assertEqual(self.post1.updated_at, datetime(2020, 1, 1, 7, 7, 7))
        self.assertEqual(self.post2.updated_at, datetime(2020, 1, 1, 1, 1, 1))

    def test_index_view(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'peach')
        self.assertContains(response, 'the cure')
        self.assertNotContains(response, 'metallica')
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_index_view_save_book(self):
        self.post2.title = 'cream'
        self.post2.save()
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'cream')
        self.assertContains(response, 'peach')

    def test_index_view_with_login(self):
        pass

    def test_display_order(self):
        pass

    def test_post_detail(self):
        response = self.client.get(reverse('posts:post_detail', kwargs={'pk': self.post1.id}))
        no_response = self.client.get(reverse('posts:post_detail', kwargs={'pk': '12345678-1234-1234-1234-1234567890ab'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'the cure')
        self.assertContains(response, 'band T')
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_search_post_view(self):
        url = '{url}?{filter}={value}'.format(url=reverse('posts:search_post'), filter='q', value='band')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '「band」の検索結果 (2 posts)')
        self.assertContains(response, 'the cure')
        self.assertNotContains(response, 'metallica')

    def test_search_post_view_no_posts(self):
        url = '{url}?{filter}={value}'.format(url=reverse('posts:search_post'), filter='q', value='2000')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '「2000」の検索結果')
        self.assertNotContains(response, 'the cure')
        self.assertNotContains(response, 'peach')
