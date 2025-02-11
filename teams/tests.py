from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from teams.models import Team, TeamCharacter
from characters.models import Character
from lightcones.models import Lightcone
from relics.models import Relic
from users.models import SilverRailUser


def create_character(name="Test Character", rarity=5, path="destruction", type="fire"):
    return Character.objects.create(name=name, rarity=rarity, path=path, type=type)


class TeamCharacterModelTests(APITestCase):

    def setUp(self):
        self.user = SilverRailUser.objects.create_superuser(
            username="testadmin",
            email="testadmin@admin.com",
            password="TestAdmin1234##",
        )
        self.client.force_authenticate(user=self.user)

    @staticmethod
    def create_team_character():
        team = Team.objects.create(name="Team A")
        character = create_character()
        lightcone = Lightcone.objects.create(
            name="Lightcone A", rarity=5, path="destruction", ability="Ability A"
        )
        team_character = TeamCharacter.objects.create(
            team=team, character=character, lightcone=lightcone
        )
        return team, character, lightcone, team_character

    def test_team_deletion_cascades_to_team_characters(self):
        team, character, lightcone, team_character = self.create_team_character()
        url = reverse("team-detail", args=[team.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TeamCharacter.objects.filter(id=team_character.id).exists())

    def test_character_deletion_cascades_to_team_characters(self):
        team, character, lightcone, team_character = self.create_team_character()
        url = reverse("character-detail", args=[character.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TeamCharacter.objects.filter(id=team_character.id).exists())

    def test_lightcone_deletion_sets_null_in_team_characters(self):
        team, character, lightcone, team_character = self.create_team_character()
        url = reverse("lightcone-detail", args=[lightcone.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        team_character.refresh_from_db()
        self.assertIsNone(team_character.lightcone)

    def test_relic_deletion_removes_from_team_characters(self):
        team, character, lightcone, team_character = self.create_team_character()
        relic = Relic.objects.create(
            name="Relic A", slot="head", set_name="Set A", effect="Effect A"
        )
        team_character.relics.add(relic)
        url = reverse("relic-detail", args=[relic.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        team_character.refresh_from_db()
        self.assertFalse(team_character.relics.filter(id=relic.id).exists())
