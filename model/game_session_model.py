from pydantic import BaseModel
from model.grid_model import GridModel


class GameSessionModel(BaseModel):
    game_id: str
    grid: GridModel