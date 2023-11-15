from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):

    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(**params):

    defaults = {
        'name': 'Sample recipe title',
        'description': 'Sample description',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(**defaults)
    return recipe


class RecipeAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipe(self):

        create_recipe(name='Pizza 1')
        create_recipe(name='Pasta 2')

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-name')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):

        recipe = create_recipe()

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):

        payload = {
            'name': 'Sample recipe',
            'description': 'Sample description',
        }
        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)

    def test_partial_update(self):

        original_description = 'Original description'
        recipe = create_recipe(
            name='Sample recipe title',
            description=original_description,
        )

        payload = {'name': 'New recipe name'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, original_description)

    def test_full_update(self):

        recipe = create_recipe(
            name='Sample recipe name',
            description='Sample recipe description.',
        )

        payload = {
            'name': 'New recipe name',
            'description': 'New recipe description',
        }
        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)

    def test_delete_recipe(self):

        recipe = create_recipe()

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())
