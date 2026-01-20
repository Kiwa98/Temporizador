# Temporizador

 
 DOCUMENTAÇÃO TÉCNICA
Sistema de Temporização de Esteira com Sinalização Manual
1. Visão Geral

Este sistema foi desenvolvido para controlar uma esteira transportadora por tempo, utilizando um ciclo automático de ligado/parado, com sinalização manual independente através de uma lâmpada verde acionada pelo operador.

O sistema é composto por:

Um PC com interface gráfica (Python + Tkinter)

Um Arduino com dois relés

Relé da esteira

Relé da lâmpada verde

Não há sensores envolvidos nesta versão do sistema.

2. Objetivo do Sistema

Garantir que a esteira opere em ciclos temporizados, impondo um ritmo fixo de trabalho.

Permitir que o operador sinalize uma ação (ex: OK visual) através de uma lâmpada verde, sem interferir no ciclo da esteira.

Substituir soluções puramente elétricas ou inversores simples, oferecendo lógica de controle semelhante a um CLP.

3. Arquitetura do Sistema
3.1 Diagrama Conceitual (Lógico)
<img width="666" height="243" alt="image" src="https://github.com/user-attachments/assets/bd5b55c5-8523-4f95-bcd6-cd4ce6a9dc66" />


4. Componentes Utilizados
4.1 Software (PC)

Python 3.x

Tkinter (Interface Gráfica)

PySerial (Comunicação Serial)

Pynput (Captura global da tecla ENTER)

4.2 Hardware

Arduino (Uno, Nano ou equivalente)

Módulo de relés (ativo em nível baixo)

Esteira transportadora

Lâmpada verde de sinalização

Fonte de alimentação adequada

5. Funcionamento Geral
5.1 Inicialização do Sistema

O operador seleciona a porta COM na interface.

O operador clica em “Iniciar Sistema”.

O sistema:

Abre a comunicação serial com o Arduino

Ativa o modo automático

Liga a esteira imediatamente

Inicia a contagem do tempo de esteira ligada

⚠️ Importante: o temporizador não depende do ENTER para iniciar.

6. Lógica do Temporizador (Automático)

O sistema opera em loop contínuo, com dois estados principais:

6.1 Estado: ESTEIRA LIGADA

A esteira é acionada imediatamente.

Inicia-se a contagem do Tempo Ligada (configurável em segundos).

Ao final do tempo:

A esteira é desligada

O sistema muda para o estado PARADA

6.2 Estado: ESTEIRA PARADA

A esteira permanece desligada.

Inicia-se a contagem do Tempo Parada (configurável em segundos).

Ao final do tempo:

O sistema retorna ao estado LIGADA

A esteira é religada automaticamente

6.3 Ciclo Contínuo
LIGADA → (Tempo Ligada) → PARADA → (Tempo Parada) → LIGADA → ...


Este comportamento é equivalente a dois temporizadores TON em um CLP.

7. Funcionamento do Leitura do QR (Automatica)
7.1 Ação da Leitura

A Leitura é monitorada globalmente.

Ao ser pressionada:

O sistema envia um comando ao Arduino

O relé da lâmpada verde é acionado

A lâmpada permanece ligada por 0,5 segundos

A lâmpada é desligada automaticamente

7.2 Independência do Ciclo

O ENTER:

❌ Não liga a esteira

❌ Não para a esteira

❌ Não reinicia o temporizador

O ciclo automático continua inalterado.

8. Interface Gráfica (IHM)
8.1 Elementos Disponíveis

Seleção da porta COM

Ajuste do tempo de:

Esteira LIGADA

Esteira PARADA

Indicadores visuais:

Estado da esteira (Ligada / Parada)

Modo do ciclo (Ligada / Parada)

Tempo restante do ciclo

Área de log de eventos

9. Comunicação Serial
9.1 Comandos Enviados do PC para o Arduino
Comando	Função
ESTEIRA_ON	Liga o relé da esteira
ESTEIRA_OFF	Desliga o relé da esteira
LUZ_VERDE_PULSO	Liga a lâmpada verde por 0,5s
10. Segurança e Estabilidade

A interface gráfica é atualizada utilizando método thread-safe (after), evitando travamentos.

O controle de tempo é baseado em timestamp real, garantindo precisão.

O sistema não depende de sensores, reduzindo pontos de falha.

A lógica de controle segue padrão de máquina de estados simples (FSM).


