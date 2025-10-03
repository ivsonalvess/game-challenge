
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import random

BOARD_SIZE = 20
START_MONEY = 300
LAP_BONUS = 100
MAX_ROUNDS = 1000

@dataclass
class Property:
    index: int
    price: int
    rent: int
    owner: Optional['Player'] = None

@dataclass
class Player:
    name: str
    strategy: str
    balance: int = START_MONEY
    position: int = 0
    active: bool = True
    turn_order: int = 0
    owned: List[int] = field(default_factory=list)

    def decide_buy(self, prop: Property, rng: random.Random) -> bool:
        if self.balance < prop.price:
            return False
        if self.strategy == "impulsivo":
            return True
        if self.strategy == "exigente":
            return prop.rent > 50
        if self.strategy == "cauteloso":
            return (self.balance - prop.price) >= 80
        if self.strategy == "aleatorio":
            return rng.random() < 0.5
        return False

def create_board() -> List[Property]:
    prices = [100, 120, 150, 180, 200, 220, 240, 260, 300, 320,
              340, 360, 380, 400, 420, 450, 480, 500, 520, 550]
    board = []
    for i, price in enumerate(prices):
        rent = round(price * 0.30)
        board.append(Property(index=i, price=price, rent=rent))
    return board

@dataclass
class GameResult:
    winner: str
    ranking: List[str]

class Game:
    def __init__(self):
        self.rng = random.Random()
        self.board: List[Property] = create_board()
        players = [
            Player(name="impulsivo", strategy="impulsivo"),
            Player(name="exigente", strategy="exigente"),
            Player(name="cauteloso", strategy="cauteloso"),
            Player(name="aleatorio", strategy="aleatorio"),
        ]
        self.rng.shuffle(players)
        for idx, p in enumerate(players):
            p.turn_order = idx
        self.players: List[Player] = players
        self.rounds_played = 0

    def simulate(self, max_rounds: int = MAX_ROUNDS) -> GameResult:
        while self.rounds_played < max_rounds and self._active_count() > 1:
            for player in self.players:
                if self._active_count() == 1:
                    break
                if not player.active:
                    continue
                self._take_turn(player)
            self.rounds_played += 1

        active = [p for p in self.players if p.active]
        if len(active) == 1:
            winner = active[0]
        else:
            winner = max(self.players, key=lambda p: (p.balance, -p.turn_order))

        ranked = sorted(self.players, key=lambda p: (-p.balance, p.turn_order))
        return GameResult(winner=winner.name, ranking=[p.name for p in ranked])

    def _active_count(self) -> int:
        return sum(1 for p in self.players if p.active)

    def _take_turn(self, player: Player):
        roll = self.rng.randint(1, 6)
        new_pos = player.position + roll
        if new_pos >= BOARD_SIZE:
            player.balance += LAP_BONUS
        player.position = new_pos % BOARD_SIZE

        tile = self.board[player.position]
        if tile.owner is None:
            if player.decide_buy(tile, self.rng):
                self._buy(player, tile)
            return

        owner = tile.owner
        if owner is player or owner is None or not owner.active:
            return
        self._pay_rent(player, owner, tile.rent)

    def _buy(self, player: Player, tile: Property):
        if tile.owner is not None:
            return
        if player.balance >= tile.price:
            player.balance -= tile.price
            tile.owner = player
            player.owned.append(tile.index)

    def _pay_rent(self, player: Player, owner: Player, rent: int):
        player.balance -= rent
        owner.balance += rent
        if player.balance < 0:
            self._eliminate(player)

    def _eliminate(self, player: Player):
        player.active = False
        for idx in list(player.owned):
            prop = self.board[idx]
            if prop.owner is player:
                prop.owner = None
        player.owned.clear()
