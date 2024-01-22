from django.shortcuts import render
from . import util
import markdown

def markdown_to_html(title):
    markdowner = markdown.Markdown()
    if util.get_entry(title) == None:
        return None
    else:
        return markdowner.convert(util.get_entry(title))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })





def entry(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/entry_not_found.html", {
            "message": "Requested page was not found"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": util.get_entry(title)
        })