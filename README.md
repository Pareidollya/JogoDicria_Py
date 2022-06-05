# JogoDicria_Py
jogo dicria utilizando python arcade. Para avaliação de Processamento de imagens.

objetivo: Sobreviver o máximo.

Ideias pré-desenvolvimento:

    mapa básico;

    mecânicas básicas de movimentação ;

    spawn de inimigos;

    direcionamento dos inimigos;
    
    colisão do inimigo ao player e tirar vida;

    direcionar inimigos ao player;

    mecânicas de disparo do player;

    colisão do disparo a inimigos;

    pontuação por kill;

    aumentar a dificuldade por segundo passado (surgir inimigos);

    tipos de inimigo;
    
    limitar numero de disparos (munição) - spawn ao disparar em tempo aleatório;
    
    recuperar vida - spawn ao perder vida em tempo aleatório;


Desenvolvimento:

    Funções de movimentação no: w a s d;

    Sprites e colisão;

    Vida do jogador (perder vida na colisão);

    Movimentação das sprites pelo mapa;

    Disparar;
    
    Timer para exibição do tempo e controlar mecanicas de resurgimento;

    Resurgir novos sprites caso esteja abaixo do numero configurado;

    Sprites que seguem o player;

    Aumentar numero de surgimentos e velocidade dos sprites conforme o tempo avance;






Materiais de referencia utilizados 

   Python arcade: https://api.arcade.academy/en/latest/index.html

   Movimentação: https://api.arcade.academy/en/latest/examples/sprite_move_keyboard.html#sprite-move-keyboard
    
   Bouncing sprites: https://api.arcade.academy/en/latest/examples/sprite_collect_coins_move_bouncing.html#sprite-collect-coins-move-bouncing

   Follower sprites: https://api.arcade.academy/en/latest/examples/sprite_follow_simple.html#sprite-follow-simple

   Disparos: https://api.arcade.academy/en/latest/examples/sprite_bullets_aimed.html#sprite-bullets-aimed

   Timer: https://api.arcade.academy/en/latest/examples/timer.html#timer
