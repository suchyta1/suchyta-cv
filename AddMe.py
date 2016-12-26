#!/usr/bin/env python

import bibtexparser
import numpy as np
import numpy.core.defchararray as npchar
import copy
import re

if __name__=='__main__':
    me = '{Suchyta}, E.'
    ME = 'E. Suchyta'
    num = 3

    infile = 'suchyta-papers-2.bib'
    selectedfile = 'suchyta-papers-selected-modified.bib'
    additionalfile = 'suchyta-papers-additional-modified.bib'

    with open(infile) as f:
        bib = bibtexparser.load(f)
    with open(infile) as f:
        selected = bibtexparser.load(f)
    with open(infile) as f:
        additional = bibtexparser.load(f)

    spos = 0
    apos = 0
    for j in range(len(bib.entries)):
        authors = npchar.strip( bib.entries[j]['author'].split(' and') )
        select = True
        omit = False

        if len(authors) > num:
            authors = authors[0:num]
            last = 'et~al.'
            if me not in authors:
                last = '%s (including %s)'%(last,ME)
                select = False
            if bib.entries[j][u'ID'] in ['2012SPIE.8451E..12H', '2015AJ....150..150F', '2016JPhCS.759a2095K', 'choi2016stream']:
                select = True
            authors = np.append(authors, last)

        bib.entries[j]['author'] = ' and '.join(authors)
        bib.entries[j]['author'] = bib.entries[j]['author'].replace("{Fermi-LAT}, T.", "{Fermi-LAT}")
        bib.entries[j]['title'] = bib.entries[j]['title'].replace('\ge', '$\ge$')

        if (u'journal' in bib.entries[j].keys()) and (bib.entries[j][u'journal'].lower().find('arxiv')!=-1):
            bib.entries[j][u'journal'] = 'arXiv'
            bib.entries[j][u'volume'] = bib.entries[j]['eprint']
        comp = re.compile('<.+?>')
        bib.entries[j][u'title'] = comp.sub('',bib.entries[j][u'title']).strip()
        comp = re.compile('\\\~\{\}')
        bib.entries[j][u'title'] = comp.sub('$\sim$',bib.entries[j][u'title']).strip()

        if (u'pages' in bib.entries[j].keys()) and (bib.entries[j][u'pages']=='0'):
            del bib.entries[j]['pages']
        if (u'booktitle' in bib.entries[j].keys()) and (bib.entries[j][u'booktitle'].lower().find('aps meeting')!=-1):
            omit = True
        if (u'journal' in bib.entries[j].keys()) and (bib.entries[j][u'journal'].lower().find("the astronomer's telegram")!=-1):
            omit = True
        if (u'title' in bib.entries[j].keys()) and (bib.entries[j][u'title'].startswith("Embrace the Dark Side")):
            omit = True

        if omit:
            del selected.entries[spos]
            del additional.entries[apos]
            continue

        if not select:
            del selected.entries[spos]
            additional.entries[apos] = copy.copy( bib.entries[j] )
            apos += 1
        else:
            del additional.entries[apos]
            selected.entries[spos] = copy.copy( bib.entries[j] )
            spos += 1


    writer = bibtexparser.bwriter.BibTexWriter()
    writer.order_entries_by = False
    with open(additionalfile, 'w') as out:
        out.write(writer.write(additional))

    writer = bibtexparser.bwriter.BibTexWriter()
    writer.order_entries_by = False
    with open(selectedfile, 'w') as out:
        out.write(writer.write(selected))
