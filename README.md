# Poker-Simulator

## Architecture
sources

game.py
croupier.py
bot.py

class poker
class player
class croupier


classe bot() ??

Initialisation de la partie : classe Poker_game()

paramètres qui doivent être initialisé pour une partie:
- joueurs : list d'id
- blind initiale b > 0
- stacks initiaux : dictionnaire { joueurs : stack }
- règle d'évolution de la blind

Initialisation : classe table(Poker)

- Créer un ordre fixe dans les joueurs : J = [j_1, ..., j_p]
- initialise la variable dealer
- initialise le croupier

Mise à jour de la table entre chaque tour :
- delete joueurs avec stacks = 0
- change le dealer
- upgrade la blind si necessaire

classe croupier() :
- permet de gérer un tour et notamment les mises

classe round(Table) :

- croupier initialise la liste des joueurs actifs initialement dans le round
- croupier distribue les cartes aux joueurs

- Preflop : 
    - petite blind/ grosse blind mise auto
    - for j in Joueurs actifs à partir du Dealer + 2 :
        - action du joueur j
        - if action == fold : joueur j n'est plus actif
        - if action call
    - 
- Flop :
- Turn :
- River :
