from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import ValidationError

from lightcones.models import Lightcone
from rest_framework.test import APITestCase
from django.urls import reverse

from users.models import SilverRailUser
from characters.tests import CharacterAPITests


def create_lightcone(
    name="Bright Star", ability="blows you up hugely wow", path="destruction", rarity=4
):
    return Lightcone.objects.create(
        name=name, ability=ability, path=path, rarity=rarity
    )


class LightconeModelTests(TestCase):

    def test_lightcone_creation_succeeds(self):
        lightcone = create_lightcone()
        self.assertEqual(lightcone.name, "Bright Star")
        self.assertEqual(lightcone.path, "destruction")
        self.assertEqual(lightcone.rarity, 4)

    def test_lightcone_creation_fails_with_invalid_data(self):
        with self.assertRaises((ValidationError, IntegrityError)):
            Lightcone.objects.create(name="", path="unknown", rarity=1)
        with self.assertRaises((ValidationError, IntegrityError)):
            Lightcone.objects.create(name="a lightcone", path="destruction", rarity=1)
        with self.assertRaises((ValidationError, IntegrityError)):
            Lightcone.objects.create(name="a lightcone", path="unknown", rarity=4)
        with self.assertRaises((ValidationError, IntegrityError)):
            Lightcone.objects.create(name="", path="harmony", rarity=5)

    def test_lightcone_retrieval_succeeds(self):
        lightcone = create_lightcone()
        retrieved_lightcone = Lightcone.objects.get(name="Bright Star")
        self.assertEqual(retrieved_lightcone, lightcone)

    def test_lightcone_update_succeeds(self):
        lightcone = create_lightcone()
        lightcone.name = "Shining Star"
        lightcone.save()
        updated_lightcone = Lightcone.objects.get(pk=lightcone.pk)
        self.assertEqual(updated_lightcone.name, "Shining Star")

    def test_lightcone_deletion_succeeds(self):
        lightcone = create_lightcone()
        lightcone_id = lightcone.id
        lightcone.delete()
        with self.assertRaises(Lightcone.DoesNotExist):
            Lightcone.objects.get(pk=lightcone_id)


class LightconeAPITests(APITestCase):

    def setUp(self):
        self.lightcone = create_lightcone()
        self.lightcone_url = reverse(
            "lightcone-detail", kwargs={"pk": self.lightcone.pk}
        )
        self.lightcone_list_url = reverse("lightcone-list")
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

    def get_lightcone_http_data(
        self, name="New Lightcone", ability="ability desc.", path="harmony", rarity=4
    ):
        return {
            "name": name,
            "ability": ability,
            "path": path,
            "rarity": rarity,
        }

    def test_create_lightcone(self):
        data = {
            "name": "Shining Star",
            "rarity": 5,
            "path": "destruction",
            "ability": "blows you up hugely wow 2",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.lightcone_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lightcone.objects.count(), 2)
        self.assertEqual(Lightcone.objects.get(name="Shining Star").path, "destruction")

    def test_retrieve_lightcone(self):
        response = self.client.get(self.lightcone_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Bright Star")

    def test_update_lightcone(self):
        data = {
            "name": "Shining Star",
            "rarity": 5,
            "path": "harmony",
            "ability": "blows you up hugely wow 2",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.lightcone_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lightcone.refresh_from_db()
        self.assertEqual(self.lightcone.path, "harmony")

    def test_delete_lightcone(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.lightcone_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lightcone.objects.count(), 0)

    def test_create_lightcone_non_superuser(self):
        self.set_self_as_regular_user()
        data = self.get_lightcone_http_data(rarity=5)
        response = self.client.post(self.lightcone_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lightcone.objects.count(), 1)

    def test_retrieve_lightcone_non_superuser(self):
        self.set_self_as_regular_user
        response = self.client.get(self.lightcone_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Bright Star")

    def test_update_lightcone_non_superuser(self):
        data = self.get_lightcone_http_data(name="Updated Lightcone")
        self.set_self_as_regular_user()
        response = self.client.put(self.lightcone_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNotNone(Lightcone.objects.get(name="Bright Star"))

    def test_delete_lightcone_non_superuser(self):
        self.set_self_as_regular_user()
        response = self.client.delete(self.lightcone_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lightcone.objects.count(), 1)
