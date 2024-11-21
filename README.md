# Poker-Simulator

## Architecture
``sources``

``game.py``
``croupier.py``
``bot.py``

``class Poker_game``
``class player``
``class croupier``



Initialisation de la partie : ``class Poker_game()``

paramètres qui doivent être initialisés pour une partie:
- joueurs : list d'id (str)
- blind initiale : variable ``b`` > 0
- stacks initiaux : dictionnaire ``Stacks : { joueurs : stack }``
- règle d'évolution de la blind, tuple (frequence, multiplicateur) : on multiplie la blind tout les x tours de table

class ``croupier(Poker_game)`` : (?)
- gère la distirbution des cartes (?)

Initialisation : ``class Table(Poker_game)``

- Créer un ordre aléatoire et fixe dans les joueurs : ``J_table = [1 : j_?, ..., p : j_?]``
- initialise la position du dealer : ``dealer_pos : int``
- initialise un croupier (classe croupier)

Mise à jour de la table entre chaque round :
- met à jour la position du dealer :
    dealer pos += 1 moduelo nombre joueurs
    dealer_id = id du dealer
    if Stacks[dealer_id] == 0 :
        on skip ce tour de dealer
- augmente la blind si necessaire


clas round(Table) :

- initialiser pot à 0
- initialiser mise minimale à 0

- initialise la liste des joueurs actifs dans le round (ceux avec un stack non nul) : ``J_round = [joueurs if Stack[joueurs > 0]]``
- dictionnaire : ``Round = {joueurs : {état : wait , mise actuelle : 0 , cartes : (_,_)} }``

- on suit les différentes étapes du jeux : ``Step = [Preflop, Flop, Turn, River]``

desctiption de la variable ``état`` du dict ``Round`` : 
- au début tout le monde est en wait car personne n'a parlé
- lorsqu'une personne parle, son état passe soit en call (si check ou call), soit en fold
- si une personne est en fold, on ne lui propose plus jamais de parlé lors du round
- si une personne est wait, on ne termine pas le round mais on lui demande de parlé
- si une personne est en call :
    - si la mise minimale = mise du joueur, on termine la phase du round (preflop, flop etc..)
    - si la mise minimale > mise du joueur (cela veut dire qu'il y a eu un raise), on propose au joueur de parler à nouveau


- Preflop :

    - croupier distribue les cartes aux joueurs : mise à jour du dict ``Round``
    - petite blind/ grosse blind mise auto grâce à la variable ``Dealer_pos`` : 
        - ``id_petite  = J_pos[Dealer]`` et ``id _grosse = J_pos[Dealer+1]``
        - stack du joueur petite blinde diminue de 0.5 blind
        - stack du joueur grosse blind diminue de 1 blind
        - mise à jour de ``Round`` pour rajouter la mise actuelle de id_petite et id_grosse
        - pot += petite + grosse
    - mise minimale fixer à grosse blind
    - for j > ``Dealer_pos`` + 2 :
        - if l'état du joueur j est fold, pass
        - if mise joueurs j == mise minimale actuelle et état joueurs j == call, end preflop
        - else : action du joueur j, mise possible entre minimale actuelle- mise_joueur_j ou fold
        - if action = fold : 
            - état joueur j devient fold
            - check s'il reste plus d'un joueurs actif, sinon on lui ajoute le pot à son stack et on termine le round
        - if action = call : mise à jour de la mise actuelle joueur j, pot += mise joueur j, etc
        - if action = raise : pareil + mise à jour mise minimale to raise value

- Flop :
    - croupier deal 3 cartes visibles par tt le monde
    - On remet les joueurs qui n'ont pas fold en état d'attente de parole :
        Round[players[état]] = wait if Round[players[état]] not fold
        Round[players[mise actuelle]] = 0
        mise minimale = 0
    - for j >  ``Dealer_pos`` :
        - on répète le proceess de mises précédent
- Turn :
    - croupier révèle 1 cartes visible par tt le monde.
    - for j > dealer :
        on répète le proceess de mises précédent
- River :
    - croupier révèle 1 cartes visible par tt le monde.
    - for j > dealer :
    - on répète le proceess de mises précédent (sans la partie petite grosse)
    lorsqu'on atteint end_river :
        - si il y a plus d'un joueurs actifs, alors ils révèlent leurs cartes et le croupier donne un gagnant,
