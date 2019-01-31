from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r'^api/v1/wiki/(?P<pk>[0-9]+)$',
        views.get_delete_update_wiki_page,
        name='get_delete_update_wiki_page'
    ),
    re_path(
        r'^api/v1/wiki/$',
        views.get_post_wiki_page,
        name='get_post_wiki_page'
    ),

    re_path(
        r'^api/v1/wiki/page/(?P<uuid>[0-9A-Fa-f-]+)/version$',
        views.get_page_versions,
        name='get_page_versions'
    ),

    re_path(
        r'^api/v1/wiki/page/(?P<uuid>[0-9A-Fa-f-]+)/version/(?P<version>[0-9]+)$',
        views.get_version,
        name='get_version'
    ),

    re_path(
        r'^api/v1/wiki/page/(?P<uuid>[0-9A-Fa-f-]+)/current/version$',
        views.get_current_version,
        name='get_current_version'
    ),

    re_path(
        r'^api/v1/wiki/page/(?P<uuid>[0-9A-Fa-f-]+)/current/version/(?P<version>[0-9]+)$',
        views.set_current_version,
        name='set_current_version'
    ),
]
