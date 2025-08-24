from typing import Dict

import json
from game.grid import Grid
from fastapi import WebSocket
from model.game_session_model import GameSessionModel
from model.grid_model import GridCellContent, GridCellModel, GridModel

class GameSession:
    def __init__(self, game_id: str, grid: Grid):
        self.game_id = game_id
        self.grid = grid
        self.connections: list[WebSocket] = []

    def to_dto(self) -> GameSessionModel:
        return GameSessionModel(
            game_id=self.game_id,
            grid=self.grid.to_dto()
        )

    def connect(self, websocket: WebSocket):
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def handle_message(self, websocket: WebSocket, data: Dict):
        # Handle incoming messages from the client
        # This could include game actions, updates, etc.
        if 'action' not in data:
            await websocket.close(code=1008, reason="Invalid message format")
            return
        
        action = data['action']
        game_id = data.get('game_id', self.game_id)

        if action == 'update_grid':
            
            if 'grid' not in data:
                await websocket.close(code=1008, reason="Grid data not provided")
                return
            
            grid_data = data['grid']
            
            grid_model = GridModel(
                width=grid_data['width'],
                height=grid_data['height'],
                cells=[
                    [GridCellModel(
                        content=GridCellContent(cell['content']),
                        region_color=cell['regionColor'],
                        x=cell['x'],
                        y=cell['y']
                    ) for cell in row] for row in grid_data['cells']
                ]
            )
            is_over = self.grid.check_game_over(grid_model=grid_model)
            if is_over:
                await websocket.send_json({
                    'game_id': game_id,
                    'action': 'game_over',
                    'message': 'Game over! You won!'
                })
                return

        elif action == 'end_game':
            self.disconnect(websocket)