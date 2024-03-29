from django.shortcuts import render
from . import util
from markdown2 import Markdown
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def markdown_to_html(title):
    markdowner = Markdown()
    if util.get_entry(title) == None:
        return None
    else:
        return markdowner.convert(util.get_entry(title))


def entry(request, title):
    content = markdown_to_html(title)
    if content == None:
        return render(request, "encyclopedia/entry_not_found.html", {
            "message": f"Requested page '{title}' was not found"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })


def search(request):
    if request.method == "POST":
        query = request.POST.get('q')
        if query in util.list_entries():
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "content": markdown_to_html(query)
            })
        else:
            entries_found = []
            for item in util.list_entries():
                if query.lower() in item.lower():
                    entries_found.append(item)
            if len(entries_found) == 0:
                return render(request, "encyclopedia/entry_not_found.html", {
                    "message": f"No entries with name '{query}'"
                })
            else:
                return render(request, "encyclopedia/search_results.html", {
                    "entries": entries_found
                })


def add(request):
    if request.method == "GET":
        return render(request, "encyclopedia/add.html")
    else:
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/entry_not_found.html", {
                "message": f"Entry with name {title} allready exist"
            })
        else:
            util.save_entry(title,content)
            return render(request, "encyclopedia/entry.html",{
                "title": title,
                "content": markdown_to_html(title)
            })


def edit(request):
    if request.method == "POST":
        title = request.POST.get("entry_title")
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": util.get_entry(title)
        })
    

def save(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": markdown_to_html(title)
        })
    

def random_page(request):
    title = random.choice(util.list_entries())
    return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": markdown_to_html(title)
        })