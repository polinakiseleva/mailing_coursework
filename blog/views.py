from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import BlogPostForm
from blog.models import Blog
from mailing.forms import StyleFormMixin


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Blog
    form_class = BlogPostForm
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.add_blog'

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()
        return super().form_valid(form)


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    extra_context = {'title': 'Все статьи', }
    permission_required = 'blog.view_blog'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    form_class = BlogPostForm
    permission_required = 'blog.view_blog'
    success_url = reverse_lazy('blog:view')
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogPostForm
    permission_required = 'blog.change_blog'

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()
        return super().form_valid(form)


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.delete_blog'


@permission_required('blog.delete_blog')
def toggle_activity(request, pk):
    article_item = get_object_or_404(Blog, pk=pk)
    if article_item.is_published:
        article_item.is_published = False
    else:
        article_item.is_published = True
    article_item.save()
    return redirect(reverse('blog:list'))
