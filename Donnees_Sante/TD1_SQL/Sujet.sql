

-- Q1 Afficher la table séjour 

SELECT * FROM sejour;

-- Q2 Sélectionner les patients de la ville 1

SELECT * FROM patient
	WHERE id_ville=1;

-- Q3 Afficher les patients nés après le 31/03/1986

SELECT * FROM patient
	WHERE date_naissance>1986-03-31;

-- Q4 Afficher les séjours commencés après le 01/02/2020 dans l’hôpital 1

SELECT * FROM sejour
	WHERE id_hopital=1 AND date_debut_sejour>2020-02-01

-- Q5 Afficher les séjours des hôpitaux 1 et 3

SELECT * FROM sejour
	WHERE id_hopital IN (1,3);

-- Q6 Compter le nombre de patient par ville

SELECT id_ville, count(*) FROM patient
	GROUP BY id_ville;

-- Q7 Compter le nombre de séjours par hopital

SELECT id_hopital, count(*) FROM sejour
	GROUP BY id_hopital;

-- Q8 Modifier la requête précédente pour n'afficher que l'id_patient et le nom de la ville

SELECT id_patient, ville FROM patient
	INNER JOIN ville;

-- Q9 Afficher, pour chaque séjour, les hôpitaux dans lesquels ils ont eu lieu

SELECT id_sejour, hopital FROM sejour AS s
	JOIN hopital AS h ON h.id_hopital=s.id_hopital;

-- Q10 Compter le nombre de patients par ville en affichant le NOM de la ville

SELECT ville, count(*) FROM patient AS p
	JOIN ville AS v ON v.id_ville=p.id_ville
	GROUP BY ville;

-- Q11 Compter le nombre de séjours par hôpital en affichant le NOM de l'hôpital

SELECT hopital, count(*) FROM sejour AS s
	JOIN hopital AS h ON h.id_hopital=s.id_hopital
	GROUP BY hopital;

-- Q12 Compter le nombre de patients femme par ville en affichant le nom de la ville

SELECT ville, count(*) FROM patient AS p
	JOIN ville AS v ON v.id_ville=p.id_ville 
	WHERE sexe="F"
	GROUP BY ville;

-- Q13 Compter le nombre de séjours commençés après le 01/02/2020 pour chaque hôpital en affichant le nom de l'hôpital

SELECT hopital, count(*) FROM sejour AS s
	JOIN hopital AS h ON h.id_hopital=s.id_hopital
	WHERE s.date_debut_sejour>2020-02-01
	GROUP BY hopital;

------------------------------------------------------------------ 
-- Exécuter la requête et **interpréter** le résultat :

INSERT INTO ville
(id_ville, ville)
VALUES(6, 'Béthune');

-- Q13 Insérer Loos dans la table ville

INSERT INTO ville
	(id_ville, ville) VALUES(7, 'Loos');

------------------------------------------------------------------ 
-- Exécuter la requête et **interpréter** le résultat :

UPDATE ville SET ville = 'Lens' WHERE id_ville = 6;

-- Q14 Remplacer le libellé de la ville numéro 7 par Douai

UPDATE ville SET ville = 'Douai' WHERE id_ville = 7;

------------------------------------------------------------------ 
-- Exécuter la requête et **interpréter** le résultat :

DELETE FROM ville WHERE id_ville = 6;

-- Q15 supprimer la ville numéro 7

DELETE FROM ville WHERE id_ville = 7;
