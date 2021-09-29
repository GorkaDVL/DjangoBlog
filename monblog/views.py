
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, PostForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

#def home(request):
#    return render(request, 'home.html', {})

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return HttpResponseRedirect(reverse('article-detail', args =[str(pk)]))

def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list': cat_menu_list})
    

def CategoryView(request, cats):
    category_posts = Post.objects.filter(category__iexact=cats.replace('-', ' '))
    return render(request, 'categories.html', {'cats': cats.title().replace('-', ' ') , 'category_posts':category_posts})


# Affiche tous les articles sur la page Home
class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    #ordering = ['-id']
    ordering = ['-post_date' ]

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


#Affiche le contenu d'un article sur la page article_details
class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'
    method = 'POST'
    
    def get_context_data(self, *args, **kwargs):

        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        liked = False
        post = Comment.objects.filter(
            post=self.get_object()).order_by('-date_added')
        context['comments'] = post
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm(instance=self.request.user)
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context




    def post(self, request, *args, **kwargs):
        new_comment = Comment(body=request.POST.get('body'),name=self.request.user, post=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)
        

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    #fields = '__all__'
    #fields = ('title', 'body')
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(AddPostView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


"""
class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'
    #fields = '__all__'



    def get_context_data(self, *args, **kwargs):
        comment = Comment.objects.all()
        post = Post.objects.all()
        context = super(AddCommentView, self).get_context_data(*args, **kwargs)
        context["comment"] = comment
        context["post"] = post
        return context




    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    
    def get_success_url(self):

        return reverse_lazy('article-detail', kwargs={'pk': self.kwargs['pk']})
    
   



 
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('home')
"""
class AddCategoryView(CreateView):
    model = Category
    #form_class = PostForm
    template_name = 'add_category.html'
    fields = '__all__'
    #fields = ('title', 'body')
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(AddCategoryView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'
    #fields = ['title', 'title_tag', 'body']
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(UpdatePostView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context
class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(DeletePostView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context