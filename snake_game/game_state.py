"""Lógica de estado do Jogo da Cobrinha, independente de renderização."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


def _is_opposite(a: Direction, b: Direction) -> bool:
    return a.value[0] == -b.value[0] and a.value[1] == -b.value[1]


Point = tuple[int, int]


@dataclass
class GameState:
    """Mantém o estado completo de uma partida do jogo da cobrinha."""

    grid_width: int
    grid_height: int
    snake: list[Point] = field(default_factory=list)
    direction: Direction = Direction.RIGHT
    _pending_direction: Direction = field(default=Direction.RIGHT, repr=False)
    food: Point = field(default=(0, 0))
    score: int = 0
    game_over: bool = False

    def __post_init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        """Reinicia o estado para uma nova partida."""
        center_x = self.grid_width // 2
        center_y = self.grid_height // 2
        self.snake = [(center_x, center_y), (center_x - 1, center_y), (center_x - 2, center_y)]
        self.direction = Direction.RIGHT
        self._pending_direction = Direction.RIGHT
        self.score = 0
        self.game_over = False
        self.food = self._spawn_food()

    def _spawn_food(self) -> Point:
        occupied = set(self.snake)
        available = [
            (x, y)
            for x in range(self.grid_width)
            for y in range(self.grid_height)
            if (x, y) not in occupied
        ]
        return random.choice(available) if available else self.snake[0]

    def change_direction(self, new_direction: Direction) -> None:
        """Registra a próxima direção, ignorando inversões de 180 graus."""
        if _is_opposite(new_direction, self.direction):
            return
        self._pending_direction = new_direction

    def step(self) -> None:
        """Avança o estado do jogo em um tick do game loop."""
        if self.game_over:
            return

        self.direction = self._pending_direction
        head_x, head_y = self.snake[0]
        delta_x, delta_y = self.direction.value
        new_head = (head_x + delta_x, head_y + delta_y)

        if self._is_collision(new_head):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self._spawn_food()
        else:
            self.snake.pop()

    def _is_collision(self, point: Point) -> bool:
        x, y = point
        hits_wall = x < 0 or x >= self.grid_width or y < 0 or y >= self.grid_height
        hits_self = point in self.snake[:-1]
        return hits_wall or hits_self
