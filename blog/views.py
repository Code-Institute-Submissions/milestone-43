from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import BlogPost
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm


# Create your views here.


def all_blogs(request):
    """ A view to return the blog page """

    blogs = BlogPost.objects.all().order_by('-post_date')

    context = {
        'blogs': blogs,
    }
    return render(request, 'blog/blog.html', context)



@login_required
def add_blog(request):
    """ Add a blog to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse, 'home')

    if request.method == 'POST':
        blog = BlogPostForm(request.POST, request.FILES)
        if blog.is_valid():
            blog = blog.save()
            messages.success(request, 'Successfully added blog!')
            return redirect(reverse('all_blogs'))
        else:
            messages.error(request, 'Failed to add blog. Please ensure the form is valid.')
    else:
        blog = BlogPostForm()

    template = 'blog/add_blog.html'
    context = {
        'blog': blog,
    }

    return render(request, template, context)


@login_required
def edit_blog(request, blog_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse, 'home')

    blog = get_object_or_404(BlogPost, pk=blog_id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('blog_detail', args=[blog.id]))
        else:
            messages.error(request, 'Failed to update blog. Please ensure the form is valid.')
    else:
        form = BlogPostForm(instance=blog)
        messages.info(request, f'You are editing {blog.title}')

    template = 'blog/edit_blog.html'
    context = {
        'form': form,
        'blog': blog,
    }

    return render(request, template, context)

@login_required
def delete_blog(request, blog_id):
    """ Delete a blog from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse, 'home')

    blog = get_object_or_404(BlogPost, pk=blog_id)
    blog.delete()
    messages.success(request, 'Blog deleted!')
    return redirect(reverse('all_blogs'))





def blog_detail(request, blog_id):
    """ A view to show individual blog posts """

    blog = get_object_or_404(BlogPost, pk=blog_id)
    total_likes = blog.total_likes

    liked = False
    if blog.likes.filter(id=request.user.id).exists():
        liked = True

    context = {
        'blog': blog,
        'total_likes': total_likes,
        'liked': liked,
    }

    return render(request, 'blog/blog_details.html', context)

# like_view taken from Codemy online tutorial
def like_view(request, pk):
    blog = get_object_or_404(BlogPost, id=request.POST.get('blog_id'))
    liked = False
    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
        liked = False
    else:
        blog.likes.add(request.user)
        liked = True
  
    return HttpResponseRedirect(reverse('blog_detail', args=[str(pk)]))


@login_required
def add_comment(request):
    """ Add a product to the store """
    if not request.user.authenticated:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse, 'home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
