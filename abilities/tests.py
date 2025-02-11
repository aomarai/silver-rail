from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from characters.models import Character
from abilities.models import Ability
from django.urls import reverse


class AbilityModelTests(APITestCase):
    def setUp(self):
        self.character = Character.objects.create(
            name="Hero", type="fire", path="destruction", rarity=5
        )

    def test_ability_creation_succeeds(self):
        ability = Ability.objects.create(
            character=self.character, name="Fireball", type="skill"
        )
        self.assertEqual(ability.name, "Fireball")
        self.assertEqual(ability.type, "skill")
        self.assertEqual(ability.character, self.character)

    def test_ability_creation_fails_with_invalid_data(self):
        with self.assertRaises(ValidationError):
            Ability.objects.create(character=self.character, name="", type="unknown")

    def test_ability_retrieval_succeeds(self):
        ability = Ability.objects.create(
            character=self.character, name="Fireball", type="skill"
        )
        retrieved_ability = Ability.objects.get(name="Fireball")
        self.assertEqual(retrieved_ability, ability)

    def test_ability_update_succeeds(self):
        ability = Ability.objects.create(
            character=self.character, name="Fireball", type="skill"
        )
        ability.name = "Flame Burst"
        ability.save()
        updated_ability = Ability.objects.get(pk=ability.pk)
        self.assertEqual(updated_ability.name, "Flame Burst")

    def test_ability_deletion_succeeds(self):
        ability = Ability.objects.create(
            character=self.character, name="Fireball", type="skill"
        )
        ability_id = ability.id
        ability.delete()
        with self.assertRaises(Ability.DoesNotExist):
            Ability.objects.get(pk=ability_id)
