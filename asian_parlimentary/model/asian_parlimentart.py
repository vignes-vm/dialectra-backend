from models.parlimentary import Parlimentary
from models.speakers import Speakers
from pydantic import BaseModel
from typing import List, Optional

class AsianParliamentary(Parlimentary):
    def __init__(self,topic:str):
        super().__init__(
            name="Asian parlimentary",
            speakers=[
                Speakers(name="PM", party="Gov", role="Prime Minister",is_ai=True,prompt=f"Ai vs human. Prime Minister need to support about AI in the topic:{topic},This is the first person of the speech"),  # PM is AI
                Speakers(name="LO", party="Opp", role="Leader of Opposition",is_ai=False,prompt=""),
                Speakers(name="DPM", party="Gov", role="Deputy Prime Minister",is_ai=False,prompt=""),
                Speakers(name="DLO", party="Opp", role="Deputy Leader of Opposition",is_ai=False,prompt=""),
                Speakers(name="Gov Whip", party="Gov", role="Whip",is_ai=False,prompt=""),
                Speakers(name="Opp Whip", party="Opp", role="Whip",is_ai=False,prompt="")
            ],
            duration=1800,
            topic=topic,
            current_speaker_index=0,  # Start with PM (index 0)
            speeches=[],  # Initialize empty speeches list
            debate_state="not_started"  # Initial state
        )
