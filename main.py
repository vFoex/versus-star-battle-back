from typing import Dict
from fastapi import FastAPI, WebSocket
from game.game_service import GameService
from game.grid import Grid
from game.game_session import GameSession
from model.game_session_model import GameSessionModel
import uuid

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:4200",  # Angular
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


game_sessions: Dict[str, GameSession] = {}

@app.get("/create-game", response_model=GameSessionModel)
def create_game() -> GameSessionModel:

    grid: Grid = GameService().create_game()
    if not grid:
        raise ValueError("Grid is not initialized")
    game_session = GameSession(game_id=str(uuid.uuid4()), grid=grid)

    game_sessions[game_session.game_id] = game_session

    return game_session.to_dto()


@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    await websocket.accept()
    if game_id not in game_sessions:
        print(f"Game session {game_id} not found", game_sessions)
        await websocket.close(code=1008, reason="Game session not found")
        return
    
    game_session = game_sessions[game_id]
    game_session.connect(websocket)


    try:
        while True:
            data = await websocket.receive_json()
            await game_session.handle_message(websocket, data)
    except Exception as e:
        print(f"Error: {e}")