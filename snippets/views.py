from django.shortcuts import render, get_object_or_404, redirect
from .models import Snippet, Language, Tag
from .forms import SnippetForm, LanguageForm, TagForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView
from django.db.models import Q

# Create your views here.

# snippets


def list_snippet(request):
    snippets = Snippet.objects.all()
    return render(request, 'snippets/list_snippet.html', {'snippets': snippets})


def detail_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    return render(request, 'snippets/detail_snippet.html', {"snippet": snippet, "users": snippet.user.all(), "tags": snippet.tag.all(), "forks": snippet.forks.count()})


@login_required
def create_snippet(request):
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.author = request.user
            snippet.save()
            snippet.user.add(request.user)
            snippet.save()
            return redirect('detail_snippet', pk=snippet.pk)
    else:
        form = SnippetForm()
    return render(request, 'snippets/edit_snippet.html', {'form': form})


@login_required
def edit_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    if request.user != snippet.author:
        raise PermissionDenied()
    if request.method == "POST":
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            snippet = form.save()
            snippet.save()
            return redirect('detail_snippet', pk=snippet.pk)
    else:
        form = SnippetForm(instance=snippet)
    return render(request, 'snippets/edit_snippet.html', {'form': form})


@login_required
def delete_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    if request.user != snippet.author:
        raise PermissionDenied()
    snippet.delete()
    return redirect('list_snippet')


@login_required
def copy_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    user_old = list(snippet.user.all())
    tag_old = list(snippet.tag.all())
    # breakpoint()
    snippet.pk = None
    snippet.author = request.user
    snippet.parent = get_object_or_404(Snippet, pk=pk)
    snippet.save()
    for user in user_old:
        snippet.user.add(user)
    for tag in tag_old:
        snippet.tag.add(tag)
    return redirect('detail_snippet', pk=snippet.pk)


class SearchResultsView(ListView):
    model = Snippet
    template_name = 'snippets/search_snippet.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Snippet.objects.filter(Q(title__icontains=query) | Q(
            description__icontains=query) | Q(tag__name__icontains=query) | Q(language__name__icontains=query))
        return object_list


# languages
def list_language(request):
    languages = Language.objects.all()
    return render(request, 'snippets/list_language.html', {'languages': languages})


def detail_language(request, pk):
    language = get_object_or_404(Language, pk=pk)
    return render(request, 'snippets/detail_language.html', {"language": language})


@ login_required
def create_language(request):
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            language = form.save()
            return redirect('detail_language', pk=language.pk)
    else:
        form = LanguageForm()
    return render(request, 'snippets/edit_language.html', {'form': form})


@ login_required
def edit_language(request, pk):
    language = get_object_or_404(Language, pk=pk)
    if request.method == "POST":
        form = LanguageForm(request.POST, instance=language)
        if form.is_valid():
            language = form.save(commit=False)
            language.save()
            return redirect('detail_language', pk=language.pk)
    else:
        form = LanguageForm(instance=language)
    return render(request, 'snippets/edit_language.html', {'form': form})


@ login_required
def delete_language(request, pk):
    language = get_object_or_404(Language, pk=pk)
    language.delete()
    return redirect('list_language')


# tags
def list_tag(request):
    tags = Tag.objects.all()
    return render(request, 'snippets/list_tag.html', {'tags': tags})


def detail_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    return render(request, 'snippets/detail_tag.html', {"tag": tag})


@ login_required
def create_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            return redirect('detail_tag', pk=tag.pk)
    else:
        form = TagForm()
    return render(request, 'snippets/edit_tag.html', {'form': form})


@ login_required
def edit_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.save()
            return redirect('detail_tag', pk=tag.pk)
    else:
        form = TagForm(instance=tag)
    return render(request, 'snippets/edit_tag.html', {'form': form})


@ login_required
def delete_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    return redirect('list_tag')


# user
@ login_required
def user_profile(request):
    snippets = Snippet.objects.filter(
        user=request.user) | Snippet.objects.filter(author=request.user)
    return render(request, 'snippets/profile.html', {"snippets": snippets})
