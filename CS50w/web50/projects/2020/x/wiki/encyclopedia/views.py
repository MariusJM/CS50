from django.shortcuts import render
from . import util
import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def markdown_to_html(title):
    markdowner = markdown.Markdown()
    if util.get_entry(title) == None:
        return None
    else:
        return markdowner.convert(util.get_entry(title))


def entry(request, title):
    content = markdown_to_html(title)
    if content == None:
        return render(request, "encyclopedia/entry_not_found.html", {
            "message": "Requested page was not found"
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
            found = []
            for item in util.list_entries():
                if query.lower() in item.lower():
                    found.append(item)
            return render(request, "encyclopedia/index.html", {
                "entries": found
            })