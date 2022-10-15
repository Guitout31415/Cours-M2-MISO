var _pj;

function _pj_snippets(container) {
  function in_es6(left, right) {
    if (right instanceof Array || typeof right === "string") {
      return right.indexOf(left) > -1;
    } else {
      if (right instanceof Map || right instanceof Set || right instanceof WeakMap || right instanceof WeakSet) {
        return right.has(left);
      } else {
        return left in right;
      }
    }
  }

  container["in_es6"] = in_es6;
  return container;
}

_pj = {};

_pj_snippets(_pj);

class DnaSeq {
  constructor(id, desc, seq) {
    /*
    :param id: (str) id de la séquence
    :param desc: (str) description de la séquence
    :param seq: (str) la séquence ADN
    */
    this.__id = id;
    this.__description = desc;
    this._seq = seq;
    this.__length = seq.length;
    this._codon_table = null;
    this._rev_seq = this.__reverse_complement();
  }

  get_id() {
    /*Donne l'id de la séquence.
     :return: (str) id du gène
    */
    return this.__id;
  }

  get_sequence() {
    /*Donne la séquence d'ADN.
     :return: (str) séquence d'ADN
    */
    return this._seq;
  }

  get_desc() {
    /*Donne la description de la séquence.
     :return: (str) description de la séquence
    */
    return this.__description;
  }

  computeORF(l) {
    /*Calcule tous les ORF de taille >= l dans la séquence.
     :param l: (int) longueur minimale des ORF à chercher
    :return: (list) liste des ORFs triées par position de départ croissante
    */
    var ORF, START, STOP, codon, codon2, nEnd, nStart;
    this.__orfs = [];
    [START, STOP] = [this._codon_table["START"], this._codon_table["STOP"]];

    for (var i = 0, _pj_a = this.__length; i < _pj_a; i += 1) {
      codon = this._seq.slice(i, i + 3);

      if (_pj.in_es6(codon, START)) {
        nStart = i;

        for (var j = i, _pj_b = this.__length; j < _pj_b; j += 3) {
          codon2 = this._seq.slice(j, j + 3);

          if (_pj.in_es6(codon2, STOP)) {
            nEnd = j + 3;

            if (this._seq.slice(nStart, nEnd).length >= l) {
              ORF = new OrfSeq(this._seq, nStart, nEnd, "+", nStart % 3);
              ORF.set_codon_table(this._codon_table);

              this.__orfs.append(ORF);
            }

            break;
          }
        }
      }
    }

    for (var i = 0, _pj_a = this.__length; i < _pj_a; i += 1) {
      codon = this._rev_seq.slice(i, i + 3);

      if (_pj.in_es6(codon, START)) {
        nStart = i;

        for (var j = nStart, _pj_b = this.__length; j < _pj_b; j += 3) {
          codon2 = this._rev_seq.slice(j, j + 3);

          if (_pj.in_es6(codon2, STOP)) {
            nEnd = j + 3;

            if (this._rev_seq.slice(nStart, nEnd).length >= l) {
              ORF = new OrfSeq(this._rev_seq, this.__length - nEnd, this.__length - nStart, "-", nStart % 3);
              ORF.set_codon_table(this._codon_table);

              this.__orfs.append(ORF);
            }

            break;
          }
        }
      }
    }

    return sorted(this.__orfs, {
      "key": e => {
        return e.get_location()[0];
      }
    });
  }

}
