from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from django.urls import resolve
from boards.views import home, board_topics, new_topic
from boards.models import Board, Topic, Post
from ..forms import NewTopicForm


class HomeTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(id=1,name='Django',description='Django board.')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        url = reverse('home')
        # url = reverse('boards:home')
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))

    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))


class BoardTopicsTests(TestCase):
    def setUp(self):
        # 此处需要填写id,否则后面单元测试无法通过,结果未知
        Board.objects.create(id=1, name='Django', description='Django board.')
        User.objects.create(username='john', email='john@doe.com', password='123') # <- indluded this line here


    def test_board_topics_view_success_status_code(self):
        # 测试Django是否对于现有的Board 返回status code状态码
        url = reverse('board_topics', kwargs={'pk': 1})
        # print(url)
        # url = reverse('bt: board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        # 测试Django是否对于不存在于数据库的Board返回status code 404(页面未找到)
        url = reverse('board_topics', kwargs={'pk': 99})
        # url = reverse('bt: board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        # 测试Django是否使用了正确的视图函数去渲染topics
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        :return:
        """
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        :return:
        """
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(id=1,name='Django',description='Django board.')

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_contains_form(self): # <- new test
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        # 处理的是抓取的上下文的表单实例,检查它是否是一个NewTopicForm
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_invalid_post_data(self): # <- updated this one
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        :return:
        """
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)