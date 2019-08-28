#!/usr/bin/env python

import bibtexparser
import copy
import common


if __name__ == '__main__':
    num = 3
    me = '{Suchyta}, E.'
    ME = 'E. Suchyta'

    selectedfile = 'suchyta-papers-new.bib'
    infiles  = ["../2019-03-26.bib", "../cs.bib"]
    suchyta = common.SuchytaPubs(files=infiles, use_arxiv=False, num=num, me=me, ME=ME)
    bib = suchyta.bib
    writer = bibtexparser.bwriter.BibTexWriter()
    writer.order_entries_by = False
    with open(selectedfile, 'w') as out:
        out.write(writer.write(bib))


    """
    infile = '../2019-03-26.bib'
    selectedfile = 'suchyta-papers-new.bib'
    suchyta = common.SuchytaPubs(files=[infile], use_arxiv=False, num=num, me=me, ME=ME)

    bib = suchyta.bib
    print(type(bib.entries))
    selected = copy.deepcopy(bib)
    spos = 0
    for j in range(len(bib.entries)):
        select = True

        if select:
            selected.entries[spos] = copy.copy( bib.entries[j] )
            spos += 1
        else:
            del selected.entries[spos]
            continue

    writer = bibtexparser.bwriter.BibTexWriter()
    writer.order_entries_by = False
    with open(selectedfile, 'w') as out:
        out.write(writer.write(selected))
    """

