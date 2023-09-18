import httpx
from bs4 import BeautifulSoup

from .models import Statistics
from .util import API_CLASSIFICATION
# from flags import participants

def _get_the_scores(soup: BeautifulSoup):
    values = [value.text for value in soup]
    
    if len(values) >= 2:
        score_one, score_two = values[:2]
        score_three = values[2] if len(values) > 2 else None
    
    if score_three == None:
        return score_one, score_two
    return score_one, score_two, score_three

class Classification(object):
    def __init__(self) -> None:
        self.response = httpx.get(API_CLASSIFICATION, timeout=10.0)
        self.response.raise_for_status()
    
    def _get_statistics_country(self, soup: BeautifulSoup):
        from dataclasses import asdict

        _standing = soup.find_all('li', 'Standing_standings__rowLink__Skr86')
        self.statistics = {'results': []}

        for standing in _standing:
            position = standing.find('div', 'Standing_standings__cell__5Kd0W').text
            label    = standing.find('div', 'Standing_standings__cellIcon__EbcOR').get('title')
            country  = standing.find('p', 'title-7-medium Standing_standings__teamName__psv61').text
            # flag     = participants[country]

            matches_played, goal_difference = _get_the_scores(standing.find_all('div', 'Standing_standings__cell__5Kd0W Standing_standings__cellTextDimmed__vpZYH'))
            won, tied, losses = _get_the_scores(standing.find_all('div', 'Standing_standings__cellLargeScreen__ttPap'))
            points = standing.find('span', 'title-7-bold').text

            data = Statistics(
                # flag=flag,
                country=country,
                position=position,
                label=label,
                matches_played=matches_played,
                won=won, tied=tied, losses=losses,
                goal_difference=goal_difference,
                points=points
            )

            self.statistics['results'].append(asdict(data))

    @property
    def get_positions(self):
        soup = BeautifulSoup(self.response.content, "html.parser")
        section_classification_country = soup.find('div', 'xpaLayoutContainerComponentResolver--standings')

        self._get_statistics_country(section_classification_country)

        return self.statistics