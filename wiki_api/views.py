from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import WikiPage
from .serializers import WikiPageSerializer


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_wiki_page(request, pk):
    try:
        page = WikiPage.objects.get(pk=pk)
    except WikiPage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single page
    if request.method == 'GET':
        serializer = WikiPageSerializer(page)
        return Response(serializer.data)

    # update details of a single page and create new version
    if request.method == 'PUT':
        data = {
            'title': request.data.get('title'),
            'text': request.data.get('text')
        }
        page = WikiPage.objects.update(page)
        serializer = WikiPageSerializer(page, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a single page
    if request.method == 'DELETE':
        page.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def get_post_wiki_page(request):
    # get all pages
    if request.method == 'GET':
        pages = WikiPage.objects.pages()
        serializer = WikiPageSerializer(pages, many=True)
        return Response(serializer.data)
    # insert a new record for a page
    elif request.method == 'POST':
        page = {
            'title': request.data.get('title'),
            'text': request.data.get('text')
        }
        serializer = WikiPageSerializer(data=page)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_page_versions(request, uuid):
    if request.method == 'GET':
        pages = WikiPage.objects.filter(uuid=uuid).order_by('-version')
        serializer = WikiPageSerializer(pages, many=True)
        return Response(serializer.data)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_version(request, uuid, version):
    if request.method == 'GET':
        page = WikiPage.objects.pages_version(uuid=uuid, version=version)
        serializer = WikiPageSerializer(page)
        return Response(serializer.data)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT'])
def get_current_version(request, uuid, version=None):
    if request.method == 'GET':
        page = WikiPage.objects.pages_current_version(uuid=uuid)
        serializer = WikiPageSerializer(page)
        return Response(serializer.data)
    elif request.method == 'PUT':
        WikiPage.objects.filter(uuid=uuid).update(is_current=False)
        page = WikiPage.objects.pages_version(uuid=uuid, version=version)
        page.is_current = True
        page.save()
        serializer = WikiPageSerializer(page)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_404_NOT_FOUND)
