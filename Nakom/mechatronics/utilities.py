from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def pagination(objects_list, page, objects_per_page=10):
    paginator = Paginator(objects_list, objects_per_page)

    try:
        objects_list = paginator.page(page)

    except PageNotAnInteger:
        objects_list = paginator.page(1)

    except EmptyPage:
        objects_list = paginator.page(paginator.num_pages)

    return objects_list
