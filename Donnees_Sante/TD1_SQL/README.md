# sql_td1

### Septembre 2022

### Objectifs
- Savoir se connecter à un DBMS
- Exécuter des requêtes SQL dans un script (sélectionner, modifier, supprimer des données dans une table, etc)
- Distinguer les opérations du DDL avec celles du DML
- Mettre les variables au bon format (numéric, charactère, date, etc)
- Fusionner 2 tables avec des requêtes JOIN

### Données

Fichier *sejour.zip* :
- Création de la base (DDL)
- Insertion des données :
    - ville: un identifiant par ville
    - patient: un identifiant par patient + date de naissance + id de la ville
    - hopital: un identifiant par hopital (lieu du séjour)
    - séjour: un identifiant par séjour + identifiant du patient + date début + date de fin + identifiant du lieu (hopital)


### Notes

- Date au format aaaa-mm-dd
- Sélectionner la connexion dans DBeaver
- les requêtes se terminent par un ';' 
- utiliser un ' pour encadrer des chaînes de caractères ou des dates 
- group by / select

## Connexion

host : ilis-omop.univ-lille.fr
port : 5432
nom d'utilisateur : login ilis
mot de passe : mot de passe ilis

1 - DBeaver

2 - PgAdmin
https://ilis-omop.univ-lille.fr/phppgadmin/

## Requêtes - DML


## Exercices

### 1- Select

- Exécuter les requêtes et **interpréter** les 3 résultats :

> __________
> select * from patient ;
> ____
> select id_patient, sexe 
> from patient ;
> _____
> select count(*) from patient ;
> _____

- **Q1 : Afficher la table séjour**

- Exécuter les requêtes et **interpréter** les 2 résultats :

> __________
> select *
> from patient 
> where sexe = 'M';
> ____
> select *
> from patient
> where date_naissance > '1960-01-01';
> _____

- **Q2 : Sélectionner les patients de la ville 1**

- **Q3 : Afficher les patients nés après le 31/03/1986**

- Exécuter les requêtes et **interpréter** le résultat :

> __________
> select *
> from patient 
> where date_naissance > '1960-01-01'
> and sexe = 'F';
> ____

- **Q4 : Afficher les séjours commencés après le 01/02/2020 dans l'hôpital 1**

- Exécuter les requêtes et **interpréter** le résultat :

> __________
> select *
> from patient 
> where id_ville in (1, 2) ;
> ____

- **Q5 : Afficher les séjours des hôpitaux 1 et 3**

- Exécuter les requêtes et **interpréter** le résultat :

> __________
> select sexe, count(*)
> from patient 
> group by sexe ;
> ____

- **Q6 : Compter le nombre de patients par ville**

- **Q7 : Compter le nombre de séjours par hôpital**


- Exécuter les requêtes et **interpréter** le résultat :

> __________
> select *
> from patient p inner join ville v 
> on p.id_patient = v.id_ville ;
> ____

- **Q8 : Modifier la requête précédente pour n'afficher que l'id_patient et le nom de la ville**

- **Q9 : Afficher, pour chaque séjour, les hôptiaux dans lesquels ils ont eu lieu**

- **Q10 : Compter le nombre de patients par ville en affichant le NOM de la ville**

- **Q11 : Compter le nombre de séjours par hôpital en affichant le NOM de l'hôpital**

- **Q12 : Compter le nombre de patients femme par ville en affichant le nom de la ville**

- **Q13 : Compter le nombre de séjours commençés après le 01/02/2020 pour chaque hôpital en affichant le nom de l'hôpital**

### 2- Insert


- Exécuter les requêtes et **interpréter** le résultat :

> __________
> insert into ville (id_ville, ville)
> values(6, 'Béthune') ;
> ____

- **Q14 : Insérer Loos dans la table ville**

### 3- Update

- Exécuter les requêtes et **interpréter** le résultat :

> __________
> update ville set ville = 'Lens' 
> where id_ville = 6 ;
> ____

- **Q15 : Remplacer le libellé de la ville numéro 7 par Douai**


### 4- Delete

- Exécuter les requêtes et **interpréter** le résultat :

> __________
> delete from ville 
> where id_ville = 6 ;
> ____

- **Q16 : supprimer la ville numéro 7**


## Create table
