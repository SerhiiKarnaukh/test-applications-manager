from django.test import TestCase, Client
from django.urls import reverse
from core.models import Category, Tag, Project, ProjectGallery
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


def get_temp_image():
    img_io = BytesIO()
    image = Image.new("RGB", (100, 100), color="blue")
    image.save(img_io, 'JPEG')
    img_io.seek(0)
    return SimpleUploadedFile("test.jpg", img_io.read(), content_type="image/jpeg")


class CoreViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(title="Vue.js", slug="vuejs")
        self.tag = Tag.objects.create(title="Web", slug="web")
        self.project = Project.objects.create(
            title="Vue Project",
            content="Awesome Vue.js project",
            photo=get_temp_image(),
            github_url="https://github.com/example/vue",
            view_url="https://example.com/vue",
            slug="vue-project",
            category=self.category,
            ordering=1
        )
        self.project.tags.add(self.tag)
        ProjectGallery.objects.create(project=self.project, image=get_temp_image())

    def test_category_detail_view(self):
        url = reverse('core:category_detail', kwargs={'slug': 'vuejs'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_project_detail_view(self):
        url = reverse('core:project_detail', args=['vuejs', 'vue-project'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)
        self.assertTemplateUsed(response, 'core/portfolio_detail.html')

    def test_project_search_list_view(self):
        url = reverse('core:search') + '?keyword=Vue'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_projects_by_tag_view(self):
        url = reverse('core:tag', kwargs={'slug': 'web'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)
        self.assertTemplateUsed(response, 'core/index.html')
