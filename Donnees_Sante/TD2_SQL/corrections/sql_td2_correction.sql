

-- ville

DROP TABLE IF EXISTS ville;

CREATE TABLE ville (
	id_ville 		int NOT NULL,
	ville 			varchar(50) NULL,
	CONSTRAINT pk_ville PRIMARY KEY (id_ville)
);

-- patient

DROP TABLE IF EXISTS patient;

CREATE TABLE patient (
	id_patient 		int NOT NULL,
	date_naissance	date NULL,
	sexe			char(1) null,
	id_ville		integer not null,
	CONSTRAINT pk_patient PRIMARY KEY (id_patient),
	constraint fk_patient_ville foreign key (id_ville) references ville (id_ville)
); 

-- hopital

DROP TABLE IF EXISTS hopital;

CREATE TABLE hopital (
	id_hopital 			int NOT NULL,
	hopital 			varchar(50) NULL,
	CONSTRAINT pk_hopital PRIMARY KEY (id_hopital)
);

-- sejour

DROP TABLE IF EXISTS sejour;

CREATE TABLE sejour (
	id_sejour 		int NOT NULL,
	id_patient		int not NULL,
	date_debut_sejour 	date not null,
	date_fin_sejour		date not null,
	id_hopital			int not null,
	CONSTRAINT pk_sejour PRIMARY KEY (id_sejour),
	constraint fk_sejour_patient foreign key (id_sejour) references sejour (id_sejour),
	constraint fk_sejour_hopital foreign key (id_hopital) references hopital (id_hopital)
);

-- unite
-- Créer une table unité avec les colonnes suivantes :
-- id_unite
-- code_unite
-- nom_unite
-- date_debut_validite
-- date_fin_validite
-- Créer les contraintes nécessaires (clé primaire, clé étrangère) 

DROP TABLE IF EXISTS unite;

CREATE TABLE unite (
	id_unite 			int NOT NULL,
	code_unite			char(4) not null
	nom_unite 			varchar(50) not NULL,
	date_debut_validite	date not null,
	date_fin_validite	date not null,
	CONSTRAINT pk_unite PRIMARY KEY (id_unite)
);

-- rum
-- Créer une table RUM avec les colonnes suivantes :
-- id_rum 
-- id_sejour
-- date_entree
-- date_sortie
-- mode_entree
-- mode_sortie
-- Créer les contraintes nécessaires (clé primaire, clé étrangère) 

DROP TABLE IF EXISTS rum;

CREATE TABLE rum (
	id_rum 			int NOT NULL,
	id_sejour		int not null,
	date_entree     date not NULL,
	date_sortie		date not null,
	mode_admission		char(2),
	mode_sortie		char(2),
	CONSTRAINT pk_rum PRIMARY KEY (id_rum),
	constraint fk_rum_sejour foreign key (id_sejour) references sejour (id_sejour)
);

-- acte
-- Créer une table acte avec les colonnes suivantes :
-- id_acte 
-- code_acte
-- libelle_acte
-- date_debut_validite
-- date_fin_validite

DROP TABLE IF EXISTS acte;

CREATE TABLE acte (
	id_acte 			int NOT NULL,
	code_acte			char(7) not null,
	libelle_acte 			varchar(50) not NULL,
	date_debut_validite	date not null,
	date_fin_validite	date not null,
	CONSTRAINT pk_acte PRIMARY KEY (id_acte)
);

-- acte
-- Créer une table rum_acte avec les colonnes suivantes :
-- id_acte 
-- id_rum
-- date_acte

DROP TABLE IF EXISTS rum_acte;

CREATE TABLE rum_acte (
	id_acte 			int NOT NULL,
	id_rum				int not null,
	date_acte 			date not null,
	CONSTRAINT pk_rum_acte PRIMARY KEY (id_acte, id_rum, date_acte),
	constraint fk_rum_acte_rum foreign key (id_rum) references rum (id_rum),
	constraint fk_rum_acte_acte foreign key (id_acte) references acte (id_acte)
);

-- diagnostic

DROP TABLE IF EXISTS diagnostic;

CREATE TABLE diagnostic (
	id_diagnostic			int NOT NULL,
	code_diagnostic			char(4) not null,
	libelle_diagnostic 		varchar(50) not NULL,
	date_debut_validite	date not null,
	date_fin_validite	date not null,
	CONSTRAINT pk_diagnostic PRIMARY KEY (id_diagnostic)
);

-- Rum Diagnostic
DROP TABLE IF EXISTS rum_diagnostic;

CREATE TABLE rum_diagnostic (
	id_diagnostic 			int NOT NULL,
	id_rum				int not null,
	date_diagnostic 			date not null,
	CONSTRAINT pk_rum_diagnostic PRIMARY KEY (id_diagnostic, id_rum, date_diagnostic),
	constraint fk_rum_diagnostic_rum foreign key (id_rum) references rum (id_rum),
	constraint fk_rum_diagnostic_diagnostic foreign key (id_diagnostic) references diagnostic (id_diagnostic)
);


-- Suppression des tables

DROP TABLE IF EXISTS rum_acte;
DROP TABLE IF EXISTS acte;
DROP TABLE IF EXISTS rum_diagnostic;
DROP TABLE IF EXISTS diagnostic;
DROP TABLE IF EXISTS rum;
DROP TABLE IF EXISTS unite;

-- Insertion d'enregistrements

------------------- rum --------------------------

insert into rum (id_rum, id_sejour, date_entree, date_sortie, mode_admission, mode_sortie)
values
(1, 1, '2020-01-01', '2020-01-05', '5', '5'),
(2, 1, '2020-01-05', '2020-01-10', '5', '8'),
(3, 2, '2020-01-01', '2020-01-02', '8','8'),
(4, 2, '2020-01-02', '2020-01-04', '8','8'),
(5, 2, '2020-01-04', '2020-01-12', '8','8');

----------------- rum acte -----------------------

INSERT INTO rum_acte (id_rum, id_acte, date_acte)
 VALUES
 (1, 1, '2020-01-01'),
 (2, 1, '2020-01-05'),
 (3, 2, '2020-01-01'),
 (4, 3, '2020-01-04'),
 (5, 2, '2020-01-10');

------------------ rum diagnostic -------------------

INSERT INTO rum_diagnostic (id_rum, id_diagnostic, date_diagnostic)
 VALUES
 (1, 1, '2020-01-01'),
 (2, 1, '2020-01-05'),
 (3, 1, '2020-01-01'),
 (4, 4, '2020-01-02'),
 (4, 5, '2020-01-04');



