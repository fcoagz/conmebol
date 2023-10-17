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
    
    team_counter = 0
    date_index = 0
    journey_index = 0
    result_counter = 0
    results = []

    for i in range(len(team_names)):
        team_counter += 1

        if team_counter == 10:
            for j in range(i-9, i+1):
                result_counter += 1

                if result_counter == 2:
                    if all(g == '' for g in [goals[j-1], goals[j]]):
                        first_team = team_names[j-1]
                        second_team = team_names[j]
                        date = match_dates[date_index]

                        data = NextMatches(
                            first_team=first_team,
                            second_team=second_team,
                            date=date
                        )

                        if _journeys[journey_index] not in results:
                            results[_journeys[journey_index]] = []
                        
                        results[_journeys[journey_index]].append(asdict(data))

                        date_index += 1
                        result_counter = 0
                    else:
                        first_team = {'country': team_names[j-1], 'goals': goals[j-1]}
                        second_team = {'country': team_names[j], 'goals': goals[j]}
                        winner = 'Tie' if goals[j-1] == goals[j] else team_names[j-1] if goals[j-1] > goals[j] else team_names[j]
                        time = match_dates[date_index]

                        data = LiveMatches(
                            first_team=first_team,
                            second_team=second_team,
                            winner=winner,
                            time=time
                        )

                        if _journeys[journey_index] not in results:
                            results[_journeys[journey_index]] = []
                        
                        results[_journeys[journey_index]].append(asdict(data))

                        date_index += 1
                        team_counter = 0
            
            journey_index += 1
            team_counter = 0
    
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