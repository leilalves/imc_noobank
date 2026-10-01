# Noobank 💜 — exercício de clone de app bancário digital (estilo Nubank)

Exercício de estudo: recria a experiência de um app de banco digital (saldo,
Pix, extrato) protegido por biometria, com **dados fictícios**. Nenhum nome,
logo ou marca de app real é usado.

**Escopo combinado:** só telas/UI, sem persistência em disco tudo (saldo,
extrato, Pix) volta ao estado inicial quando você fecha e abre o app de novo.

Este projeto está organizado no **padrão MVC (Model – View – Controller)**,
usando **orientação a objetos** — incluindo os 4 paradigmas (abstração,
herança, polimorfismo e encapsulamento). Para facilitar o estudo, cada
camada foi mantida em **um único arquivo**.

## Como rodar

```bash
python -m venv venv
Windows: venv\Scripts\activate
pip install "flet[all]"
pip install flet flet-local-auth
python main.py
```

Para rodar (sem biometria de verdade, use o botão "Desbloquear"):

```bash
flet run --web main.py 
flet run --android main.py
flet run --ios main.py
```

## Estrutura do projeto

```
noobank_mvc/
├── model.py         # MODEL — dados + regras de negócio
├── view.py          # VIEW — todas as telas
├── controller.py    # CONTROLLER — orquestra Model e View
├── main.py          # ponto de entrada: cria Model + Controller e inicia o Flet
└── README.md
```

## Avisos

- Isto é um **exercício educacional**. Não movimenta dinheiro real, não
  se conecta a nenhum banco e não deve ser usado para nada além de estudo.
- Nenhum recurso visual, nome ou marca do app real Nubank (ou de qualquer
  concorrente) foi copiado usuário, contatos, saldo e extrato são
  totalmente fictícios.
