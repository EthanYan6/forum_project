from django.urls import reverse
from django.test import TestCase
from django.urls import resolve
from boards.views import home, board_topics, new_topic
from boards.models import Board


class HomeTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(id=1,name='Django',description='Django board.')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        url = reverse('home')
        # url = reverse('boards:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)

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


    def test_board_topics_view_success_status_code(self):
        # 测试Django是否对于现有的Board 返回status code状态码
        url = reverse('board_topics', kwargs={'pk': 1})
        # print(url)
        # url = reverse('bt: board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_toopics_view_not_found_status_code(self):
        # 测试Django是否对于不存在于数据库的Board返回status code 404(页面未找到)
        url = reverse('board_topics', kwargs={'pk': 99})
        # url = reverse('bt: board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        # 测试Django是否使用了正确的视图函数去渲染topics
        view = resolve('/boards/1/')
        self.assertEqual(view.func, board_topics)


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(id=1,name='Django',description='Django board.')

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEqual(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))