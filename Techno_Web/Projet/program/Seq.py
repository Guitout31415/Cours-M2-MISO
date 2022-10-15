__author__ = ['LEMAIRE Guillaume', 'LUONG Tony']

class SequenceError(Exception):
    pass

class DnaSeq():
    def __init__(self, id, desc, seq):
        """
        :param id: (str) id de la séquence
        :param desc: (str) description de la séquence
        :param seq: (str) la séquence ADN
        """
        self.__id = id
        self.__description = desc
        self._seq = seq
        self.__length = len(seq)
        self._codon_table = None
        self._rev_seq = self.__reverse_complement()

    def get_id(self):
        """Donne l'id de la séquence.

        :return: (str) id du gène
        """
        return self.__id

    def get_sequence(self):
        """Donne la séquence d'ADN.

        :return: (str) séquence d'ADN
        """
        return self._seq

    def get_desc(self):
        """Donne la description de la séquence.

        :return: (str) description de la séquence
        """
        return self.__description

    def set_codon_table(self, Fi):
        """Lit un fichier Fi et construit une table de codon.

        La table de codon sera un dictionnaire où chaque clé sera un codon et
        la valeur, la traduction du codon, et 2 clés 'START' et 'STOP' ayant
        pour valeur un ensemble contenant les codons start et stop.

        :param Fi: (str) lien vers le fichier contenant le code génétique
        """
        with open(Fi, 'r') as fileIn:
            AAs = fileIn.readline().split(' ')[-1]
            Starts = fileIn.readline().split(' ')[-1]
            B1 = fileIn.readline().split(' ')[-1]
            B2 = fileIn.readline().split(' ')[-1]
            B3 = fileIn.readline().split(' ')[-1]
        self._codon_table = {"START": set(), "STOP": set()}
        for i in range(64):
            aa = AAs[i]
            st = Starts[i]
            codon = B1[i] + B2[i] + B3[i]
            if aa not in self._codon_table:
                self._codon_table[codon] = []
            self._codon_table[codon].append(aa)
            if st != "-":
                if st == "M":
                    self._codon_table["START"].add(codon)
                else:
                    self._codon_table["STOP"].add(codon)


    def computeORF(self, l):
        """Calcule tous les ORF de taille >= l dans la séquence.

        :param l: (int) longueur minimale des ORF à chercher
        :return: (list) liste des ORFs triées par position de départ croissante
        """
        self.__orfs = []
        START, STOP = self._codon_table["START"], self._codon_table["STOP"]
        # Parcours du brin +
        for i in range(0, self.__length):
            codon = self._seq[i:i+3]
            if codon in START:
                nStart = i # Sauvegarde de la position du codon start dans la séquence
                for j in range(i, self.__length, 3): # Parcours codon par codon
                    codon2 = self._seq[j:j+3]
                    if codon2 in STOP:
                        nEnd = j+3
                        if len(self._seq[nStart:nEnd]) >= l:
                            ORF = OrfSeq(self._seq, nStart, nEnd, '+', nStart%3)
                            ORF.set_codon_table(self._codon_table)
                            self.__orfs.append(ORF)
                        break
        # Parcours du brin -
        for i in range(0, self.__length):
            codon = self._rev_seq[i:i+3]
            if codon in START:
                nStart = i
                for j in range(nStart, self.__length, 3):
                    codon2 = self._rev_seq[j:j+3]
                    if codon2 in STOP:
                        nEnd = j+3
                        if len(self._rev_seq[nStart:nEnd]) >= l:
                            ORF = OrfSeq(self._rev_seq, self.__length-nEnd, self.__length-nStart, '-', nStart%3)
                            ORF.set_codon_table(self._codon_table)
                            self.__orfs.append(ORF)
                        break
        return sorted(self.__orfs, key=lambda e:e.get_location()[0])

    def __reverse_complement(self):
        """Crée le brin complémentaire de la séquence."""
        rev_seq = ""
        reverse = {'A':'T', 'T':'A', 'C':'G', 'G':'C', 'N':'N'}
        rseq0 = self._seq[::-1]
        for i in range(0, len(self._seq)):
            rev_seq += reverse[rseq0[i]]
        return rev_seq



class OrfSeq(DnaSeq):

    def __init__(self, seq, start, end, strand, frame):
        """
        :param seq: (str) séquence de l'ORF
        :param start: (int) position du codon start dans le référentiel du brin +
        :param end: (int) position du codon stop dans le référentiel du brin +
        :param strand: (str) brin + ou brin -
        :param frame: (int) phase de l'ORF ; 0, 1 ou 2
        """
        self._ref_seq = seq
        self.__start = start
        self.__end = end
        self.__strand = strand
        self.__frame = frame
        self.__score = None

    def get_location(self):
        """Donne le couple de positions de l'ORF.

        :return: (tuple) le couple de (start, end) de l'ORF
        """
        return (self.__start+1, self.__end)

    def get_score(self):
        """Donne le score de l'ORF.

        :return: (float) score de l'ORF
        """
        return self.__score

    def get_strand(self):
        """Donne le brin de l'ORF.

        :return: (str) brin + ou brin -
        """
        return self.__strand

    def get_frame(self):
        """Donne la phase de lecture de l'ORF.

        :return: (int) la phase de lecture de l'ORF
        """
        return self.__frame

    def get_orf(self):
        """Donne la séquence de l'ORF en prenant en compte le brin.

        :return: (str) la séquence
        """
        if self.__strand == '+':
            return self._ref_seq[self.__start:self.__end]
        else:
            return self._ref_seq[len(self._ref_seq)-self.__end:len(self._ref_seq)-self.__start]

    def compute_score_codon(self, table):
        """Calcule le score de chaque codon à partir de la table de comptage table.

        :param table: (dict) table de comptage
        """
        no_start_stop = set(self.__codon_table.keys())-{'START', 'STOP'}-set([s for s in self.__codon_table['STOP']])
        for codon in no_start_stop:
            aa = self.__codon_table[codon][0]
            syn_codon = [cod for cod in no_start_stop if self.__codon_table[cod][0] == aa]
            ri = len(syn_codon) * table[codon] / sum([table[cod] for cod in syn_codon])
            self.__codon_table[codon].append(ri)

    def set_codon_table(self, table):
        """Permet d'ajouter la table de codon à self.

        :param table: (dict) table de comptage
        """
        self.__codon_table = table

    def scoreORF(self):
        """Calcule le score de l'ORF."""
        self.__score = 0
        for codon in [self.get_orf()[i:i+3] for i in range(0, len(self.get_orf())-3, 3)]:
            ri = self.__codon_table[codon][1]
            self.__score += ri-1

    def read_matrix(self, Fi):
        """Lecture et création d'un dictionnaire stockant la matrice de poids.

        :param Fi: chemin vers le fichier contenant la matrice de poids de GGAGA
        """
        self.__matrix = {'A':[], 'C':[], 'G':[], 'T':[]}
        with open(Fi, 'r') as fileIn:
            fileIn.readline()
            for line in fileIn.readlines():
                split = line.split('\t')
                self.__matrix['A'].append(float(split[0]))
                self.__matrix['C'].append(float(split[1]))
                self.__matrix['G'].append(float(split[2]))
                self.__matrix['T'].append(float(split[3]))


    def rechercheRBS(self):
        """Recherche la présence du site de fixation RBS GGAGA en tenant compte de la matrice de poids."""
        if self.__strand == "+":
            if self.__start <= 15:
                return False
            else:
                list_motifs = [self._ref_seq[i:i+5] for i in range(self.__start-15-1, self.__start-8+1)]
                for motif in list_motifs:
                    score = 0
                    cpt = 0
                    for l in motif:
                        score += self.__matrix[l][cpt]
                        cpt += 1
                    if score >= 4.5:
                        return True
                return False
        else:
            start_rev = len(self._ref_seq)-self.__end
            if start_rev <= 15:
                return False
            else:
                list_motifs = [self._ref_seq[i:i+5] for i in range(start_rev-15, start_rev-8+1)]
                for motif in list_motifs:
                    score = 0
                    cpt = 0
                    for l in motif:
                        score += self.__matrix[l][cpt]
                        cpt += 1
                    if score >= 4.5:
                        return True
                return False
