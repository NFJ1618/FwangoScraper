from dataclasses import dataclass
from typing import Optional

@dataclass
class TeamObject:
    team_name: Optional[str] = ""
    player1: Optional[str] = ""
    player2: Optional[str] = ""
    tournament: Optional[str] = ""
    division: Optional[str] = ""
    date: Optional[str] = ""
    url: Optional[str] = ""
        
@dataclass
class TournamentData:
    name: Optional[str] = ""
    date: Optional[str] = ""
    url: Optional[str] = ""

@dataclass
class GameData:
    team1 : Optional[str] = ""
    team2 : Optional[str] = ""
    t1_points : Optional[int] = -5
    t2_points : Optional[int] = -5
    tournament_stage : Optional[str] = ""
    tournament_name : Optional[str] = ""
    division: Optional[str] = ""
    

@dataclass
class SeriesData:
    round: Optional[str] = ""
    team1: Optional[str] = ""
    team2: Optional[str] = ""
    tournament: Optional[str] = ""
    division: Optional[str] = ""
    t1_scores: Optional[str] = ""
    t2_scores: Optional[str] = ""

@dataclass
class TeamResultObject:
    result: Optional[int] = 0
    team_name: Optional[str] = ""
    wins: Optional[int] = 0
    losses: Optional[int] = 0
    division: Optional[str] = ""
    tournament: Optional[str] = ""