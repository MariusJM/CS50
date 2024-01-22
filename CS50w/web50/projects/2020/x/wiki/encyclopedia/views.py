from django.shortcuts import render
from . import util
from markdown import markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def markdown_to_html(title):
    title_saved = util.get_entry(title)
    markdowner = markdown()

    if title_saved == None:
        return None
    else:
        return markdowner.convert(title_saved)
