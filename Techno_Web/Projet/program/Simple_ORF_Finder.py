"""Ce programme permet de prédire des ORFs dans une séquence ADN à l'aide d'une table de comptage des codons."""
__author__ = ['LEMAIRE Guillaume', 'LUONG Tony']

import argparse
import sys
from Seq import *

def parseFasta(Fi):
    """Permet d'extraire l'identifiant, la description et la séquence du fichier Fi.

    :param Fi: (str) lien vers le fichier au format fasta
    :return: (list) liste contenant l'objet DnaSeq
    """
    assert Fi.split('.')[-1] in {'fa', 'fna', 'ffn', 'faa', 'frn', 'fas', 'fasta'}, \
        "Veuillez fournir un fichier au format Fasta !"
    DNA_list = []
    with open(Fi, 'r') as fileIn:
        all_lines = fileIn.readlines()
    cpt_line = 0
    for line in all_lines:
        if '>' == line[0]:
            split = line.split(' ')
            id, desc = split[0][1:], ' '.join(split[1:-1])
            seq = ""
            for line2 in all_lines[cpt_line+1:]:
                if line2[0] == '>':
                    break
                else:
                    seq += line2[:-1]
            DNA_list.append(DnaSeq(id, desc, seq))
        cpt_line += 1
    return DNA_list

def count_codon(dna):
    res = dict()
    seq = dna.get_sequence()
    for a in ["A", "T", "C", "G"]:
        for b in ["A","T","C","G"]:
            for c in ["A","T","C","G"]:
                res[a+b+c] = seq.count(a+b+c)
    return res

def search_orf_in_interval(debutIntervalle, finIntervalle, l_orf):
    """Permet de chercher des ORFs dans la liste l_orf.

    Utilise une double dichotomie pour chercher les positions des ORFs
    ayant leurs positions start entre debutIntervalle et finIntervalle.

    :param debutIntervalle: (int) borne inférieure
    :param finIntervalle: (int) borne supérieure
    :param l_orf: (list) liste d'ORFs
    :return: (list) liste d'ORFs tel que debut < start < fin
    """
    a, b = 0, len(l_orf)-1
    m1 = (a+b)//2
    while m1 != a and m1 != b:
        if l_orf[m1].get_location()[0] < debutIntervalle:
            a = m1
            m1 = (a + b) // 2
        elif l_orf[m1].get_location()[0] > debutIntervalle:
            b = m1
            m1 = (a + b) // 2
        elif l_orf[m1].get_location()[0] == debutIntervalle:
            break
    if l_orf[m1].get_location()[0] < debutIntervalle:
        m1 += 1
    a, b = m1, len(l_orf)-1
    m2 = (a+b)//2
    while m2 != a and m2 != b:
        if l_orf[m2].get_location()[0] < finIntervalle:
            a = m2
            m2 = (a+b)//2
        elif l_orf[m2].get_location()[0] > finIntervalle:
            b = m2
            m2 = (a+b)//2
        elif l_orf[m2].get_location()[0] == finIntervalle:
            break
    if l_orf[m2+1].get_location()[0] < finIntervalle:
        m2 += 1
    return l_orf[m1:m2+1]

def display_orf(all_orf, output_file):
    """Permet d'afficher toutes les ORFs au format gff.

    :param all_orf: (dict) dictionnaire de toutes les ORFs de tous les objets DnaSeq
    :param output_file: (str) fichier de sortie du listing des ORFs
    """
    go_print = ''
    for DnaSeq in all_orf.keys():
        orfs = all_orf[DnaSeq][1]
        for orf in orfs:
            go_print += DnaSeq.get_id() + "\tSimple_ORF_Finder\t" + DnaSeq.get_desc() + "\t" + \
                   str(orf.get_location()[0]) + "\t" + str(orf.get_location()[1]) + "\t" + str(orf.get_score()) + \
                   "\t" + orf.get_strand() + "\t" + str(orf.get_frame()) + '\n'

    if output_file is not None:
        with open(output_file, 'w') as fileOut:
            fileOut.write(go_print)

    else:
        print(go_print)

def read_usage_table(Fi):
    """Lit la table de comptage des codons stocké dans le fichier Fi.

    :param Fi: (str) lien vers la table de comptage des codons
    :return: (dict) table de comptage des codons
    """
    res = {}
    with open(Fi, 'r') as fileIn:
        for line in fileIn:
            split = line.split('\t')[:]
            res[split[0]] = int(split[-1][:-1])
    return res

def computeORFscore(list_orf, table):
    """Permet de calculer le score de tous les ORFs.

    :param list_orf: (list) liste des ORFs
    :param table: (dict) table de comptage
    :return: (list) liste des ORFs qui ont leur score calculés
    """
    for orf in list_orf:
        orf.compute_score_codon(table)
        orf.scoreORF()
    return list_orf

def is_separated(A, B):
    """Permet de savoir si A et B sont disjoints.

    :param A: (tuple, list) intervalle A
    :param B: (tuple, list) intervalle B
    :return: (bool) True si A ∩ B = ∅, False sinon.
    """
    interA = set([i for i in range(A[0], A[1]+1)])
    interB = set([i for i in range(B[0], B[1]+1)])
    return interA & interB == set()

def first_no_intersection(list_orf):
    """Calcule l'ORF disjointe la plus proche de celle que l'on regarde.

    :param list_orf: (list) liste d'objets ORF
    :return: (dict) key = position de l'ORF dans list_orf ; value = position de la 1ère ORF qui n'intersecte pas la key
    """
    res = {}
    for j in range(len(list_orf)-1, 0, -1):
        J = j-1
        while not is_separated(list_orf[J].get_location(), list_orf[j].get_location()):
            J -= 1
            if J < 0:
                break
        res[j] = J
    return res

def SORF(i, list_orf, no_inter, scoremax):
    """Calcule le score maximal après avoir lu les i premières ORF non-chevauchantes.

    :param i: (int) index
    :param list_orf: (list) liste des ORFs
    :param no_inter: (dict) key = position de l'ORF dans list_orf ; value = position de la 1ère ORF qui n'intersecte pas la key
    :param scoremax: (list) liste contenant [SORF(0), SORF(1), ..., SORF(i-1)]
    :return: (int) le score maximisé pour les i premières ORF
    """
    if i == 0:
        return list_orf[0].get_score()
    if no_inter[i] == -1:
        return max(scoremax[i-1], list_orf[i].get_score())
    return max(scoremax[i-1], scoremax[no_inter[i]]+list_orf[i].get_score())

def maximiseORFscore(list_orf):
    """Calcule le score maximal pour tous les ORFs non-chevauchantes.

    :param list_orf: (list) liste d'ORFs
    :return: (tuple) le score maximal et liste des ORFs qui sont à l'origine du score maximal
    """
    list_orf = sorted(list_orf, key=lambda x:x.get_location()[1])
    no_inter = first_no_intersection(list_orf)
    scoremax = []

    for i in range(len(list_orf)):
        scoremax.append(SORF(i, list_orf, no_inter, scoremax))

    orf_max = []
    i = len(list_orf)-1
    while i != -1:
        if scoremax[i] == scoremax[no_inter[i]]+list_orf[i].get_score():
            orf_max.append(list_orf[i])
            i = no_inter[i]
        else:
            i -= 1
        if no_inter[i] == -1:
            break
    orf_max.append(list_orf[scoremax.index(max(scoremax[:i]))])
    return (scoremax, sorted(orf_max, key=lambda x:x.get_location()[0]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Simple_ORF_finder.py", description="Programme de recherche d'ORF")
    parser.add_argument('-f', '--infasta', help="lien vers le fichier fasta du génome à analyser", required=True)
    #parser.add_argument('-c', '--counttable', help="lien vers table de comptage des codons", required=True)
    parser.add_argument('-t', '--codonstable', help="lien vers code génétique utilisé pour la traduction", required=True)
    parser.add_argument('-o', '--outgff', help="nom d'un fichier de sortie au format GFF")
    parser.add_argument('-s', '--minorfsize', help='taille minimum des ORFs (défaut = 300)', type=int, default=300)
    parser.add_argument('-i', '--interval', help="intervalle de positions pour récupérer les ORFs ayant un codon start dans l'intervalle (par défaut = toutes les ORFs)", type = int, nargs = 2, default=[0,0])
    parser.add_argument('-m', '--matrix', help="lien vers la matrice de poids GGAGA avec un score seuil = 4.5", required=True)
    params = parser.parse_args(sys.argv[1:])

    print("Lancement du programme de recherche d'ORF : \n")

    DnaSeq_list = parseFasta(params.infasta)
    ORF_of_DNAseq = {}
    for DnaSeq in DnaSeq_list:
        DnaSeq.set_codon_table(params.codonstable)
        list_ORF = DnaSeq.computeORF(params.minorfsize)
        for orf in list_ORF:
            orf.read_matrix(params.matrix)
        usage_table = count_codon(DnaSeq)
        #usage_table = read_usage_table(counttable)
        list_ORF = computeORFscore(list_ORF, usage_table)
        list_ORF_filtering = [orf for orf in list_ORF if orf.rechercheRBS()]
        maximise = maximiseORFscore(list_ORF_filtering)
        if params.interval == [0, 0]:
            list_ORF_final = search_orf_in_interval(0, len(DnaSeq_list[0].get_sequence()), maximise[1])
        else:
            list_ORF_final = search_orf_in_interval(params.interval[0], params.interval[1], maximise[1])
        ORF_of_DNAseq[DnaSeq] = (maximise[0][-1], list_ORF_final)


    for dna in ORF_of_DNAseq:
        if params.outgff is None:
            print(f"Le score maximal de {dna.get_id()} est de {ORF_of_DNAseq[dna][0]} et vous trouverez toutes les ORFs non-chevauchantes qui en sont à l'origine au format gff plus bas :\n")
        else:
            print(f"Le score maximal de {dna.get_id()} est de {ORF_of_DNAseq[dna][0]} et vous trouverez toutes les ORFs non-chevauchantes qui en sont à l'origine au format gff dans le fichier {params.outgff}.")
    display_orf(ORF_of_DNAseq, params.outgff)

