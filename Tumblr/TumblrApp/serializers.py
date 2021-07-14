import json

from rest_framework import serializers

from .models import *


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file', 'post')

    def get_queryset(self):
        return self.Meta.model.objects.all()


class DataSerializer(object):
    class Meta:
        fields = '__all__'

    def get_data(self, obj):
        pass

    def create_data(self, obj):
        pass

    def update_data(self, **kwargs):
        pass

    def delete_data(self, **kwargs):
        pass


class TextData(DataSerializer):
    def __init__(self):
        self.serializer = TextSerializer

    def get_data(self, obj):
        return self.serializer(self.serializer.Meta.model.objects.get(post_id=obj.id)).data

    def create_data(self, **kwargs):
        data = self.serializer.Meta.model.objects.create(**kwargs)
        return self.serializer(data)

    def update_data(self, obj, **kwargs):
        instance = self.serializer.Meta.model.objects.get(post_id=obj.id)
        for (key, value) in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        instance.save()
        return self.serializer(instance)

    def delete_data(self, obj):
        self.serializer.Meta.model.objects.get(post_id=obj.id).delete()


class LinkData(DataSerializer):
    def __init__(self):
        self.serializer = LinkSerializer

    def get_data(self, obj):
        return self.serializer(self.serializer.Meta.model.objects.get(post_id=obj.id)).data

    def create_data(self, **kwargs):
        data = self.serializer.Meta.model.objects.create(**kwargs)
        return self.serializer(data)

    def update_data(self, obj, **kwargs):
        instance = self.serializer.Meta.model.objects.get(post_id=obj.id)
        for (key, value) in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        instance.save()
        return self.serializer(instance)

    def delete_data(self, obj):
        self.serializer.Meta.model.objects.get(post_id=obj.id).delete()


class NoneData(DataSerializer):
    def __init__(self):
        self.serializer = FileSerializer

    def get_data(self, obj):
        return list()

    def create_data(self, **kwargs):
        return dict()

    def update_data(self, obj, **kwargs):
        return dict()

    def delete_data(self, obj):
        pass


class BasePostData(object):

    def __init__(self, strategy):
        self.strategy = strategy

    def get_data(self, obj):
        return self.strategy.get_data(obj)

    def create_data(self, **kwargs):
        return self.strategy.create_data(**kwargs)

    def update_data(self, obj, **kwargs):
        return self.strategy.update_data(obj, **kwargs)

    def delete_data(self, obj):
        return self.strategy.delete_data(obj)


class PostSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()
    content_data = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'post_type', 'content_data', 'likes', 'tags', 'files')

    def get_queryset(self):
        return self.Meta.model.objects.all()

    def get_files(self, obj):
        data = File.objects.filter(post=obj.id)
        if len(data) > 0:
            return FileSerializer(data, many=True).data
        else:
            return list()

    def get_strategy(self, type):
        if type.lower() == 'text':
            return TextData()
        elif type.lower() == 'link':
            return LinkData()
        else:
            return NoneData()

    def get_content_data(self, obj):
        strategy = self.get_strategy(obj.post_type)
        solver = BasePostData(strategy)
        return solver.get_data(obj)

    def create(self, validated_data):
        content_data = validated_data.pop('content_data', dict())
        files = validated_data.pop('files', list())
        post = Post.objects.create(**validated_data)
        strategy = self.get_strategy(post.post_type)
        solver = BasePostData(strategy)
        if isinstance(content_data, str):
            content_data = json.loads(content_data)
        content_data['post_id'] = post.id
        solver.create_data(**content_data)
        if len(files) > 0:
            files_data = [File(post=post, file=file) for file in files]
            File.objects.bulk_create(files_data)
        return PostSerializer(post)

    def update(self, instance, validated_data):
        content_data = validated_data.pop('content_data', dict())
        files = validated_data.pop('files', list())
        for (key, value) in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        instance.save()
        if isinstance(content_data, str):
            content_data = json.loads(content_data)
        strategy = self.get_strategy(instance.post_type)
        solver = BasePostData(strategy)
        solver.update_data(instance, **content_data)
        return PostSerializer(instance)

    def delete(self, obj):
        strategy = self.get_strategy(obj.post_type)
        solver = BasePostData(strategy)
        solver.delete_data(obj)
        obj.delete()
        return


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ('text1', 'text2', 'type')

    def get_queryset(self):
        return self.Meta.model.objects.all()


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('url', 'caption', 'type')

    def get_queryset(self):
        return self.Meta.model.objects.all()
