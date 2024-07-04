from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import PostSerializer, CommentSerializer, PostCreateSerializer

from .models import Post, Category, Tag, Comment
from .forms import CommentForm
from .filters import PostFilter


class BlogListView(ListView):
    model = Post
    paginate_by = 2
    template_name = "post/post_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['category'] = self.request.GET.get('category')
        context['tag'] = self.request.GET.get('tag')
        context['search_query'] = self.request.GET.get('search_query')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')
        tag_slug = self.request.GET.get('tag')
        query = self.request.GET.get('search_query')

        if query:
            queryset = queryset.filter(
                Q(name__iregex=query) | Q(description__iregex=query)
            )

        # if category_slug:
        #     queryset = queryset.filter(
        #         Q(category__slug=category_slug)
        #     )

        if category_slug:
            category = Category.objects.get(slug=category_slug)
            queryset = queryset.filter(category=category)

        if tag_slug:
            tag = Tag.objects.get(slug=tag_slug)
            queryset = queryset.filter(tags=tag)

        return queryset


class BlogDetailView(DetailView):
    model = Post
    template_name = "post/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comment_set.all()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url())
        return self.get(request, *args, **kwargs)


class BlogCreateView(SuccessMessageMixin, CreateView):
    model = Post
    template_name = "post/post_new.html"
    fields = ["name", "description", "featured_image", "tags", "category"]
    success_message = "%(name)s успешно создан"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(SuccessMessageMixin, UpdateView):
    model = Post
    template_name = "post/post_edit.html"
    fields = ["name", "description", "featured_image", "tags", "category"]
    success_message = "%(name)s успешно обновлен"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class BlogDeleteView(DeleteView):
    model = Post
    template_name = "post/post_delete.html"
    success_url = reverse_lazy("post_list")

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def handler404(request, exception):
    return render(request, 'error404.html', status=404)


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class CommentsViewSet(viewsets.ViewSet):
    serializer_class = CommentSerializer

    def list(self, request, post_pk=None):
        comments = Comment.objects.filter(post_id=post_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class PostCreateViewSet(CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        category_id = self.request.data.get('category')
        category_data = Category.objects.get(pk=category_id)

        tags = self.request.data.get('tags')
        data = []
        for i in tags:
            data.append(Tag.objects.get(pk=i))

        serializer.save(author=self.request.user, category=category_data, tags=data)



