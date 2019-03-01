Dematik
=======

Dematik simplifie la dématérialisation des processus.

La solution permet de générer des formulaires en partant:
- de fichiers yaml pour les libellés
- de simples fichiers texte pour la définition des formulaires

Points forts :
- L'emploi de simples fichiers texte accélère la mise au point de formulaires (copier/coller, ...).
- La relecture des libellés ou encore la définition d'un formulaire devient un jeu d'enfant 
- L'approche par bloc pré-packagé permet une homogénéité des formulaires
- L'écriture des conditions est simplifiée. Les conditions sont écrites en français et traduites automatiquement en python.
- Tout est en français (message d'erreur, définition du formulaire, conditions, ...)

Points faibles :
 - L'écriture d'une condition dont la typologie n'a pas été prévue nécessite le recours à des développements
 - L'utilisation de types de champs non prévus nécessite le recours à des développements

Pré-requis
----------

Dematik nécessite python version 2.7 et pip

Installation
------------

```bash
git clone https://github.com/departement-loire-atlantique/dematik
cd dematik
pip install .
```

Utilisation
-----------

Génération de tous les processus modifiés :
```bash
python -m dematik
```

Génération de tous les processus :
```bash
python -m dematik --force
```

Génération d'un seul processus (ici process/definition/aide_habitat/pa.def) :
```bash
python -m dematik --pattern aide_habitat/pa.def
```

Génération d'un seul processus (ici process/definition/aide_habitat/pa.def) en mode mise au point :
```bash
python -m dematik --pattern aide_habitat/pa.def --debug
```

Développement
-------------

```bash
git clone https://github.com/departement-loire-atlantique/dematik
cd dematik
pip install -e .
```

Validation du programme (éxécution des tests unitaires)
```bash
python -m unittest discover
```

Documentation
-------------

Les contenus textuels des champs sont stockés dans un fichier .yaml stocké dans le dossier process/labels

Exemple :

```yaml

identifiant: texte sur une ligne

liste:
  Titre de la liste:
    - Elément 1
    - Elément 2

identifiant2: >
  texte sur 
  plusieurs lignes


  laisser deux lignes vides pour démarrer un nouveau paragraphe

texte_enrichi: >
  Titres :
  
  # ceci est un titre 1
  ## ceci est un titre 2
  ### ceci est un titre 3
  #### ceci est un titre 3

  Ceci est en  **gras** (mettre ** avant et après le mot en gras)
  Ceci est en *italique* (mettre * avant et après le mot en italique)

  Pour faire une liste, précéder la phrase de - :
  - élément 1
  - élément 2
```

Les définitions de formulaires sont stockés dans des fichiers .def stockés dans le dossier process/definition

Exemple :
```
formulaire "nom du formulaire" 

    url "url-du-formulaire" 
    description "description du formulaire"
    identifiant "identifiant-du-formulaire"

    workflow "nom du workflow"
    Le paramètre "nom_paramètre" du workflow vaut "valeur"
    Le paramètre "nom_paramètre2" du workflow vaut "valeur2"


    listing ce_champ_sera_affiche_en_colonne_dans_les_listes
    listing ce_champ_sera_affiche_en_colonne_dans_les_listes

    filter ce_champ_permettra_de_filtrer
    filter ce_champ_permettra_de_filtrer

page nom_page

    liste* ma_liste_obligatoire

    texte mon_texte

    champ_texte beneficiaire:nom

page nom_page_2
    
    titre titre_nom_page_2

    champ_texte mandant:nom

```

Le nom d'un libellé peut être utilisé simplement ou précédé d'un espace de nommage.

Exemple :

mandant:nom => Espace de nommage = mandant, libellé = nom

Les espaces de nommages permettent d'utiliser le même libellé plusieurs fois sans pour autant créer d'ambiguité lors de leur utilisateur dans une condition.


Pour ajouter un pré-remplissage d'un champ basé sur le profil de l'utilisateur, utiliser la syntaxe suivante :

> si **condition** alors préremplir **code_cham** avec **profil:civilite**

ou 

> préremplir **code_cham** avec **profil:civilite**

Liste des codes pour les valeurs dépendant du profil :
- profil:civilite : Civilité
- profil:nom : Nom
- profil:prenom : Prénom
- profil:adresse : Adresse (rue et numéro)
- profil:code_postal : Adresse (code postal)
- profil:commune : Adresse (commune)
- profil:courriel : Courriel
- profil:telephone_mobile : Téléphone mobile
- profil:telephone_fixe : Téléphone fixe


ROADMAP
-------

- Support des conditions dans les définitions
- Validation et d'autocomplétion pour les fichiers de définition (éditeur)
- Mise à jour automatique dans une instance publik
