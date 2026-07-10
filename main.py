"""Ponto de entrada do Jogo da Cobrinha."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _candidate_python_roots() -> list[Path]:
    """Lista diretórios onde uma instalação Python (com Tcl/Tk) pode estar.

    Em instalações quebradas ou parcialmente movidas, `sys.base_prefix` pode
    não apontar para o diretório real (ex.: cai no diretório de trabalho
    atual). Por isso combinamos várias fontes: o executável em uso, os
    prefixos reportados pelo `sys`, e o local padrão de instalação do
    Python no Windows.
    """
    roots = [
        Path(sys.executable).parent,
        Path(sys.base_prefix),
        Path(sys.prefix),
    ]

    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            roots.extend(Path(local_app_data, "Programs", "Python").glob("Python3*"))

    return roots


def _fix_tcl_tk_env() -> None:
    """Corrige TCL_LIBRARY/TK_LIBRARY quando apontam para outro venv/instalação.

    Algumas IDEs (ex.: PyCharm) herdam essas variáveis de ambiente de outra
    configuração de execução, e instalações Python quebradas/incompletas do
    Windows fazem o Tkinter procurar o init.tcl no lugar errado. Aqui
    varremos diretórios candidatos do próprio interpretador em execução e
    sobrescrevemos as variáveis assim que encontramos uma instalação válida.
    """
    for root in _candidate_python_roots():
        tcl_dir = root / "tcl"
        if not tcl_dir.is_dir():
            continue

        for entry in tcl_dir.iterdir():
            name = entry.name.lower()
            if name.startswith("tcl8") and (entry / "init.tcl").exists():
                os.environ["TCL_LIBRARY"] = str(entry)
            elif name.startswith("tk8"):
                os.environ["TK_LIBRARY"] = str(entry)

        if "TCL_LIBRARY" in os.environ:
            return


_fix_tcl_tk_env()

import tkinter as tk  # noqa: E402  (precisa vir depois do fix de ambiente)
from tkinter import messagebox  # noqa: E402

from snake_game.logger_config import get_logger  # noqa: E402
from snake_game.ui import SnakeGameApp  # noqa: E402

logger = get_logger(__name__)


def main() -> None:
    root = tk.Tk()
    try:
        SnakeGameApp(root)
        root.mainloop()
    except Exception:
        logger.exception("Falha ao iniciar o Jogo da Cobrinha.")
        messagebox.showerror(
            "Erro ao iniciar",
            "Não foi possível iniciar o jogo. Detalhes foram salvos no log.",
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
