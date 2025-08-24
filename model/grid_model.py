from enum import Enum
from typing import List
from pydantic import BaseModel

class GridCellContent(Enum):
    STAR = "star"
    CROSS = "cross"
    EMPTY = "empty"

class GridCellModel(BaseModel):
    content: GridCellContent = GridCellContent.EMPTY
    region_color: str
    x: int
    y: int


class GridModel(BaseModel):
    width: int
    height: int
    cells: List[List[GridCellModel]]
