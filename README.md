# Competição de Liga 4

O objetivo deste projeto é armazenar todos os artefatos referentes a competição de Liga4 do segundo semestre de 2022. Todas as implementações dos jogadores participantes estão no diretório [./src/games/fourinrow_popout/](./src/games/fourinrow_popout/). Os logs das pré-competições e das competições estão em [./src/games/fourinrow_popout/results/](./src/games/fourinrow_popout/results/). 

## Jogadores desclassificados

| Nome da equipe | Motivo | Evidências |
|:---------------|:-------|:-----------|
|Bergsons4       | Exception: Player Bergsons4, you can not pop out from an empty column nor pop out a piece that is not yours. | Este jogador gera uma exception toda vez que é inserido na competição. Os logs de erro podem ser vistos em: [1](./src/games/fourinrow_popout/results/log_error_campeonato_bergsons4.txt) e [2](./src/games/fourinrow_popout/results/log_error_campeonato_bergsons4_2x.txt). Os logs das competições onde este erro foi gerado são: [1](./src/games/fourinrow_popout/results/log_campeonato_bergsons4.txt) e [2](./src/games/fourinrow_popout/results/log_campeonato_bergsons4_2x.txt). |
| AI_vs_Mecat    | Exception: Player Mecat, you can not pop out from an empty column nor pop out a piece that is not yours. | Este erro foi identificado em execuções de pré-campeonato. Os logs estão em: [1](./src/games/fourinrow_popout/results/log_campeonato_com_ai_vs_mecat.txt) e [2](./src/games/fourinrow_popout/results/log_error_campeonato_com_ai_vs_mecat.txt). | 
| Palestra       | TypeError: 'NoneType' object is not subscriptable | Este erro foi identificado em execuções de pré-campeonato. Os logs estão em: [1](./src/games/fourinrow_popout/results/log_campeonato_palestra.txt) e [2](./src/games/fourinrow_popout/results/log_error_campeonato_palestra.txt). |

## Resultados da competição

A competição foi executada 3 vezes sem nenhuma interrupção. 

* A primeira competição iniciou às `2022-11-18 23:58` e terminou às `2022-11-19 00:50:31`. Alguns jogadores fizeram uso do tempo máximo permitido por jogada, mas nenhum ultrapassou o limite de **10 segundos**. Nenhum jogador perdeu do jogador aleatório. O log da competição pode ser visto no arquivo [src/games/fourinrow_popout/results/log_campeonato1.txt](./src/games/fourinrow_popout/results/log_campeonato1.txt). O resultado da primeira competição foi: 

```
{'Random': 0, 'AIPlayer': 12, '4_e_par': 4, 'Akatsuki': 6, 'Carlos Monteiro - baladesejo': 16, 'Celta Preto': 19, 'Grupo_X': 9, 'Aranhatron 8000': 16, 'Marco': 5, 'Robotica': 14, 'Trio_De_Ferro': 9}
```

* A segunda competição iniciou às `2022-11-19 07:58` e terminou às `2022-11-19 08:47`. Alguns jogadores fizeram uso do tempo máximo permitido por jogada, mas nenhum ultrapassou o limite de **10 segundos**. Nenhum jogador perdeu do jogador aleatório. O log da competição pode ser visto no arquivo [src/games/fourinrow_popout/results/log_campeonato2.txt](./src/games/fourinrow_popout/results/log_campeonato2.txt). O resultado da segunda competição foi:

```
{'Random': 0, 'AIPlayer': 12, '4_e_par': 4, 'Akatsuki': 6, 'Carlos Monteiro - baladesejo': 17, 'Celta Preto': 19, 'Grupo_X': 9, 'Aranhatron 8000': 16, 'Marco': 5, 'Robotica': 13, 'Trio_De_Ferro': 9}
```

* A terceira competição iniciou às `2022-11-19 16:53` e terminou às `2022-11-19 17:45`. Alguns jogadores fizeram uso do tempo máximo permitido por jogada, mas nenhum ultrapassou o limite de **10 segundos**. Nenhum jogador perdeu do jogador aleatório. O log da competição pode ser visto no arquivo [src/games/fourinrow_popout/results/log_campeonato3.txt](./src/games/fourinrow_popout/results/log_campeonato3.txt). O resultado da segunda competição foi:

```
{'Random': 0, 'AIPlayer': 12, '4_e_par': 4, 'Akatsuki': 6, 'Carlos Monteiro - baladesejo': 15, 'Celta Preto': 19, 'Grupo_X': 9, 'Aranhatron 8000': 17, 'Marco': 5, 'Robotica': 13, 'Trio_De_Ferro': 10}
```

Os resultados apresentados nas 3 execuções da competição foram consistentes, como pode-se ver na tabela abaixo:

| Jogador                           | Execução 1 | Execução 2 | Execução 3 | Colocação  | 
|:--------                          |:----------:|:----------:|:----------:|:----------:|
|Random                             | 0 | 0 | 0    |
|AIPlayer - 4Connect                | 12 | 12 | 12 | 4o lugar|
|4_e_par                            | 4 | 4 | 4    | 8o lugar|
|Akatsuki                           | 6 | 6 | 6    | 6o lugar|
|Carlos Monteiro - baladesejo       | 16 | 17 | 15 | 2o lugar|
|Celta Preto                        | 19 | 19 | 19 | Campeão |
|Grupo_X                            | 9 | 9 | 9    | 5o lugar|
|Aranhatron 8000                    | 16 | 16 | 17 | 2o lugar|
|Marco                              | 5 | 5 | 5    | 7o lugar|
|Robotica                           | 14 | 13 | 13 | 3o lugar|
|Trio_De_Ferro                      | 9 | 9 | 10   | 5o lugar|


## Re-execução da competição

Caso você queira, é possível executar novamente a competição. Neste caso basta executar os seguintes comandos: 

```bash
cd src/games/fourinrow_popout/
python Tournament.py
```

Se você quiser gerar os arquivos de log, basta digitar: 

```bash
python Tournament.py log
```

## Notas finais

A seguir são apresentadas as notas finais, incluindo a parte de documentação: 

| Nome Equipe | Documentação | Competição | Observações | Nota Final |
|:------------|:------------:|:----------:|:------------|:-----------|
| 4Connect	|A+	|C|	----| 7.5|
|4_e_par	|C	|C|	Não foi alterado o nome do jogador no método name(). Modificações irrelevantes no código. Não apresenta dados que sustentam as respostas. Por exemplo, dados sobre os testes.| 5|
|AI_vs_Mecat|B |I|	Exception: Player Mecat, you can not pop out from an empty column nor pop out a piece that is not yours. Não apresenta dados que sustentam as respostas. Por exemplo, dados sobre os testes.| 4.5|
|Akatsuki-4| A+|C|	----| 7.5|
|baladesejo|A+|	A|	----| 9.5|
|Bergsons4|	A+|	I|	Exception: Player Bergsons4, you can not pop out from an empty column nor pop out a piece that is not yours.| 6|
|celta_preto|A+|A+|	----| 10|
|grupo_x|B|	C|Não apresenta dados que sustentam as respostas. Por exemplo, dados sobre os testes.| 6|
|G_Aranha|	A|	A| 	Não tem o link para o documento "Research on different heuristics..."  A implementação tinha uns prints "sobrando".| 9|
|MarMoli|C|	C|Não tem referências, não responde todas as perguntas. A implementação tinha uns prints "sobrando" | 5|
|palestra|B|I|Não apresenta dados que sustentam as respostas. Por exemplo, dados sobre os testes. TypeError: 'NoneType' object is not subscriptable| 4.5|
|robotics4|	B|	B|	Poucas modificações feitas a partir do código referência. Não apresenta dados que sustentam as respostas. Por exemplo, dados sobre os testes.|7 |
|TrioDeFerro|B|	C|	Poucas modificações feitas a partir do código referência. Não apresenta dados que sustentam as respostas. Por exemplo, dados sobre os testes.|6 |