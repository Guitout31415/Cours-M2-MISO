
------------------------------------------------------------------ 
-- select
------------------------------------------------------------------ 

select * from patient;

select id_patient, sexe from patient;

select count(*) from patient;

-- Q1 Afficher la table séjour 

select * from sejour;

-- where
------------------------------------------------------------------ 

select *
from patient 
where sexe = 'M';

select *
from patient
where date_naissance > '1960-01-01';

-- Q2 selectionner les patients de la ville 1

select *
from patient 
where id_ville = 1;

-- Q3 afficher les patients nés après le 31/03/1986

select *
from patient
where date_naissance > '1986-03-31';

-- AND
------------------------------------------------------------------ 

select *
from patient
where date_naissance > '1960-01-01'
and sexe = 'F';

-- Q4 afficher les séjours commencer après le 01/02/2020 dans l'hopital 1

select *
from sejour
where date_debut_sejour > '2020-02-01'
and id_hopital = 1;


-- IN
------------------------------------------------------------------ 

select * 
from patient
where id_ville in (1, 2);

-- Q5 afficher les séjours des hôpitaux 1 et 3

select * 
from sejour
where id_hopital in (1, 3);

-- GROUP BY
------------------------------------------------------------------ 

select sexe, count(*)
from patient
group by sexe;

-- Q6 Compter le nombre de patient par ville

select id_ville, count(*)
from patient
group by id_ville;

-- Q7 Compter le nombre de séjours par hopital

select id_hopital, count(*)
from sejour
group by id_hopital;

-- INNER JOIN
------------------------------------------------------------------ 

select *
from patient p inner join ville v 
on p.id_ville = v.id_ville;

-- Q8 Modifier la requête précédente pour n'afficher que l'id_patient et la ville
 
select id_patient, ville
from patient p inner join ville v 
on p.id_ville = v.id_ville;

-- Q9 Afficher les séjours et les hôptiaux dans lesquels ils ont lieu

select *
from sejour s inner join hopital h
on s.id_hopital = h.id_hopital;

-- Q10 Compter le nombre de patients par ville en affichant le nom de la ville

select v.ville, count(*)
from patient p inner join ville v 
on p.id_ville = v.id_ville
group by v.ville 
order by count(*) desc;

-- Q11 Compter le nombre de séjours par hopital en affichant le nom de l'hôpital

select h.hopital, count(*)
from sejour s inner join hopital h 
on s.id_hopital = h.id_hopital
group by h.hopital
order by count(*) desc;

-- Q12 Compter le nombre de patients femme
-- par ville en affichant le nom de la ville

select v.ville, count(*)
from patient p inner join ville v
on p.id_ville = v.id_ville
where p.sexe = 'F'
group by v.ville 
order by count(*) desc;

-- Q12 Compter le nombre de séjours commençant après le 01/02/2020
-- par hopital en affichant le nom de l'hôpital

select h.hopital, count(*)
from sejour s inner join hopital h 
on s.id_hopital = h.id_hopital
where date_debut_sejour > '2020-02-01'
group by h.hopital
order by count(*) desc;

-- insert
------------------------------------------------------------------ 

INSERT INTO ville
(id_ville, ville)
VALUES(6, 'Béthune');

-- Q13 Insérer Loos dans la table ville

INSERT INTO ville
(id_ville, ville)
VALUES(7, 'Loos');

-- update
------------------------------------------------------------------ 

update ville set ville = 'Lens' where id_ville = 6;

-- Q14 Remplacer le libellé de la ville numéro 7 par Douai

update ville set ville = 'Douai' where id_ville = 7;

-- delete
------------------------------------------------------------------ 

delete from ville where id_ville = 6;

-- Q15 supprimer la ville numéro 7

delete from ville where id_ville = 7;
