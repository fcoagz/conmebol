import httpx
from bs4 import BeautifulSoup

from .util import API_MATCHES
from .models import NextMatches, LiveMatches
# from flags import participants

def get_match_prox_or_live(_journeys: list, matches: BeautifulSoup):
    from dataclasses import asdict

    team_names = [x.text for team in matches for x in team.find_all('span', 'SimpleMatchCardTeam_simpleMatchCardTeam__name__7Ud8D')]
    goals = [x.text for team in matches for x in team.find_all('span', 'SimpleMatchCardTeam_simpleMatchCardTeam__score__UYMc_')]
    match_dates = [x.find('time').get('datetime') if x.find('time') else x.text for team in matches for x in team.find_all('div', 'SimpleMatchCard_simpleMatchCard__matchContent__prwTf')]
    
    results = {}
    for i in range(0, len(team_names), 2):
        first_team = team_names[i]
        second_team = team_names[i+1]
        date = match_dates[i//2]

        if all(g == '' for g in [goals[i], goals[i+1]]):
            data = NextMatches(
                first_team=first_team,
                second_team=second_team,
                date=date
            )
            if _journeys[i//10] not in results:
                results[_journeys[i//10]] = []
            results[_journeys[i//10]].append(asdict(data))
        else:
            first_team = {'country': first_team, 'goals': goals[i]}
            second_team = {'country': second_team, 'goals': goals[i+1]}
            winner = 'Tie' if goals[i] == goals[i+1] else first_team if goals[i] > goals[i+1] else second_team
            time = date

            data = LiveMatches(
                first_team=first_team,
                second_team=second_team,
                winner=winner,
                time=time
            )
            if _journeys[i//10] not in results:
                results[_journeys[i//10]] = []
            results[_journeys[i//10]].append(asdict(data))

    return results

class Matches(object):
    def __init__(self) -> None:
        self.response = httpx.get(API_MATCHES, timeout=10.0)
        self.response.raise_for_status()

    @property
    def get_matches(self):
        soup = BeautifulSoup(self.response.content, "html.parser")
        section_matches = soup.find('div', 'MatchCardsListsAppender_container__y5ame')

        _journeys = [journey.text for journey in section_matches.find_all('div', 'SectionHeader_container__iVfZ9')]
        _matches  = section_matches.find_all('div', 'SimpleMatchCard_simpleMatchCard__content__ZWt2p')

        self.results = get_match_prox_or_live(_journeys, _matches)

        return self.results