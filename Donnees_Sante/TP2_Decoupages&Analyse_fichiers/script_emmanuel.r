setwd("~/Documents") ;
df <- read.table(file="sejours.rsa.txt", header=FALSE,
                 sep="#") ;

# age
start <- 53 ; stop <- 55 ;
df$age <- substring(df$V1, start, stop) ;
df$age  <- as.numeric( df$age ) ;
summary(df$age) ;
hist(df$age, col="pink", freq=FALSE) ; 
lines(density(na.omit(df$age))) ;

# sexe
start <- 59 ; stop <- 59 ;
df$sexe <- substring(df$V1, start, stop) ;
df$sexe[which(df$sexe=="1")] <- "H" ;
df$sexe[which(df$sexe=="2")] <- "F" ;
table(df$sexe, useNA="always") ;
pie(table(df$sexe)) ;

# GHM : groupe homogène de malades
# GENRSA : programme qui calcule le GHM <- diags, actes...
start <- 42 ; stop <- 47 ;
df$ghm <- substring(df$V1, start, stop) ;
table(df$ghm) ;
pie(table(df$ghm)) ;

# diagnostic principal : DP
start <- 203 ; stop <- 208 ;
df$dp <- substring(df$V1, start, stop) ;
table(df$dp) ;
pie(table(df$dp)) ;

# diagnostic relié : DR
start <- 209 ; stop <- 214 ;
df$dr <- substring(df$V1, start, stop) ;
table(df$dr) ;
pie(table(df$dr)) ;
table(df$dr=="      ") ;  # six espaces pour le vide

# les zones PGV
nb_repetitions <- as.numeric(substring(df$V1, 109, 109)) ;
start <- 224 ;
length <- 2 * nb_repetitions ;
stop <- start + length - 1 ;
df$zone_pgv <- substring(df$V1, start, stop) ;
table(df$zone_pgv) ;

# les zones radiothérapie
nb_repetitions <- as.numeric(substring(df$V1, 131, 131)) ;
start <- stop + 1 ;
length <- 7 * nb_repetitions ;
stop <- start + length - 1 ;
df$zone_radioth <- substring(df$V1, start, stop) ;
table(df$zone_radioth) ;

# les zones UM (ou RUM), 60 de large
nb_repetitions <- as.numeric(substring(df$V1, 51, 52)) ;
start <- stop + 1 ;
length <- 60 * nb_repetitions ;
stop <- start + length - 1 ;
df$zone_rum <- substring(df$V1, start, stop) ;

# les zones diagnostics associés significatifs, 6 de large
nb_repetitions <- as.numeric(substring(df$V1, 215, 218)) ;
start <- stop + 1 ;
length <- 6 * nb_repetitions ;
stop <- start + length - 1 ;
df$zone_das <- substring(df$V1, start, stop) ;

# les zones d'actes, 22 de large
nb_repetitions <- as.numeric(substring(df$V1, 219, 223)) ;
start <- stop + 1 ;
length <- 22 * nb_repetitions ;
stop <- start + length - 1 ;
df$zone_act <- substring(df$V1, start, stop) ;
df$zone_act[1:20] ;

