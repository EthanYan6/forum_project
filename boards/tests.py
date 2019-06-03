from django.core.urlresolvers import reverse
from django.test import TestCase
from django.urls import resolve
from boards.views import home, board_topics
from boards.models import Board


class HomeTest(TestCase):
    def test_home_view_status_code(self):
        url = reverse('boards:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)


class BoardTopicsTests(TestCase):
    def setUp(self):
        # 准备运行测试环境,用来模拟场景
        Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        # 测试Django是否对于现有的Board 返回status code状态码
        url = reverse('board_topics: board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_toopics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEqual(view.func, board_topics())
