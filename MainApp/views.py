from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from MainApp.models import Snippet
from MainApp.forms import SnippetForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


@login_required
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': snippets
        }
    return render(request, 'pages/view_snippets.html', context)


@login_required(login_url='home')
def add_snippet_page(request):
    # Создаем пустую форму при запросе методом GET
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
            }
        return render(request, 'pages/add_snippet.html', context)
    
    # Получаем данные из формы и на их основе создаем новый Сниппет в БД
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save() 
            return redirect("snippets-list")
        return render(request, "pages/add_snippet.html", {'form': form})


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
        }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"Snippet with id={snippet_id} not found")
    else:
        context = {
            "pagename": "Просмотр сниппета",
            "snippet": snippet,
            "type": "view"
        }
        return render(request, "pages/snippet_detail.html", context)


def snippet_edit(request, snippet_id: int):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        return Http404
    
    # Variant 1
    # Хотим получить страницу с данными сниппета
    if request.method == "GET":
        context = {
            "pagename": "Редактирование сниппета",
            "snippet": snippet,
            "type": "edit"
        }
        return render(request, "pages/snippet_detail.html", context)
    
    # Variant 2
    # ==================================================================
    # Получение сниппета с помощью формы SnippetForm
    # if request.method == "GET":
    #     form = SnippetForm(instance=snippet)
    #     return render(request, "pages/add_snippet.html", {"form": form})
    # ==================================================================

    # Хотим использовать данные из формы и сохранить изменения в базе
    if request.method == "POST":
        data_form = request.POST
        # Есть экземпляр класса Snippet и новые данные в словаре data_form 
        # что нужно: взять данные из data_form и заменить ими значения атрибутов экземпляра snippet
        # как это сделать?
        snippet.name = data_form["name"]
        snippet.code = data_form["code"]
        if (change_date := data_form.get("creation_date")):
            snippet.creation_date = change_date
        # сохраняем этот изменения в базу
        snippet.save()
        return redirect("snippets-list")


def snippet_delete(request, snippet_id: int):
    snippet = Snippet.objects.get(id=snippet_id)
    snippet.delete()
    return redirect("snippets-list")


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print("username =", username)
        # print("password =", password)

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                "pagename": "PythonBin",
                "errors": ["wrong username or password"]
            }
            return render(request, "pages/index.html", context)
    return redirect("home")


def logout(request):
    auth.logout(request)
    return redirect('home')
