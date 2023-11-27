from rest_framework import viewsets
from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        return serializers.RecipeSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name')
        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__startswith=name)
        return queryset.all().order_by('-name')

    def create(self, request, *args, **kwargs):
        return super(RecipeViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(RecipeViewSet, self).update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super(RecipeViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(RecipeViewSet, self).retrieve(request, *args, **kwargs)
