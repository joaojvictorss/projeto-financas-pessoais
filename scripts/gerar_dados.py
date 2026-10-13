import random, csv, calendar, pickle
from datetime import date

random.seed(42)
MESES = [(2025, 10), (2025, 11), (2025, 12)] + [(2026, m) for m in range(1, 10)]
PAG = ["Cartão de crédito", "Pix", "Débito", "Dinheiro", "Boleto"]

def d(ano, mes, dia):
    return date(ano, mes, min(dia, calendar.monthrange(ano, mes)[1]))

def money(a, b):
    return round(random.uniform(a, b), 2)

L = []  # (data, descricao, categoria, tipo, valor, forma_pagamento)
for ano, mes in MESES:
    # Receitas
    L.append((d(ano, mes, 5), "Salário", "Salário", "Receita", 5600.00, "Pix"))
    if random.random() < 0.45:
        L.append((d(ano, mes, random.randint(10, 25)), "Projeto freelance", "Freelance", "Receita", money(400, 1200), "Pix"))
    L.append((d(ano, mes, 28), "Rendimento da reserva", "Rendimentos", "Receita", money(18, 48), "Pix"))

    # Moradia (fixas + luz variável)
    L.append((d(ano, mes, 8), "Aluguel", "Moradia", "Despesa", 1350.00, "Boleto"))
    L.append((d(ano, mes, 8), "Condomínio", "Moradia", "Despesa", 250.00, "Boleto"))
    L.append((d(ano, mes, 10), "Internet", "Moradia", "Despesa", 99.90, "Débito"))
    L.append((d(ano, mes, 15), "Conta de luz", "Moradia", "Despesa", money(85, 165), "Boleto"))

    # Assinaturas
    L.append((d(ano, mes, 12), "Streaming de vídeo", "Assinaturas", "Despesa", 39.90, "Cartão de crédito"))
    L.append((d(ano, mes, 14), "Streaming de música", "Assinaturas", "Despesa", 21.90, "Cartão de crédito"))
    # Saúde
    L.append((d(ano, mes, 3), "Academia", "Saúde", "Despesa", 109.90, "Cartão de crédito"))
    for _ in range(random.randint(0, 2)):
        L.append((d(ano, mes, random.randint(1, 28)), "Farmácia", "Saúde", "Despesa", money(25, 110), random.choice(["Débito", "Pix"])))
    if random.random() < 0.15:
        L.append((d(ano, mes, random.randint(1, 28)), "Consulta médica", "Saúde", "Despesa", money(150, 280), "Pix"))
    # Educação
    L.append((d(ano, mes, 6), "Curso online", "Educação", "Despesa", 59.90, "Cartão de crédito"))
    if random.random() < 0.2:
        L.append((d(ano, mes, random.randint(1, 28)), "Livro técnico", "Educação", "Despesa", money(60, 140), "Cartão de crédito"))
    # Alimentação
    for _ in range(random.randint(5, 7)):
        L.append((d(ano, mes, random.randint(1, 28)), "Supermercado", "Alimentação", "Despesa", money(70, 230), random.choice(["Débito", "Cartão de crédito", "Pix"])))
    for _ in range(random.randint(3, 5)):
        L.append((d(ano, mes, random.randint(1, 28)), "Restaurante", "Alimentação", "Despesa", money(32, 105), random.choice(PAG[:3])))
    for _ in range(random.randint(3, 6)):
        L.append((d(ano, mes, random.randint(1, 28)), "Delivery", "Alimentação", "Despesa", money(26, 68), "Cartão de crédito"))
    # Transporte
    L.append((d(ano, mes, 2), "Recarga transporte público", "Transporte", "Despesa", 150.00, "Pix"))
    for _ in range(random.randint(4, 9)):
        L.append((d(ano, mes, random.randint(1, 28)), "Corrida de aplicativo", "Transporte", "Despesa", money(12, 38), "Cartão de crédito"))
    # Lazer
    for _ in range(random.randint(2, 5)):
        L.append((d(ano, mes, random.randint(1, 28)), random.choice(["Cinema", "Bar com amigos", "Show", "Passeio"]), "Lazer", "Despesa", money(40, 170), random.choice(PAG[:3])))
    # Compras (sazonal)
    n = random.randint(0, 2)
    if mes in (11, 12): n += 2
    for _ in range(n):
        L.append((d(ano, mes, random.randint(1, 28)), random.choice(["Roupas", "Eletrônicos", "Casa e decoração", "Presente"]),
                  "Compras", "Despesa", money(70, 320), "Cartão de crédito"))
    # Outros
    for _ in range(random.randint(1, 3)):
        L.append((d(ano, mes, random.randint(1, 28)), random.choice(["Barbeiro", "Lavanderia", "Taxa bancária", "Correios"]), "Outros", "Despesa", money(18, 95), random.choice(PAG[:3])))

L.sort(key=lambda x: x[0])
with open("lancamentos.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["lancamento_id", "data", "descricao", "categoria", "tipo", "valor", "forma_pagamento"])
    for i, (dt, ds, ct, tp, vl, fp) in enumerate(L, 1):
        w.writerow([i, dt.isoformat(), ds, ct, tp, f"{vl:.2f}", fp])

ORC = [("Moradia", 1900), ("Alimentação", 1100), ("Transporte", 450), ("Saúde", 250), ("Lazer", 400),
       ("Educação", 200), ("Assinaturas", 120), ("Compras", 350), ("Outros", 200)]
with open("orcamento.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["categoria", "orcamento_mensal"]); w.writerows(ORC)

pickle.dump((L, ORC, MESES), open("dados.pkl", "wb"))
rec = sum(x[4] for x in L if x[3] == "Receita"); desp = sum(x[4] for x in L if x[3] == "Despesa")
print(len(L), "lançamentos | receitas", round(rec, 2), "| despesas", round(desp, 2), "| saldo", round(rec - desp, 2))
for m in MESES:
    r = sum(x[4] for x in L if x[3] == "Receita" and (x[0].year, x[0].month) == m)
    dd = sum(x[4] for x in L if x[3] == "Despesa" and (x[0].year, x[0].month) == m)
    print(m, round(r), round(dd), round(r - dd))
