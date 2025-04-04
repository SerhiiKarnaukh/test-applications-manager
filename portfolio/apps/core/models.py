from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='Slug', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:category_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, verbose_name='Slug', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:tag', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['title']


class Project(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to='portfolio/projects/', blank=True)
    github_url = models.URLField(max_length=200)
    view_url = models.URLField(max_length=200)
    slug = models.SlugField(max_length=255, verbose_name='Slug', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 related_name='projects')
    tags = models.ManyToManyField(Tag, blank=True, related_name='projects')
    ordering = models.PositiveIntegerField(default=0, verbose_name="Ordering")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:project_detail',
                       args=[self.category.slug, self.slug])

    class Meta:
        verbose_name_plural = 'Projects'
        ordering = ['-created_at']


class ProjectGallery(models.Model):
    project = models.ForeignKey(Project,
                                related_name='projectgallery',
                                default=None,
                                on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio/project_gallery/', max_length=255)

    def __str__(self):
        return self.project.title

    class Meta:
        verbose_name = 'projectgallery'
        verbose_name_plural = 'project gallery'
