
------------------------------------------------------------------ 
-- select
------------------------------------------------------------------ 

select * from patient;

select id_patient, sexe from patient;

select count(*) from patient;

-- Q1 Afficher la table séjour 



-- where
------------------------------------------------------------------ 

select *
from patient 
where sexe = 'M';

select *
from patient
where date_naissance > '1960-01-01';

-- Q2 Sélectionner les patients de la ville 1


-- Q3 Afficher les patients nés après le 31/03/1986


-- AND
------------------------------------------------------------------ 

select *
from patient
where date_naissance > '1960-01-01'
and sexe = 'F';

-- Q4 Afficher les séjours commencés après le 01/02/2020 dans l’hôpital 1


-- IN
------------------------------------------------------------------ 

select * 
from patient
where id_ville in (1, 2);

-- Q5 Afficher les séjours des hôpitaux 1 et 3


-- GROUP BY
------------------------------------------------------------------ 

select sexe, count(*)
from patient
group by sexe;

-- Q6 Compter le nombre de patient par ville


-- Q7 Compter le nombre de séjours par hopital


-- INNER JOIN
------------------------------------------------------------------ 

select *
from patient p inner join ville v 
on p.id_ville = v.id_patient;

-- Q8 Modifier la requête précédente pour n'afficher que l'id_patient et le nom de la ville


-- Q9 Afficher, pour chaque séjour, les hôptiaux dans lesquels ils ont eu lieu


-- Q10 Compter le nombre de patients par ville en affichant le NOM de la ville


-- Q11 Compter le nombre de séjours par hôpital en affichant le NOM de l'hôpital


-- Q12 Compter le nombre de patients femme par ville en affichant le nom de la ville


-- Q13 Compter le nombre de séjours commençés après le 01/02/2020 pour chaque hôpital en affichant le nom de l'hôpital



-- insert
------------------------------------------------------------------ 

-- Exécuter la requête et **interpréter** le résultat :

INSERT INTO ville
(id_ville, ville)
VALUES(6, 'Béthune');

-- Q13 Insérer Loos dans la table ville


-- update
------------------------------------------------------------------ 

-- Exécuter la requête et **interpréter** le résultat :

update ville set ville = 'Lens' where id_ville = 6;

-- Q14 Remplacer le libellé de la ville numéro 7 par Douai



-- delete
------------------------------------------------------------------ 

-- Exécuter la requête et **interpréter** le résultat :

delete from ville where id_ville = 6;

-- Q15 supprimer la ville numéro 7


