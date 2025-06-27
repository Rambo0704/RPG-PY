# Fígado's Adventure

![Python](https://img.shields.io/badge/python-3.x-blue.svg) ![Pygame](https://img.shields.io/badge/pygame-2.x-green.svg)

## 📖 Sobre o Jogo

**Fígado's Adventure** é um jogo de RPG em turnos onde o bravo herói, Fígado, enfrenta inimigos temíveis que representam bebidas alcoólicas. O objetivo é sobreviver a múltiplas fases de combate, fortalecer o personagem e, por fim, triunfar sobre a cirrose.

O jogo foi desenvolvido em Python com a biblioteca Pygame para a criação da interface gráfica e gerenciamento dos elementos visuais.

## ✨ Funcionalidades Principais

* **Combate em Turnos:** Sistema clássico de RPG onde jogador e inimigo se alternam em turnos para atacar, usar habilidades ou se defender,aonde esses turnos saão feitos utilizando o sistema de semaforização.
* **Sistema de Stamina:** Ações como atacar, usar ataques críticos ou esquivar consomem stamina, que pode ser recuperada com o sistema de Threads, adicionando uma camada tática ao combate.
* **Loja de Buffs:** Após vencer uma batalha, o jogador pode visitar uma loja para comprar melhorias para o personagem, como aumento de ataque, escudo, vida e stamina, utilizando as moedas ganhas.
* **Progressão de Fases:** O jogo é estruturado em fases, cada uma com um inimigo diferente e mais forte, como "Cerveja", "Cachaça" e "Absinto".
* **Interface Gráfica Completa:** O jogo conta com telas de menu, batalha, loja e fim de jogo, todas construídas com Pygame, incluindo sprites para os personagens, barras de status e botões interativos.
* **Trilha Sonora:** Músicas de fundo com o sistema de Threads são utilizadas para criar a atmosfera do menu, das batalhas e das telas de vitória/derrota.

## 🚀 Como Executar

Para rodar o projeto, você precisará ter o Python e o Pygame instalados.

1.  **Instale o Pygame:**
    ```bash
    pip install pygame
    ```

2.  **Execute o Jogo:**
    Navegue até a pasta raiz do projeto e execute o arquivo `main.py`:
    ```bash
    python main.py
    ```

## 🎮 Mecânicas do Jogo

### Combate
O combate é a parte central do jogo. Em cada turno, o jogador pode escolher uma das seguintes ações:
* **Atacar:** Um ataque padrão que causa dano com base no atributo de `ataque` do personagem e consome 10 de stamina.
* **Crítico:** Um ataque mais forte que causa o dobro do dano, mas consome 30 de stamina e tem 50% de chance de errar.
* **Esquivar:** Permite evitar o próximo ataque do inimigo. Custa 20 de stamina.
* **Recuperar Stamina:** O jogador pode optar por recuperar sua stamina ao longo do tempo.

### Personagem
A classe `Personagem` define as entidades do jogo (o jogador "Fígado" e os inimigos). Seus principais atributos são:
* **Vida:** Pontos de saúde do personagem. Se chegar a zero, o jogo acaba.
* **Ataque:** Define o dano base dos ataques.
* **Escudo:** Reduz o dano recebido.
* **Stamina:** Recurso necessário para executar a maioria das ações em combate.
* **Moedas:** Usadas para comprar buffs na loja.

### Loja e Buffs
Após cada vitória, o jogador ganha moedas e acesso a uma loja onde pode comprar `Buffs`. Esses buffs podem aumentar permanentemente os atributos de ataque e escudo ou recuperar vida e stamina para a próxima batalha.

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem de programação principal do projeto.
* **Pygame:** Biblioteca utilizada para a criação da interface gráfica, manipulação de sprites, áudio e eventos do jogo.

## 👥 Créditos

Este projeto foi desenvolvido por:
* Gabriel Rambo
* Pedro Viegas
* Pedro Miguel
* Rafael Machado

*(Créditos mencionados na tela de fim de jogo do projeto)*
