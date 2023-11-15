from rest_framework import serializers
from core.models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id','name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'ingredients']
        read_only_fields = ['id']

    def _add_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            Ingredient.objects.create(
                **ingredient,
                recipe=recipe
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        recipe = Recipe.objects.create(**validated_data)
        if ingredients:
            self._add_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance: Recipe, validated_data):
        ingredients = validated_data.pop("ingredients", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)

        if ingredients:
            instance.ingredients.all().delete()
            self._add_ingredients(ingredients, instance)

        instance.save()
        return instance
