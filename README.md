# Poker-Simulator

## Architecture
sources

game.py
croupier.py
bot.py

class poker
class player
class croupier



from sources/game import poker

classe bot() ??

Initialisation de la partie : classe Poker()

paramètres :
- joueurs : list d'id 
- blind initiale b > 0
- stacks : dictionnaire { joueurs : stack}
- règle d'évolution de la blind

Initialisation : classe table(Poker) ?? super_init

- Créer un ordre fixe dans les joueurs : J = [j_1, ..., j_p]
- initialiser la variable dealer

Mise à jour de la table entre chaque tour :
- delete joueurs avec stacks = 0
- change le dealer
- upgrade la blind si necessaire
- donner une glace au croupier

Créer une classe round(Table) :
- dealer distribue les cartes aux joueurs
- Preflop : 
    - petite blind/ grosse blind mise auto
    - for j in Joueurs à partir du Dealer + 2 :
        - action du joueurs j
        - stop if 
    - 
- Flop :
- Turn :
- River :
