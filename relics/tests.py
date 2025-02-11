from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from relics.models import Relic
from django.test import TestCase
from django.urls import reverse

from users.models import SilverRailUser


class RelicModelTests(TestCase):

    def test_relic_creation_succeeds(self):
        relic = Relic.objects.create(
            name="Ancient Crown",
            set_name="Ancient Set",
            effect="Increases wisdom by 10%",
            slot="head",
        )
        self.assertEqual(relic.name, "Ancient Crown")
        self.assertEqual(relic.set_name, "Ancient Set")
        self.assertEqual(relic.effect, "Increases wisdom by 10%")
        self.assertEqual(relic.slot, "head")

    def test_relic_creation_fails_with_invalid_slot(self):
        with self.assertRaises(ValidationError):
            Relic.objects.create(
                name="Mystic Gloves",
                set_name="Mystic Set",
                effect="Increases dexterity by 15%",
                slot="invalid_slot",
            )

    def test_relic_retrieval_succeeds(self):
        relic = Relic.objects.create(
            name="Ancient Crown",
            set_name="Ancient Set",
            effect="Increases wisdom by 10%",
            slot="head",
        )
        retrieved_relic = Relic.objects.get(name="Ancient Crown")
        self.assertEqual(retrieved_relic, relic)

    def test_relic_update_succeeds(self):
        relic = Relic.objects.create(
            name="Ancient Crown",
            set_name="Ancient Set",
            effect="Increases wisdom by 10%",
            slot="head",
        )
        relic.name = "Mystic Crown"
        relic.save()
        updated_relic = Relic.objects.get(pk=relic.pk)
        self.assertEqual(updated_relic.name, "Mystic Crown")

    def test_relic_deletion_succeeds(self):
        relic = Relic.objects.create(
            name="Ancient Crown",
            set_name="Ancient Set",
            effect="Increases wisdom by 10%",
            slot="head",
        )
        relic_id = relic.id
        relic.delete()
        with self.assertRaises(Relic.DoesNotExist):
            Relic.objects.get(pk=relic_id)


class RelicAPITests(APITestCase):

    def setUp(self):
        self.relic = Relic.objects.create(
            name="Ancient Crown",
            set_name="Ancient Set",
            effect="Increases wisdom by 10%",
            slot="head",
        )
        self.relic_url = reverse("relic-detail", kwargs={"pk": self.relic.pk})
        self.relic_list_url = reverse("relic-list")
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

    def get_relic_http_data(
        self,
        name="New Relic",
        set_name="relic test set",
        effect="relic effect here",
        slot="head",
    ):
        return {
            "name": name,
            "set_name": set_name,
            "effect": effect,
            "slot": slot,
        }

    def test_create_relic(self):
        data = {
            "name": "Mystic Gloves",
            "set_name": "Mystic Set",
            "effect": "Increases dexterity by 15%",
            "slot": "hands",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.relic_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Relic.objects.count(), 2)
        self.assertEqual(Relic.objects.get(name="Mystic Gloves").set_name, "Mystic Set")

    def test_retrieve_relic(self):
        response = self.client.get(self.relic_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Ancient Crown")

    def test_update_relic(self):
        data = {
            "name": "Mystic Crown",
            "set_name": "Mystic Set",
            "effect": "Increases wisdom by 15%",
            "slot": "head",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.relic_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.relic.refresh_from_db()
        self.assertEqual(self.relic.name, "Mystic Crown")

    def test_delete_relic(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.relic_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Relic.objects.count(), 0)

    def test_create_relic_non_superuser(self):
        self.set_self_as_regular_user()
        data = self.get_relic_http_data(name="Should Not Exist")
        response = self.client.post(self.relic_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Relic.objects.count(), 1)

    def test_retrieve_lightcone_non_superuser(self):
        self.set_self_as_regular_user
        response = self.client.get(self.relic_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Ancient Crown")

    def test_update_lightcone_non_superuser(self):
        data = self.get_relic_http_data(name="Updated Lightcone")
        self.set_self_as_regular_user()
        response = self.client.put(self.relic_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNotNone(Relic.objects.get(name="Ancient Crown"))

    def test_delete_lightcone_non_superuser(self):
        self.set_self_as_regular_user()
        response = self.client.delete(self.relic_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Relic.objects.count(), 1)
