from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from .speakers import Speakers

class Parlimentary(BaseModel):
    """
    A data model that represents a Parlimentary debate style.

    Attributes:
        name (str): The name of the Parlimentary debate style.
        speakers (List[Speakers]): A list of Speakers that participate in the debate.
        duration (int): The duration of the debate in seconds.
        topic (str): The topic of the debate.
        current_speaker_index (int): Index of the current speaker in the speakers list.
        speeches (List[Dict]): List of speeches made in the debate.
        debate_state (str): Current state of the debate (not_started, in_progress, completed).
    """
    id: str = None
    name: str
    speakers: List[Speakers]
    duration: int
    topic: str
    current_speaker_index: int = 0
    speeches: List[Dict[str, Any]] = []
    debate_state: str = "not_started"
