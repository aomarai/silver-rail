from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from teams.models import Team, TeamCharacter
from characters.models import Character
from lightcones.models import Lightcone
from relics.models import Relic


class TeamCharacterModelTests(APITestCase):

    def test_create_team_character(self):
        team = Team.objects.create(name="Team A")
        character = Character.objects.create(name="Character A", rarity=5)
        lightcone = Lightcone.objects.create(name="Lightcone A", rarity=5)
        team_character = TeamCharacter.objects.create(
            team=team, character=character, lightcone=lightcone
        )
        return team, character, lightcone, team_character

    def test_team_deletion_cascades_to_team_characters(self):
        team, character, lightcone, team_character = self.test_create_team_character()
        url = reverse("team-detail", args=[team.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TeamCharacter.objects.filter(id=team_character.id).exists())

    def test_character_deletion_cascades_to_team_characters(self):
        team, character, lightcone, team_character = self.test_create_team_character()
        url = reverse("character-detail", args=[character.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TeamCharacter.objects.filter(id=team_character.id).exists())

    def test_lightcone_deletion_sets_null_in_team_characters(self):
        team, character, lightcone, team_character = self.test_create_team_character()
        url = reverse("lightcone-detail", args=[lightcone.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        team_character.refresh_from_db()
        self.assertIsNone(team_character.lightcone)

    def test_relic_deletion_removes_from_team_characters(self):
        team, character, lightcone, team_character = self.test_create_team_character()
        relic = Relic.objects.create(name="Relic A")
        team_character.relics.add(relic)
        url = reverse("relic-detail", args=[relic.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        team_character.refresh_from_db()
        self.assertFalse(team_character.relics.filter(id=relic.id).exists())
