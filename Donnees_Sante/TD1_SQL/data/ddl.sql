

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



