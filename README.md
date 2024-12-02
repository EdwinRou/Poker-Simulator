# Poker-Simulator

## Architecture
`sources`

`game.py`
`croupier.py`
`bot.py`

`class Poker_game`
`class Table`
`class Round`  

Maybe :
`class player`
`class croupier`


Convention la valeur des stacks et des mises :
    - la blinde est l'unité de comptage, et Lorsque la blind augmente, la valeur par unité de blind des joueurs diminue.

Initialisation de la partie : `class Poker_game()`

paramètres qui doivent être initialisés pour une partie:
- joueurs : set of `id` (str) : `players = {j_1, j_2, ...}`
- blind initiale : variable `b > 0`
- stacks initiaux : dictionnaire `Stacks : { j_i : stack }`
- règle d'évolution de la blind, tuple (frequence, multiplicateur) : on multiplie la blind tout les x tours de table : 
`blind_rule = ( number_of_turn, multiplicative_factor)`


class `croupier(Poker_game)` : (?)
- gère la distirbution des cartes (?)

Initialisation : `class Table(Poker_game)`

- Créer un ordre aléatoire et fixe dans les joueurs : `table_order = [j_i, ..., j_n]`
- initialise le joueur dealer : ``dealer_id : str ``
- initialise `number_of_round : int = 0`
- initialise un croupier (classe croupier) (?)

Mise à jour de la table entre chaque round :
- met à jour la position du dealer :
    - dealer_id becomes the next value in `table_order`
    - if Stacks[dealer_id] == 0 : 
        on skip ce tour de dealer
- on indente `number_of_round`
- on vérifie si la blind doit être augmenté :
    - freq = blind_rule[0]
    - multiplicative_factor = blind_rule[1]
    - number_of_augmentation =  number_of_round % freq
    - facteur_total = number_of_augmentation * multiplicative_factor
    - divides all stacks by facteur total


`class round(Table)` :

- initialiser `pot : float` à 0
- initialiser `minimal_bid : float` à 0

- initialise la liste des joueurs actifs dans le round (ceux avec un stack non nul) en gardant l'ordre des joueurs :   

`J_round = [joueurs for joueurs in table_order if Stack[joueurs] > 0]`

- dictionnaire : `Round = {joueurs : {état : str , mise_actuelle : float , cartes : tuple} }`

- on suit les différentes étapes du jeux : `Step = [Preflop, Flop, Turn, River]`

- desctiption de la variable `état` du dict `Round` : 
    - `état` is in `{"wait", "in", "fold"}`
    - durant chaque phase la parole va passer indéfiniment de joueurs en joeurs juesqu'à qu'une condition d'arrêt soit rencontré
    - au début tout le monde est en "`wait`" car personne n'a parlé
    - lorsqu'une personne parle, son état passe soit en `"in"` (si `action_joueurs = check or call`), soit en `"fold"`
    - si quelqu'un `"raise"`, alors tout les joueurs qui ne sont pas `"fold"` passe en `"wait"`
    - si une personne est en `fold`, on ne lui propose plus jamais de parlé lors du round
    - si une personne est `wait`, à son tour de parole, on lui demande de parler
    - si une personne est `in` :
        - on termine la phase actuelle (flop etc)
    - use `dealer_id` to retrieve a `dealer_pos_round` 
    <!-- - si la mise minimale = mise du joueur, on termine la phase du round (preflop, flop etc..)
    - si la mise minimale > mise du joueur (cela veut dire qu'il y a eu un raise), on propose au joueur de parler à nouveau -->


- Preflop :

    - croupier distribue les cartes aux joueurs : mise à jour des variables `cartes_actuelles` du dict `Round`
    - `cartes : tuple = (numéro: int, couleur: int)`
    - on utilise `dealer_id` pour créer `dealer_pos` (position relative aux joueurs dans le round)
    - petite blind/ grosse blind mise auto :
        - `id_petite  = dealer_id` et `id _grosse = J_round[dealer_pos + 1]`
        - stack du joueur petite blinde diminue de 0.5 blind
        - stack du joueur grosse blind diminue de 1 blind
        - mise à jour de `Round` pour augmenter `mise_actuelle` à 1.5
        - `pot = 1.5`
    - ``minimal_bid = 1 ``
    - for j > `dealer_pos` + 2 :
        - if l'état du joueur j est `fold`, pass
        - if `etat` joueur j est `wait`, mise possible entre minimale actuelle- mise_joueur_j ou fold
        - if action = fold : 
            - état joueur j devient fold
            - check s'il reste plus d'un joueurs actif, sinon on lui ajoute le pot à son stack et on termine le round
        - if action = call : mise à jour de la mise actuelle joueur j, pot += mise joueur j, etc
        - if action = raise : pareil + mise à jour mise minimale to raise value


- Flop :
    - croupier deal 3 cartes visibles par tt le monde
    - On remet les joueurs qui n'ont pas fold en `état=wait` :
        Round[players[état]] = wait if Round[players[état]] not fold
        Round[players[mise actuelle]] = 0
        mise minimale = 0
    - for j >  `Dealer_pos` :
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
        - si il y a plus d'un joueurs actifs, alors ils révèlent leurs cartes et le croupier donne un gagnant