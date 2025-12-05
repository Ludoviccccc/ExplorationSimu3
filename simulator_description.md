## Objectif de la note

Cette note donne quelques éléments d'information et de justification concernant le simulateur utilisé dans les travaux de recherche automatique d'interférences. 

Elle décrit brièvement
- le comportement de certains composants liés à la gestion mémoire (caches, DDR, contrôleur DDR, interconnect), 

## Etat du simulateur et proposition d'améliorations
### Modélisation des cœurs (class "core")
#### Etat du simulateur

La simulation des cœurs est limitée à la prise en compte des instructions effectuant des accès mémoire (load et store).  En d'autres termes, le jeu d'instructions est réduit à des opérations de lecture ("read") et d'écriture ("write") en mémoire puisque, en définitive, seuls les accès mémoire sont simulés.

Pour chaque coeur, une simple boucle modélise le cycle "fetch et execute".

À chaque itération de la boucle (donc, chaque cycle processeur), le coeur peut
- attendre la fin d'une opération de lecture  ;
- exécuter un "read" (load) ;
- exécuter un "write" (store).
- exécuter une instruction n'effectuant pas d'accès mémoire, ce qui, dans le cas du simulateur, revient à ne rien faire ;

Le choix entre les trois types d'opération (tout instruction n'effectuant pas d'accès mémoire, un LD ou un ST) est choisi aléatoirement. 

Ce modèle est évidemment très simplifié:
- L'attente de l'achèvement d'un accès mémoire en lecture pour poursuivre l'exécution du code ne correspond pas à la réalité car le processeur dispose de divers mécanismes permettant justement de masquer ces latences. Cette attente n'est nécessaire que pour préserver les vraies dépendances enter accès (par ex. une séquence LD @a, WR @a doit être préservée lors de l'exécution pour maintenir la sémantique du programme).
#### Améliorations possibles

*A minima*, le simulateur pourrait être amélioré en vérifiant, à chaque cycle, si l'exécution d'une instruction est compatible des opérations mémoire en cours de réalisation. Ceci permettrait notamment de simuler le parallélisme d'exécution des requêtes en lecture.
### Modèle des caches

#### Etat simulateur

- Chaque niveau de cache (classe "ClassLevel") est configurable en taille totale, taille d'une ligne de cache et associativité. 
- Par défaut le comportement est de type "write_back", c'est à dire que l'écriture dans la mémoire de niveau inférieur a lieu lors de l'éviction de la ligne de cache. Lors de l'opération d'écriture, la ligne est simplement marquée "dirty" et lors de l'éviction de la ligne, celle-ci est écrite dans la mémoire de niveau inférieur .
- Il est aussi est possible de mettre en oeuvre un comportement de type "write-through" dans lequel l'écriture dans la mémoire de niveau inférieur a lieu immédiatement.
- La gestion de l'éviction des lignes de cache est réalisée par un PLRU (classe PLRU) dont le rôle est de déterminer la ligne à remplacer en fonction de l'état courant du cache. Idéalement, on souhaiterait mettre en oeuvre un comportement de type LRU (Least Recently Used), qui consisterait à éliminer la ligne utilisée le moins récemment afin d'exploiter au mieux le principe de localité. Cependant, cette stratégie est coûteuse à mettre en oeuvre et on préfère souvent utiliser un mécanisme plus simple appelé Pseudo-LRU qui repose sur un arbre binaire.
- Cet algorithme comporte :
	- une fonction permettant de maintenir la structure de données (arbre binaire) qui permettra de choisir le prochaine ligne à évincer en fonction des accès mémoire ("update_on-access")
	- une fonction permettant de choisir la prochaine ligne de cache à évincer ("get_victim") à partir de l'information contenue dans l'arbre binaire.
-  Le cache de dernier niveau (L2 dans le code actuel) est partagé par les deux hiérarchies mémoire. 
- Il n'y a pas de mécanisme de gestion de la cohérence de cache.

### Modèle de la DDR   (class DDRMemory)
#### Etat actuel

- La mémoire est constituée de plusieurs banques ("banks") dont chacune dispose d'un "row buffer" (une forme de cache). 
- L'état des banques de la DDR détermine les dates de complétion des opérations. Les requêtes  sont émises par le contrôleur DDR.

Les points les plus importants sont rappelés dans la liste ci-dessous : 
- La mémoire est décomposée en blocs appelé "banques" (banks) qui peuvent être accédées de manière simultanées. 
- Chaque banque est associée à un "row buffer" qui joue le rôle de cache pour une ligne mémoire (row). Lors d'un changement de ligne, le "row buffer" doit être rechargé. 
	- Les données concernant l'organisation mémoire (le passage d'une adresse physique aux "adresses " des éléments micro-architecturaux) ne sont pas toujours disponibles et doivent être parfois obtenues par rétro-engineering en exploitant notamment les latences observées. 
	- Par exemple, pour le SITARA AM5278, une adresse physique est décodée ainsi :
	   `RowSize | RankSize | BanksSize | ColumnSize | BusSize`
	-  Il est parfois possible d'obtenir des informations à partir de compteurs de performance.
- Concernant les latences, on peut retenir les points suivants :
	- l'accès à différentes lignes de la même banque conduit à d'importants délais en raison du coût de changement de ligne (*row miss*)
	- les accès simultanés à une ligne ouverte d'une banque donnée (i*ntra-bank interference*) entraînent plus de délais que l'accès simultané à différentes banques (*inter-bank interference*).
- La DDR me en oeuvre les commandes suivantes
	- Write (**WR**)
	- Read (**RD**) 
	- Active (**ACT**) pour activer une ligne fermée (closed row) ; cette opération chaque le buffer de ligne avec une nouvelle ligne. Elle dure tRCD
	- Precharge (**PRE**) pour désactiver une ligne ouverte pour une banque donnée ; cette opération écrit les information du buffer de ligne (row buffer) courant vers la mémoire. Elle dure tRP.
	- Refresh (**REF**). Cette opération a pour objectif de rafraichir les cellules mémoire. 
- Les acccès mémoire se font en burst de longueur BL x 8 bytes. Etant donnée que la mémoire est de type Double Rate (DDR : elle fournit des données sur les fronts montants et descendants de l'horloge), la durée d'un burst est BL/2. Les données du burst n'arrivent pas instantanément, mais après une latence CAS Latency (CL) pour une lecture (RD) et une latence CAS Write Latency (CL) pour une écriture (WR).
- À chaque changement de ligne pour une banque, une opération PRE de durée tRP et ACT de durée tRCD sont réalisées. 
- Périodiquement, une opération de rafraichissement mémoire (REF) doit avoir lieu. La période est tRFC. Lors de cette opération, tous les row buffers des banques mémoire doivent être préchargés  


- La durée minimale entre deux RDs ou Wrs est de tCCD (normalement égal à BL/2)
- Lors d'une transition RD => WR, 2 cycles
- Lors d'une transition WR => RD, pénalité de tWTR


- Autres contraintes 
	- ACT => ACT inter-bank  : Le délai entre deux  ACT consécutifs ne doit pas dépasser tRRD
	- ACT => PRE  :  pour une séquence intra-bank, le dt entre ACT et PRE ne doit pas excéder tRAS
	- ACT => ACT intra-bank : Le délai entre deux ACT vers la même bank bne doit pas dépasser tRC
	- RD/WR => PRE
		- Le délai entre RD et PRE doit être au minimum de tRTP
		- Le délai entre WR et PRE doit être au minimum de tWR
	- Il faut émettre 8 REF dans une fenêtre de taille 8xtREFI



#### Possibilités d'amélioration

- Vérification du respect des contraintes temporelles (une seule vérification est réalisée dans le contrôleur)
- Traitement des *bursts* qui ont un impact majeur sur les latences. 

### Modèle du contrôleur mémoire
#### Etat actuel
- (Le modèle de la DDR et celui du contrôleur mémoire sont couplés.)
- À chaque cycle :
	- le contrôleur détermine les requêtes dont le traitement est achevé (c-à-d la date courant est supérieure à la date de complétion prévue). Dans ce cas, et pour une requête de type "read",  il appelle un "callback" qui signale au coeur que l'accès est achevé? C'est ce callback qui est utilisé par le coeur pour débloquer l'exécution d'une nouvelle instruction. Aucun callback n'est prévu dans le cas d'une requête en écriture. 
	- le contrôleur traite les requêtes situées dans sa file d'entrée. Pour chaque requête, il détermine si celle-ci peut être traitée par la DDR selon son état (géré par la machine à état de la DDR) en assurant les contraintes de délais minimum (cf [1]). Puis il détermine la "meilleure" requête à traiter en fonction d'un classement établi pour privilégier les requêtes aboutissant à un "row hit", les requêtes WR sur les requêtes RD et l'ordre d'arrivée (FIFO). Enfin, il transmet la "meilleure" requête à la DDR. 
-  Le modèle reprend les "grandes lignes" des mécanismes généraux décris dans [1].

- Le contrôleur mémoire est en charge de réordonner les requêtes d'accès mémoire pour maximiser le débit d'accès mémoire. 
- Il met en œuvre plusieurs files d'attentes : une file pour les commandes, une file pour les données en lecture, une file pour les données en écriture
- Certains chip mettent en oeuvre plusieurs contrôleurs.
- Règles de priorisation
	- Prioriser les RD sur les WR de façon à minimiser les temps d'attente, mais en préservant la cohérence mémoire (WR @x RD @x doit être exécuté dans cet ordre)
	- Prioriser les lignes qui sont déjà dans les row_buffer afin d'éviter la pénalité liée à la réalisation d'une séquence PRE=>ACT.
	- Traitement des RD et WR en "batch" de façon à éviter l'overhead lié à la transition entre RD et WR
- Il existe aussi des mécanismes permettant de prévenir les problèmes de famine. 

##### Possibilités d'amélioration du simulateur
- S'assurer de la cohérence des délais. Pas d'amélioration significative nécessaire. 
#### Modèle de l'Interconnect
##### Etat actuel
- Le modèle de l'interconnect est trivial. Il consiste à maintenir une file d'attente (FIFO) des requêtes mémoire et à exécuter les requêtes dans l'ordre d'arrivée après un délai correspondant à la une latence d'accès minimale. À noter que l'on rajoute un délai aléatoire de 2 cycles max.
- À chaque cycle d'horloge (fonction "tick"), on dépile un certain nombre de requêtes parmi celles pouvant être exécuté au cycle courant que l'on transmet à la mémoire.  Le nombre de requêtes dépilé à chaque cycle est déterminé par la bande passante du bus (test "processed < self.bandwidth") et comptage du nombre de requête traitées (ligne 141).
- Les requêtes qui n'ont pas pu être traitées sont mises dans la file d'attente des requêtes à exécuter aux cycles suivants
- Il est important de noter que, tel que le code d'appel à l'horloge est réalisé, la fréquence d'horloge de l'interconnect et des "cœurs" sont les mêmes. On pourrait introduire des horloges de périodes différentes en appelant les fonction "clock" sur des cycles différents.  


##### Possibilités d'amélioration du simulateur
- Prise en compte du trafic lié aux activités de *snooping*?
- Prise en compte des mécanismes d'évitement de la famine?
- Prise en compte des différences de fréquence entre les CPU, DDR et corenet?
