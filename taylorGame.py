import pygame
import sys
import math
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura_tela = 1280  # Aumenta a largura da tela
altura_tela = 720  # Aumenta a altura da tela
tela = pygame.display.set_mode((largura_tela, altura_tela))

# Configurações do jogador
posicao_jogador = [50, 50]
velocidade_jogador = 0.8 
tamanho_jogador = 25
vidas = 5

# Configurações do inimigo
num_inimigos = 4
inimigos = []
for _ in range(num_inimigos):
    while True:
        posicao_inimigo = [random.randint(0, largura_tela), random.randint(0, altura_tela)]
        dx = posicao_jogador[0] - posicao_inimigo[0]
        dy = posicao_jogador[1] - posicao_inimigo[1]
        dist = math.hypot(dx, dy)
        if dist > 100:  # Garante que o inimigo não apareça muito perto do jogador
            break
    inimigos.append({
        'posicao': posicao_inimigo,
        'velocidade': 0.5,
        'tamanho': 25,
    })

# Configurações do tiro
tiros = []
velocidade_tiro = 5
tamanho_tiro = 5

# Configurações das fases
fase = 1
inimigos_eliminados = 0
inimigos_por_fase = {1: 30, 2: 40, 3: 60}

# Configurações da interface
fonte = pygame.font.Font(None, 36)

# Loop principal do jogo
while True:
    # Eventos do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tiro = pygame.Rect(posicao_jogador[0], posicao_jogador[1], tamanho_tiro, tamanho_tiro)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - posicao_jogador[0]
                dy = mouse_y - posicao_jogador[1]
                dist = math.hypot(dx, dy)
                dx, dy = dx / dist, dy / dist  # Normaliza o vetor
                tiros.append((tiro, dx, dy))

    # Movimento do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and posicao_jogador[0] > 0:
        posicao_jogador[0] -= velocidade_jogador
    if keys[pygame.K_d] and posicao_jogador[0] < largura_tela - tamanho_jogador:
        posicao_jogador[0] += velocidade_jogador
    if keys[pygame.K_w] and posicao_jogador[1] > 0:
        posicao_jogador[1] -= velocidade_jogador
    if keys[pygame.K_s] and posicao_jogador[1] < altura_tela - tamanho_jogador:
        posicao_jogador[1] += velocidade_jogador

    # Movimento dos inimigos
    for inimigo in inimigos:
        dx = posicao_jogador[0] - inimigo['posicao'][0]
        dy = posicao_jogador[1] - inimigo['posicao'][1]
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist  # Normaliza o vetor
        inimigo['posicao'][0] += dx * inimigo['velocidade']
        inimigo['posicao'][1] += dy * inimigo['velocidade']

    # Verifica se os inimigos tocaram o jogador
    for inimigo in inimigos:
        if pygame.Rect(posicao_jogador[0], posicao_jogador[1], tamanho_jogador, tamanho_jogador).colliderect(pygame.Rect(inimigo['posicao'][0], inimigo['posicao'][1], inimigo['tamanho'], inimigo['tamanho'])):
            vidas -= 1
            if vidas == 0:
                vidas = 5
                fase = 1
                inimigos_eliminados = 0
            posicao_jogador = [50, 50]  # O jogador volta para a posição inicial
            inimigo['posicao'] = [random.randint(0, largura_tela), random.randint(0, altura_tela)]  # O inimigo reaparece em uma nova posição
            tiros = []  # Todos os tiros são removidos

    # Movimento dos tiros
    for tiro, dx, dy in tiros:
        tiro.move_ip(dx * velocidade_tiro, dy * velocidade_tiro)
        for inimigo in inimigos:
            if tiro.colliderect(pygame.Rect(inimigo['posicao'][0], inimigo['posicao'][1], inimigo['tamanho'], inimigo['tamanho'])):
                tiros.remove((tiro, dx, dy))
                inimigo['posicao'] = [random.randint(0, largura_tela), random.randint(0, altura_tela)]  # O inimigo reaparece em uma nova posição
                inimigos_eliminados += 1
                if inimigos_eliminados >= inimigos_por_fase[fase]:
                    fase += 1
                    inimigos_eliminados = 0

    # Atualiza a tela
    tela.fill((0, 0, 0))
    pygame.draw.rect(tela, (255, 0, 0), (posicao_jogador[0], posicao_jogador[1], tamanho_jogador, tamanho_jogador))
    for inimigo in inimigos:
        pygame.draw.rect(tela, (0, 255, 0), (inimigo['posicao'][0], inimigo['posicao'][1], inimigo['tamanho'], inimigo['tamanho']))
    for tiro, dx, dy in tiros:
        pygame.draw.rect(tela, (255, 255, 255), tiro)
    texto_vidas = fonte.render('Vidas: ' + str(vidas), True, (255, 255, 255))
    tela.blit(texto_vidas, (10, 10))
    texto_fase = fonte.render('Fase: ' + str(fase), True, (255, 255, 255))
    tela.blit(texto_fase, (10, 50))
    pygame.display.flip()