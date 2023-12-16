import time

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.core.handlers.wsgi import WSGIRequest
from django.utils import timezone

from .models import Note


def home_page_view(request: WSGIRequest):
    # Обязательно! каждая функция view должна принимать первым параметром request.
    all_notes = Note.objects.all()  # Получение всех записей из таблицы этой модели.
    context: dict = {
        "notes": all_notes
    }
    return render(request, "home.html", context)


def show_note_view(request: WSGIRequest, note_uuid):
    try:
        note = Note.objects.get(uuid=note_uuid)  # Получение только ОДНОЙ записи.

    except Note.DoesNotExist:
        # Если не найдено такой записи.
        raise Http404

    return render(request, "note.html", {"note": note})


def create_note_view(request: WSGIRequest):
    if request.method == "POST":
        note = Note.objects.create(
            title=request.POST["title"],
            content=request.POST["content"],
        )
        return HttpResponseRedirect(reverse('show-note', args=[note.uuid]))

    # Вернется только, если метод не POST.
    return render(request, "create_form.html")


def edit_note_view(request: WSGIRequest, note_uuid):
    note = get_object_or_404(Note, uuid=note_uuid)
    if request.method == "GET":
        return render(request, "edit_form.html", context={'note': note})

    if request.method == 'POST':
        if not (request.POST['title'] == note.title and request.POST['content'] == note.content):
            note.title = request.POST['title']
            note.content = request.POST['content']
            note.mod_time = timezone.now()
            note.save()
        else:
            error = 'Изменений не было'
            return render(request, "edit_form.html", context={'note': note, 'error': error})
        return render(request, "note.html", {"note": note})


def delete_note_view(request: WSGIRequest, note_uuid):
    try:
        Note.objects.filter(uuid=note_uuid).delete()
    except Note.DoesNotExist:
        raise Http404

    return redirect('home')


def show_about_view(request: WSGIRequest):
    return render(request, "about.html")
