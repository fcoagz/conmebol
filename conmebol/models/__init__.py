from dataclasses import dataclass

@dataclass
class Statistics:
    # flag: str
    country: str
    position: int
    label: str
    matches_played: int
    won: int
    tied: int
    losses: int
    goal_difference: int
    points: int

@dataclass
class LastMatches:
    first_team: dict
    second_team: dict
    winner: str
    date: str

@dataclass
class NextMatches:
    first_team: str
    second_team: str
    date: str

@dataclass
class LiveMatches:
    first_team: dict
    second_team: dict
    winner: str
    time: str