import random

tabuleiro = {
    2: 12,
    5: 15,
    9: 27,
    18: 29,
    25: 35,
    14: 4,
    17: 7,
    20: 8,
    22: 11,
    32: 30,
    34: 24
}

CASA_FINAL = 36

def jogar_partida(
    chance_escada=1.0,
    inicio_jogador_2=1,
    imunidade_primeira_cobra_jogador_2=False
):
    posicoes = [1, inicio_jogador_2]
    total_cobras = 0
    total_lancamentos = 0
    imunidade_usada = False
    jogador_atual = 0

    while True:
        total_lancamentos += 1
        dado = random.randint(1, 6)
        posicoes[jogador_atual] += dado

        if posicoes[jogador_atual] >= CASA_FINAL:
            return {
                "vencedor": jogador_atual,
                "cobras": total_cobras,
                "lancamentos": total_lancamentos
            }

        if posicoes[jogador_atual] in tabuleiro:
            destino = tabuleiro[posicoes[jogador_atual]]

            if destino > posicoes[jogador_atual]:
                if random.random() <= chance_escada:
                    posicoes[jogador_atual] = destino
            else:
                if (
                    jogador_atual == 1
                    and imunidade_primeira_cobra_jogador_2
                    and not imunidade_usada
                ):
                    imunidade_usada = True
                else:
                    posicoes[jogador_atual] = destino
                    total_cobras += 1

        jogador_atual = 1 - jogador_atual

def simular(jogos=10000, **parametros):
    vitorias_jogador_1 = 0
    soma_cobras = 0
    soma_lancamentos = 0

    for _ in range(jogos):
        resultado = jogar_partida(**parametros)
        if resultado["vencedor"] == 0:
            vitorias_jogador_1 += 1
        soma_cobras += resultado["cobras"]
        soma_lancamentos += resultado["lancamentos"]

    return {
        "prob_vitoria_jogador_1": vitorias_jogador_1 / jogos,
        "media_cobras": soma_cobras / jogos,
        "media_lancamentos": soma_lancamentos / jogos
    }

resultado = simular()
print("\nNome:Gabriel Pereira Viana\nData: 17/01/2026 \nRespostas:")
print("\nprobabilidade_vitoria_jogador_1: ",round(resultado["prob_vitoria_jogador_1"]*100,2),"%")
print("\nmedia_cobras_por_jogo: ",round(resultado["media_cobras"],2))

resultado2 = simular(chance_escada=0.5)
print("\nnº_medio_completar_escada_0.5: ",round(2*resultado2["media_lancamentos"],2),"\n")

resultados_equilibrio = []

for casa_inicial in range(1, 6):
    resultado = simular(inicio_jogador_2=casa_inicial)

    resultados_equilibrio.append({
        "inicio_jogador_2": casa_inicial,
        "prob_vitoria_jogador_1": resultado["prob_vitoria_jogador_1"]
    })

for item in resultados_equilibrio:
    print(
        "Jogador 2 começa na casa",
        item["inicio_jogador_2"],
        "- Probabilidade de vitória do Jogador 1:",
        round(item["prob_vitoria_jogador_1"], 2)
    )


resultado5 = simular(imunidade_primeira_cobra_jogador_2=True)
print("\nprobabilidade_jogador2_com_imunidade: ",100*round(resultado5["prob_vitoria_jogador_1"],2),"%\n")
