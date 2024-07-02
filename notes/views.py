from django.shortcuts import render, redirect
from .models import *
from django.http import Http404, HttpResponse, FileResponse
import os

# Create your views here.


def index(request):
    # Get the notes if exist!
    if request.user.is_authenticated:
        user_notes = Note.objects.filter(owner=request.user).order_by("-date_added")
        return render(request, "notes/index.html", {"notes": user_notes})

    return render(request, "notes/index.html")


def search(request):
    # Search the notes using query
    if request.user.is_authenticated:
        filter_word = request.GET.get("filter")
        if not filter_word:
            raise Http404

        # Filter out the notes
        notes = Note.objects.filter(owner=request.user, title__icontains=filter_word)
        return render(request, "notes/index.html", {"notes": notes, "filter_word": filter_word})

    return redirect("index")


def add(request):
    # Get the colors from the database
    colors = Color.objects.all()

    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        content = request.POST.get('content')
        color = request.POST.get('color')

        # Validate the data before adding to database
        message = ""
        if not title:
            message = "Title must not be empty!"
        elif not content:
            message = "Content must not be empty!"
        elif not color:
            message = "Color must not be empty"
        elif len(title) > 100:
            message = "Title must not exceed 100 characters!"
        elif len(desc) > 100:
            message = "Description must not exceed 100 characters!"
        elif len(color) != 6:
            message = "Invalid color code ({color})"
        elif not Color.objects.filter(code=color).first():
            message = "Color not in the database!"
        else:
            # All is well, Add note to database
            note = Note.objects.create(owner=request.user, title=title, description=desc,
                                       content=content, color=Color.objects.get(code=color))
            note.save()

            return redirect("index")

        return render(request, "notes/add.html", {"colors": colors, "message": message})

    return render(request, "notes/add.html", {"colors": colors})


def note(request, pk):
    colors = Color.objects.all()
    # Get the requested note
    try:
        note = Note.objects.get(owner=request.user, pk=pk)
    except:
        raise Http404

    # If user edited the note, Handle the POST request
    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        content = request.POST.get('content')
        color = request.POST.get('color')

        # Validate the data before adding to database
        message = ""
        if not title:
            message = "Title must not be empty!"
        elif not content:
            message = "Content must not be empty!"
        elif not color:
            message = "Color must not be empty"
        elif len(title) > 100:
            message = "Title must not exceed 100 characters!"
        elif len(desc) > 100:
            message = "Description must not exceed 100 characters!"
        elif len(color) != 6:
            message = "Invalid color code ({color})"
        elif not Color.objects.filter(code=color).first():
            message = "Color not in the database!"
        else:
            note.title = title
            note.description = desc
            note.content = content
            note.color = Color.objects.get(code=color)
            note.save()

            return render(request, "notes/note.html", {"user_note": note, "colors": colors, "message": "Note updated!", "status": "success"})

        return render(request, "notes/note.html", {"user_note": note, "colors": colors, "message": message})

    return render(request, "notes/note.html", {
        "user_note": note,
        "colors": colors
    })


def delete_note(request, note_id):
    # Get the note to delete
    note = Note.objects.get(pk=note_id)
    if note.owner == request.user:
        note.delete()

    return redirect("index")


def download_note(request, note_id):
    # Get the data regarding the note on note_id
    note = Note.objects.get(pk=note_id)
    if note.owner != request.user:
        raise Http404

    directory = f"notes/userdocs/txts/{note.owner.pk}"
    # If not exists, create dir
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename = f"{directory}/{note.title}.txt"

    # Create a text file in 'txts' folder
    with open(filename, "w") as file:
        # Write the content
        for line in note.content.splitlines():
            file.write(f"{line}\n")

    return FileResponse(open(filename, "rb"), as_attachment=True)


def duplicate_note(request, note_id):
    # Get the data regarding the note on note_id
    note = Note.objects.get(pk=note_id)
    if note.owner != request.user:
        raise Http404

    # Create another note with same data as 'note'
    Note.objects.create(owner=note.owner, title=note.title, description=note.description,
                        content=note.content, color=note.color, date_added=note.date_added).save()

    return redirect("index")


def about(request):
    return render(request, "notes/about.html")


def account(request):
    if not request.user.is_authenticated:
        return redirect("index")
    return render(request, "notes/account.html")
