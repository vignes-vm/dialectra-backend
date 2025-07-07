from pydantic import BaseModel

class Speakers(BaseModel):
    name:str
    party:str
    role:str
    is_ai:bool
    prompt:str