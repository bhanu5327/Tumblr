from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from rest_framework import status
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class PostCrudView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = serializer_class().get_queryset()

    def get(self, request, *args, **kwargs):
        filters = request.GET.copy()
        if 'pk' in kwargs:
            try:
                data = self.serializer_class(self.queryset.get(pk=kwargs['pk']))
            except ObjectDoesNotExist as e:
                return Response({'error': "No data with such ID found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            if 'type' in kwargs:
                typedict = {'blog': 'text', 'quote': 'text', 'bookmark': 'link', 'image': 'link', 'video': 'link',
                            'github': 'link'}
                if kwargs['type'] not in typedict:
                    return Response({'error': "No data with such BlogType found"}, status=status.HTTP_404_NOT_FOUND)
                data1 = self.serializer_class(self.queryset.all().filter(post_type=typedict[kwargs['type']]), many=True)
                postlist = []
                for i in data1.data:
                    if i['content_data']['type'].lower() == kwargs['type'].lower():
                        postlist.append(i)
                return Response(postlist, status=status.HTTP_200_OK)
            else:
                if len(filters):
                    pass
                data = self.serializer_class(self.queryset.all(), many=True)
        return Response(data.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        body = request.data
        body['files'] = request.FILES.getlist('files')
        data = self.serializer_class().create(body)
        return Response(data.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        if 'pk' not in kwargs:
            return Response({'error': "No ID found"}, status=status.HTTP_404_NOT_FOUND)
        body = request.data
        try:
            instance = self.queryset.get(pk=kwargs['pk'])
        except ObjectDoesNotExist as e:
            return Response({'error': "No data with such ID found"}, status=status.HTTP_404_NOT_FOUND)
        data = self.serializer_class().update(instance, body)
        return Response(data.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        if 'pk' not in kwargs:
            return Response({'error': "No ID found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            instance = self.queryset.get(pk=kwargs['pk'])
        except ObjectDoesNotExist as e:
            return Response({'error': "No data with such ID found"}, status=status.HTTP_404_NOT_FOUND)
        self.serializer_class().delete(instance)
        return Response({'message': 'Deleted Successfully'}, status=status.HTTP_201_CREATED)


class PostFileCrudView(ListCreateAPIView, DestroyAPIView):
    serializer_class = FileSerializer
    queryset = serializer_class().get_queryset()

    def get(self, request, *args, **kwargs):
        data = None
        try:
            if 'pk' not in kwargs:
                return Response({'error': "No Post ID given"}, status=status.HTTP_404_NOT_FOUND)
            else:
                if 'pk2' not in kwargs:
                    data = self.serializer_class(self.queryset.filter(post_id=kwargs['pk']), many=True)
                else:
                    data = self.serializer_class(self.queryset.get(pk=kwargs['pk2'], post_id=kwargs['pk']))
            return Response(data.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({'error': "No data with such ID found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        try:
            if 'pk' not in kwargs:
                return Response({'error': "No Post ID given"}, status=status.HTTP_404_NOT_FOUND)
            else:
                post = Post.objects.get(pk=kwargs['pk'])
                if len(files) > 0:
                    files_data = [File(post=post, file=file) for file in files]
                    File.objects.bulk_create(files_data)
            return self.get(request, *args, **kwargs)
        except ObjectDoesNotExist as e:
            return Response({'error': "No POST with such ID found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        data = None
        try:
            if 'pk' not in kwargs:
                return Response({'error': "No Post ID given"}, status=status.HTTP_404_NOT_FOUND)
            else:
                if 'pk2' not in kwargs:
                    data = self.queryset.filter(post_id=kwargs['pk'])
                else:
                    data = self.queryset.get(pk=kwargs['pk2'], post_id=kwargs['pk'])
            data.delete()
            return Response({'message': 'Deleted Successfully'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({'error': "No data with such ID found"}, status=status.HTTP_404_NOT_FOUND)


class DownloadFile(APIView):

    def get(self, request, *args, **kwargs):
        if 'pk' not in kwargs:
            return Response({'error': "No File ID given"}, status=status.HTTP_404_NOT_FOUND)
        else:
            file = File.objects.get(pk=kwargs['pk'])
            return FileResponse(open(file.file.name, 'rb'))
