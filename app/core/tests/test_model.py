from django.test import TestCase
from core import models


class ModelTest(TestCase):

    def test_create_recipe(self):
        recipe = models.Recipe.objects.create(
            name='Simple recipe name',
            description='Sample recipe description',
        )

        self.assertEqual(str(recipe), recipe.name)
