"""
===============================================================================
MODEL — camada de DADOS e REGRAS DE NEGÓCIO (padrão MVC)
===============================================================================
Este é o ÚNICO arquivo de Model do projeto. Ele reúne:

    1) As classes que representam os DADOS do app (Transaction e Contact);
    2) A classe principal do Model — `BankAccount` — que guarda o estado da
       conta (saldo, extrato, contatos) e concentra TODAS as regras de
       negócio (ex.: "não pode transferir valor <= 0", "saldo não pode
       ficar negativo"). Nem a View nem o Controller sabem esses detalhes;
       eles só chamam os métodos que o Model oferece.

O Model NUNCA importa `flet` e NUNCA sabe desenhar nada na tela. Ele só
guarda e manipula dados. Quem desenha é a View; quem decide "quando" chamar
o quê é o Controller.

"""

from abc import ABC, abstractmethod

from dataclasses import dataclass

from datetime import datetime

@dataclass
class Transaction:
    
    id: str
    description: str
    category: str
    amount: float
    date: str
    emoji: str
    
    @property
    def is_income(self) -> bool:
        return self.amount >= 0

@dataclass
class Contact:
    
    name: str
    key_type: str
    key_masked: str
    initial: str
    color: str
    
def _today_label() -> str:
    return datetime.now().strftime("%d/%m")

class Account(ABC):
    @abstractmethod
    def transfer(self, contact_name: str, amount: float) -> Transaction:
        raise NotImplementedError
    
class BankAccount(Account):
    
    def __init__(
        self,
        owner_name: str,
        account_number: str, 
        initial_balance: float, 
        transactions: list[Transaction],
        contacts: list[Contact],
        ):
        
        self.owner_name = owner_name
        self.account_number = account_number
        
        self.balance = initial_balance
        
        self.balance_hidden = False
        self.unlocked = False
        
        self.transactions: list[Transaction] = list(transactions)
        self.contacts: list[Contact] = contacts
        
    @property
    def balance(self) -> float:
        return self._balance
    
    @balance.setter
    def balance(self, new_value: float) -> None:
        if new_value < 0:
            raise ValueError("O saldo da conta não pode ficar negativo.")
        self._balance = new_value
        
    def formatted_balance(self) -> str:
        if self.balance_hidden:
            return "R$ ******"
        texto = f"{self.balance:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {texto}"
    
    def toggle_balance_visibility(self) -> None:
        self.balance_hidden = not self.balance_hidden
        
    def transfer(self, contact_name: str, amount: float) -> Transaction:
        if amount <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        
        tx = Transaction(
            id=f"pix-{len(self.transactions) + 1}",
            description=f"Transferência enviada - {contact_name}",
            category="Pix enviado",
            amount=-abs(amount),
            date=_today_label(),
            emoji="↗️",
        )
        
        self.transactions.inset(0, tx)
        
        self.balance -= abs(amount)
        return tx
    
    def search_transactions(self, text: str, category_filter: str) -> list[Transaction]:
        
        texto_busca = text.lower()
        
        def bate_com_busca(tx: Transaction) -> bool:
            return texto_busca in tx.description.lower() or texto_busca in tx.category.lower()
        
        resultado = [tx for tx in self.transactions if bate_com_busca(tx)]
        if category_filter == "Entradas":
            return [tx for tx in resultado if tx.is_income]
        if category_filter == "Saídas":
            return [tx for tx in resultado if not tx.is_income]
        return resultado
    
USER_NAME = "Chuu do Loona"
ACCOUNT_NUMBER = "Conta 1234-5 · Agência 0001"
INITIAL_BALANCE = 4328.71

INITIAL_TRANSACTIONS: list[Transaction] = [
    Transaction("t1", "Salário", "Renda", 3200.00, "05/09", "💼"),
    Transaction("t2", "Supermercado Vitória", "Mercado", -186.40, "05/09", "🛒"),
    Transaction("t3", "Transferência recebida - Yves", "Pix recebido", 150.00, "06/09", "↙️"),
    Transaction("t4", "Serviço de streaming", "Assinatura", -39.90, "07/09", "🎬"),
    Transaction("t5", "Bar do China", "Alimentação", -68.00, "08/09", "🍽️"),
    Transaction("t6", "Farmácia Popular", "Saúde", -52.30, "09/09", "💊"),
    Transaction("t7", "99 Pop", "Transporte", -24.50, "10/09", "🚗"),
    Transaction("t8", "Shein", "Compras", -215.00, "11/09", "🛍️"),
    Transaction("t9", "Transferência recebida - Gowon", "Pix recebido", 90.00, "11/09", "↙️"),
    Transaction("t10", "Panobianco", "Assinatura", -99.90, "12/09", "🏋️"),
]

INITIAL_CONTACTS: list[Contact] = [
    Contact("Kim Jiwoo", "Celular", "(11) 9****-2233", "S", "#FEA87D"),
    Contact("Heejin", "E-mail", "hee***@email.com", "S", "#ED008E"),
    Contact("Jinsoul", "CPF", "123.***.***-07", "D", "#0801D5"),
    Contact("Hyunjin", "Chave aleatória", "a1b2***-****", "A", "#FFCA14"),
    Contact("Choerry", "Celular", "(21) 9****-8867", "A", "#BA01DE"),
]

def create_default_account() -> BankAccount:
    return BankAccount(
        owner_name=USER_NAME,
        account_number=ACCOUNT_NUMBER,
        initial_balance=INITIAL_BALANCE,
        transactions=INITIAL_TRANSACTIONS,
        contacts=INITIAL_CONTACTS,
    )
