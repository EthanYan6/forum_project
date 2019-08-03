from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from django.urls import resolve
from boards.views import board_topics
from boards.models import Board


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

