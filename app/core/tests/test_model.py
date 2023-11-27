from django.test import TestCase
from core import models
from unittest.mock import patch


class ModelTest(TestCase):

    def test_create_recipe(self):
        recipe = models.Recipe.objects.create(
            name='Simple recipe name',
            description='Sample recipe description',
        )

        self.assertEqual(str(recipe), recipe.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')
