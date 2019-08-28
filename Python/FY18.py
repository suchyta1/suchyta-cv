#!/usr/bin/env python

import bibtexparser
import copy
import common


if __name__ == '__main__':
    num = 3
    me = '{Suchyta}, E.'
    ME = 'E. Suchyta'

    #infile = 'ads-2018-08-30.bib'
    infile = 'ads-2018-10-26.bib'
    selectedfile = 'suchyta-papers-FY18-modified.bib'

    suchyta = common.SuchytaPubs(files=[infile], use_arxiv=False, num=num, me=me, ME=ME)
    bib = suchyta.bib
    selected = copy.deepcopy(bib)
    spos = 0
    for j in range(len(bib.entries)):
        select = False

        if ( (bib.entries[j][u'year'] == '2017') and (bib.entries[j]['month'].lower() in ['oct', 'nov', 'dec']) ):
            select = True
        elif ( (bib.entries[j][u'year'] == '2018') and (bib.entries[j]['month'].lower() in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep']) ):
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

