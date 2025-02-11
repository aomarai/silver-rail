from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from characters.models import Character
from users.models import SilverRailUser
from rest_framework import status
from django.urls import reverse


class CharacterModelTests(APITestCase):

    def test_character_creation_succeeds(self):
        character = Character.objects.create(
            name="Hero", type="fire", path="destruction", rarity=5
        )
        self.assertEqual(character.name, "Hero")
        self.assertEqual(character.type, "fire")
        self.assertEqual(character.path, "destruction")
        self.assertEqual(character.rarity, 5)

    def test_character_creation_fails_with_invalid_data(self):
        with self.assertRaises(ValidationError):
            Character.objects.create(name="", type="unknown", path="invalid", rarity=-1)
        with self.assertRaises(ValidationError):
            Character.objects.create(
                name="a dude", type="unknown", path="harmony", rarity=5
            )
        with self.assertRaises(ValidationError):
            Character.objects.create(
                name="another dude", type="fire", path="invalid", rarity=4
            )
        with self.assertRaises(ValidationError):
            Character.objects.create(
                name="woah a third dude", type="ice", path="nihility", rarity=0
            )
        with self.assertRaises(ValidationError):
            Character.objects.create(
                name="ab", type="imaginary", path="harmony", rarity=3
            )

    def test_character_retrieval_succeeds(self):
        character = Character.objects.create(
            name="Hero", type="fire", path="destruction", rarity=5
        )
        retrieved_character = Character.objects.get(name="Hero")
        self.assertEqual(retrieved_character, character)

    def test_character_update_succeeds(self):
        character = Character.objects.create(
            name="Hero", type="fire", path="destruction", rarity=5
        )
        character.name = "Super Hero"
        character.save()
        updated_character = Character.objects.get(pk=character.pk)
        self.assertEqual(updated_character.name, "Super Hero")

    def test_character_deletion_succeeds(self):
        character = Character.objects.create(
            name="Hero", type="fire", path="destruction", rarity=5
        )
        character_id = character.id
        character.delete()
        with self.assertRaises(Character.DoesNotExist):
            Character.objects.get(pk=character_id)


class CharacterAPITests(APITestCase):

    def setUp(self):
        self.character = Character.objects.create(
            name="Hero", type="fire", path="destruction", rarity=5
        )
        self.character_url = reverse(
            "character-detail", kwargs={"pk": self.character.pk}
        )
        self.character_list_url = reverse("character-list")
        self.user = SilverRailUser.objects.create_superuser(
            username="testadmin",
            email="testadmin@admin.com",
            password="TestAdmin1234##",
        )

    def set_self_as_regular_user(self):
        self.user = SilverRailUser.objects.create_user(
            username="testregularuser",
            email="testuser@userwow.com",
            password="TotallyRealPassword1234##",
        )
        self.client.force_authenticate(user=self.user)

    @staticmethod
    def get_character_http_data(name="New Hero", type="ice", path="harmony", rarity=4):
        return {"name": name, "type": type, "path": path, "rarity": rarity}

    def test_create_character(self):
        data = self.get_character_http_data()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.character_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Character.objects.count(), 2)
        self.assertEqual(Character.objects.get(name="New Hero").type, "ice")

    def test_retrieve_character(self):
        response = self.client.get(self.character_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Hero")

    def test_update_character(self):
        data = {
            "name": "Updated Hero",
            "type": "fire",
            "path": "destruction",
            "rarity": 5,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.character_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.character.refresh_from_db()
        self.assertEqual(self.character.name, "Updated Hero")

    def test_delete_character(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.character_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Character.objects.count(), 0)

    def test_create_character_non_superuser(self):
        self.set_self_as_regular_user()
        data = self.get_character_http_data(type="fire", rarity=5)
        response = self.client.post(self.character_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Character.objects.count(), 1)

    def test_retrieve_character_non_superuser(self):
        self.set_self_as_regular_user
        response = self.client.get(self.character_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Hero")

    def test_update_character_non_superuser(self):
        data = self.get_character_http_data(name="Updated Guy")
        self.set_self_as_regular_user()
        response = self.client.put(self.character_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_character_non_superuser(self):
        self.set_self_as_regular_user()
        response = self.client.delete(self.character_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Character.objects.count(), 1)
