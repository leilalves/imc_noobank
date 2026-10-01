# Noobank — exercício de clone de app bancário digital
# Reorganizado no padrão MVC (Model - View - Controller):
#
#     model.py      -> dados + regras de negócio (classes Transaction,
#                       Contact, Account e BankAccount)
#     view.py        -> todas as telas (ScreenView e suas subclasses)
#     controller.py  -> a classe NoobankController, que liga tudo
#     main.py        -> só cria o Model e o Controller e inicia o Flet

import flet as ft

from controller import NoobankController
from model import create_default_account

def main(page: ft.Page) -> None:
    """Ponto de entrada do app: cria o Model, cria o Controller e inicia."""
    # 1) Model: a conta bancária fictícia, já populada com os dados iniciais.
    account = create_default_account()

    # 2) Controller: recebe o Model e assume o controle da `page`.
    controller = NoobankController(account)
    controller.run(page)

if __name__ == "__main__":
    ft.run(main)
