# farmtech.py
# App simples de terminal: duas culturas (algodao, feijao),
# triângulo retângulo para área, e kg de insumo por dose fixa (kg/ha).
# Vetores (listas), menu com CRUD e exportação CSV.

import csv

CULTURAS = ["algodao", "feijao"]
DOSES = {
    "algodao": {"produto": "Nitrogenio (N)", "dose_kg_ha": 100.0},
    "feijao":  {"produto": "Fosforo (P)",    "dose_kg_ha":  50.0},
}

dados = {
    "algodao": {"base": [], "altura": [], "area_m2": [], "kg_insumo": []},
    "feijao":  {"base": [], "altura": [], "area_m2": [], "kg_insumo": []},
}

def area_triangulo(base_m, altura_m):
    return (base_m * altura_m) / 2.0  # m²

def kg_por_area(area_m2, dose_kg_ha):
    return dose_kg_ha * (area_m2 / 10000.0)

def escolher_cultura():
    while True:
        print("\nEscolha a cultura: [1] algodao  [2] feijao")
        op = input(">> ").strip()
        if op == "1": return "algodao"
        if op == "2": return "feijao"
        print("Opção inválida.")

def ler_float(msg, minimo=0.0):
    while True:
        try:
            v = float(input(msg).replace(",", "."))
            if v < minimo:
                print(f"Valor deve ser >= {minimo}.")
                continue
            return v
        except ValueError:
            print("Número inválido, tente de novo.")

def listar(cultura):
    b = dados[cultura]["base"]
    h = dados[cultura]["altura"]
    a = dados[cultura]["area_m2"]
    k = dados[cultura]["kg_insumo"]
    if not a:
        print(f"\nNenhum registro para {cultura}.")
        return
    print(f"\n--- Registros de {cultura} ---")
    prod = DOSES[cultura]["produto"]
    dose = DOSES[cultura]["dose_kg_ha"]
    print(f"Insumo: {prod} | dose: {dose} kg/ha")
    for i in range(len(a)):
        print(f"[{i}] base={b[i]} m, altura={h[i]} m, área={a[i]:.2f} m², insumo={k[i]:.2f} kg")

def cadastrar():
    cultura = escolher_cultura()
    base = ler_float("Base (m): ")
    altura = ler_float("Altura (m): ")
    area = area_triangulo(base, altura)
    dose = DOSES[cultura]["dose_kg_ha"]
    kg = kg_por_area(area, dose)
    for chave, val in [("base", base), ("altura", altura), ("area_m2", area), ("kg_insumo", kg)]:
        dados[cultura][chave].append(val)
    print(f"Cultura cadastrada! área={area:.2f} m² | insumo={kg:.2f} kg ({DOSES[cultura]['produto']})")

def atualizar():
    cultura = escolher_cultura()
    listar(cultura)
    if not dados[cultura]["area_m2"]:
        return
    try:
        idx = int(input("Índice para atualizar: "))
    except ValueError:
        print("Índice inválido."); return
    if idx < 0 or idx >= len(dados[cultura]["area_m2"]):
        print("Índice fora da faixa."); return

    print("Atualizar: [1] base  [2] altura")
    op = input(">> ").strip()
    if op == "1":
        dados[cultura]["base"][idx] = ler_float("Nova base (m): ")
    elif op == "2":
        dados[cultura]["altura"][idx] = ler_float("Nova altura (m): ")
    else:
        print("Opção inválida."); return

    b = dados[cultura]["base"][idx]
    h = dados[cultura]["altura"][idx]
    area = area_triangulo(b, h)
    dose = DOSES[cultura]["dose_kg_ha"]
    kg = kg_por_area(area, dose)
    dados[cultura]["area_m2"][idx] = area
    dados[cultura]["kg_insumo"][idx] = kg
    print("Registro atualizado!")

def deletar():
    cultura = escolher_cultura()
    listar(cultura)
    if not dados[cultura]["area_m2"]:
        return
    try:
        idx = int(input("Índice para remover: "))
    except ValueError:
        print("Índice inválido."); return
    if idx < 0 or idx >= len(dados[cultura]["area_m2"]):
        print("Índice fora da faixa."); return
    for k in ["base", "altura", "area_m2", "kg_insumo"]:
        dados[cultura][k].pop(idx)
    print("Registro removido.")

def exportar_csv():
    with open("culturas.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cultura", "base_m", "altura_m", "area_m2", "produto", "dose_kg_ha", "kg_necessarios"])
        for cultura in CULTURAS:
            prod = DOSES[cultura]["produto"]
            dose = DOSES[cultura]["dose_kg_ha"]
            n = len(dados[cultura]["area_m2"])
            for i in range(n):
                w.writerow([
                    cultura,
                    dados[cultura]["base"][i],
                    dados[cultura]["altura"][i],
                    dados[cultura]["area_m2"][i],
                    prod,
                    dose,
                    dados[cultura]["kg_insumo"][i],
                ])
    print('Arquivo "culturas.csv" exportado!')

def mostrar_doses():
    print("\n--- Doses fixas ---")
    for c in CULTURAS:
        print(f"- {c}: {DOSES[c]['produto']} = {DOSES[c]['dose_kg_ha']} kg/ha")

def menu():
    while True:
        print("""
===== FarmTech Solutions =====
[1] Cadastrar cultura
[2] Listar por cultura
[3] Atualizar por índice
[4] Deletar por índice
[5] Exportar CSV
[6] Ver doses fixas
[0] Sair
""")
        op = input("Escolha: ").strip()
        if op == "1": cadastrar()
        elif op == "2": listar(escolher_cultura())
        elif op == "3": atualizar()
        elif op == "4": deletar()
        elif op == "5": exportar_csv()
        elif op == "6": mostrar_doses()
        elif op == "0":
            print("Até mais!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
