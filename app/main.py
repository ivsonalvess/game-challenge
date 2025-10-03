
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from app.game import Game, GameResult

app = FastAPI(title="Simulador Banco-Imobiliário Simplificado",
              description="API para simular partida com 4 estratégias",
              version="1.0.0")

class SimulacaoResponse(BaseModel):
    winner: str
    players: List[str]

@app.post("/jogo/simular", response_model=SimulacaoResponse)
def simular_partida(
    max_rodadas: int = Query(default=1000, ge=1, le=100000, description="Máximo de rodadas")
):
    game = Game()
    result: GameResult = game.simulate(max_rounds=max_rodadas)
    return SimulacaoResponse(winner=result.winner, players=result.ranking)
