#!/usr/bin/env python

import bibtexparser
import numpy as np
import numpy.core.defchararray as npchar
import copy
import json
import re

if __name__=='__main__':
    me = '{Suchyta}, E.'
    ME = 'E. Suchyta'
    num = 3

    infile = 'suchyta-papers.bib'
    selectedfile = 'suchyta-papers-FY17-modified.bib'

    with open(infile) as f:
        bib = bibtexparser.load(f)
    with open(infile) as f:
        selected = bibtexparser.load(f)

    spos = 0
    for j in range(len(bib.entries)):
        authors = npchar.strip( bib.entries[j]['author'].split(' and') )
        select = False
        omit = False

        if len(authors) > num:
            authors = authors[0:num]
            last = 'et~al.'
            if me not in authors:
                last = '%s (including %s)'%(last,ME)
            authors = np.append(authors, last)

        bib.entries[j]['author'] = ' and '.join(authors)
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

        if omit:
            del selected.entries[spos]
            continue

        if ( (u'journal' in bib.entries[j].keys()) and (bib.entries[j][u'journal'] == 'arXiv') ):
            select = True
        elif ( (bib.entries[j][u'year'] == '2016') and (bib.entries[j]['month'] in ['oct', 'nov', 'dec']) ):
            select = True
        elif ( (bib.entries[j][u'year'] == '2017') and (bib.entries[j]['month'] in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep']) ):
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
