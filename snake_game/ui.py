"""Interface gráfica do Jogo da Cobrinha usando Tkinter Canvas."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from snake_game.database import ScoreRepository
from snake_game.game_state import Direction, GameState
from snake_game.logger_config import get_logger

logger = get_logger(__name__)

CELL_SIZE = 24
GRID_WIDTH = 25
GRID_HEIGHT = 20
TICK_MS = 110

COLOR_BACKGROUND = "#1e1e2e"
COLOR_GRID = "#282838"
COLOR_SNAKE_HEAD = "#a6e3a1"
COLOR_SNAKE_BODY = "#7ec98f"
COLOR_FOOD = "#f38ba8"
COLOR_TEXT = "#cdd6f4"
COLOR_PANEL = "#181825"

_KEY_TO_DIRECTION = {
    "Up": Direction.UP,
    "w": Direction.UP,
    "W": Direction.UP,
    "Down": Direction.DOWN,
    "s": Direction.DOWN,
    "S": Direction.DOWN,
    "Left": Direction.LEFT,
    "a": Direction.LEFT,
    "A": Direction.LEFT,
    "Right": Direction.RIGHT,
    "d": Direction.RIGHT,
    "D": Direction.RIGHT,
}


class SnakeGameApp:
    """Janela principal do jogo: liga estado, renderização e input do usuário."""

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._root.title("Jogo da Cobrinha")
        self._root.resizable(False, False)
        self._root.configure(bg=COLOR_PANEL)

        self._score_repo = ScoreRepository()
        self._high_score = self._score_repo.get_high_score()

        self._state = GameState(grid_width=GRID_WIDTH, grid_height=GRID_HEIGHT)
        self._is_running = True
        self._after_id: str | None = None

        self._build_widgets()
        self._bind_keys()
        self._schedule_tick()

    def _build_widgets(self) -> None:
        header = tk.Frame(self._root, bg=COLOR_PANEL, pady=8)
        header.pack(fill="x")

        self._score_label = tk.Label(
            header,
            text="Pontos: 0",
            font=("Segoe UI", 13, "bold"),
            fg=COLOR_TEXT,
            bg=COLOR_PANEL,
        )
        self._score_label.pack(side="left", padx=16)

        self._high_score_label = tk.Label(
            header,
            text=f"Recorde: {self._high_score}",
            font=("Segoe UI", 13, "bold"),
            fg=COLOR_TEXT,
            bg=COLOR_PANEL,
        )
        self._high_score_label.pack(side="right", padx=16)

        self._canvas = tk.Canvas(
            self._root,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg=COLOR_BACKGROUND,
            highlightthickness=0,
        )
        self._canvas.pack(padx=12, pady=(0, 12))

        footer = tk.Label(
            self._root,
            text="Use as setas ou WASD para mover  •  R para reiniciar",
            font=("Segoe UI", 9),
            fg="#6c7086",
            bg=COLOR_PANEL,
        )
        footer.pack(pady=(0, 8))

    def _bind_keys(self) -> None:
        self._root.bind("<KeyPress>", self._on_key_press)

    def _on_key_press(self, event: tk.Event) -> None:
        if event.keysym in _KEY_TO_DIRECTION:
            self._state.change_direction(_KEY_TO_DIRECTION[event.keysym])
        elif event.keysym.lower() == "r":
            self._restart()

    def _restart(self) -> None:
        self._state.reset()
        self._is_running = True

    def _schedule_tick(self) -> None:
        self._after_id = self._root.after(TICK_MS, self._on_tick)

    def _on_tick(self) -> None:
        try:
            if self._is_running:
                self._state.step()
                if self._state.game_over:
                    self._handle_game_over()
                self._render()
        except Exception:
            logger.exception("Erro inesperado durante o loop do jogo.")
            messagebox.showerror(
                "Erro no Jogo da Cobrinha",
                "Ocorreu um erro inesperado. Detalhes foram salvos no log.",
            )
            self._is_running = False
        finally:
            self._schedule_tick()

    def _handle_game_over(self) -> None:
        self._is_running = False
        if self._state.score > self._high_score:
            self._high_score = self._state.score
            self._score_repo.update_high_score(self._high_score)

    def _render(self) -> None:
        canvas = self._canvas
        canvas.delete("all")

        self._draw_grid()

        food_x, food_y = self._state.food
        canvas.create_oval(
            food_x * CELL_SIZE + 3,
            food_y * CELL_SIZE + 3,
            (food_x + 1) * CELL_SIZE - 3,
            (food_y + 1) * CELL_SIZE - 3,
            fill=COLOR_FOOD,
            outline="",
        )

        for index, (x, y) in enumerate(self._state.snake):
            color = COLOR_SNAKE_HEAD if index == 0 else COLOR_SNAKE_BODY
            canvas.create_rectangle(
                x * CELL_SIZE + 1,
                y * CELL_SIZE + 1,
                (x + 1) * CELL_SIZE - 1,
                (y + 1) * CELL_SIZE - 1,
                fill=color,
                outline="",
            )

        self._score_label.config(text=f"Pontos: {self._state.score}")
        self._high_score_label.config(text=f"Recorde: {self._high_score}")

        if self._state.game_over:
            self._draw_game_over_overlay()

    def _draw_grid(self) -> None:
        canvas = self._canvas
        width = GRID_WIDTH * CELL_SIZE
        height = GRID_HEIGHT * CELL_SIZE
        for x in range(0, width, CELL_SIZE):
            canvas.create_line(x, 0, x, height, fill=COLOR_GRID)
        for y in range(0, height, CELL_SIZE):
            canvas.create_line(0, y, width, y, fill=COLOR_GRID)

    def _draw_game_over_overlay(self) -> None:
        canvas = self._canvas
        width = GRID_WIDTH * CELL_SIZE
        height = GRID_HEIGHT * CELL_SIZE
        canvas.create_rectangle(0, 0, width, height, fill=COLOR_BACKGROUND, stipple="gray50")
        canvas.create_text(
            width // 2,
            height // 2 - 16,
            text="FIM DE JOGO",
            font=("Segoe UI", 22, "bold"),
            fill=COLOR_TEXT,
        )
        canvas.create_text(
            width // 2,
            height // 2 + 20,
            text="Pressione R para reiniciar",
            font=("Segoe UI", 12),
            fill=COLOR_TEXT,
        )
