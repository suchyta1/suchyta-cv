import bibtexparser
import numpy as np
import numpy.core.defchararray as npchar
import re
from operator import itemgetter


class SuchytaPubs(object):

    def MonthMap(self, check, bib, index):

        for i, month in enumerate(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']):

            if check.find(month) != -1:
                bib.entries[index]['monthnum'] = i + 1

        return bib


    def AddMonthNum(self, bib):
        for i in range(len(bib.entries)):

            try:
                month = bib.entries[i]['month'].lower()
            except:
                month = 0

            bib = self.MonthMap(month, bib, i)

        return bib


    def read(self, files):
        bibtxt = ""
        for infile in files:
            with open(infile) as f:
                thistxt = f.read()
                bibtxt = bibtxt + thistxt
        return bibtxt


    def autoselect(self, bib, j, use_arxiv):
        omit = False
        if ((u'journal' in bib.entries[j].keys()) and (bib.entries[j][u'journal'] == 'arXiv' )):
            del bib.entries[j]['pages']
            del bib.entries[j]['eid']
            if not use_arxiv:
                omit = True

        if (u'pages' in bib.entries[j].keys()) and (bib.entries[j][u'pages'] == '0'):
            del bib.entries[j]['pages']

        if (u'booktitle' in bib.entries[j].keys()) and (bib.entries[j][u'booktitle'].lower().find('aps meeting') != -1):
            omit = True

        if (u'journal' in bib.entries[j].keys()) and (bib.entries[j][u'journal'].lower().find("the astronomer's telegram") != -1):
            omit = True

        if ((u'journal' in bib.entries[j].keys()) and (bib.entries[j][u'journal'].lower().find('vizier') != -1)):
            omit = True

        return omit


    def __init__(self, files=[], use_arxiv=False, num=3, me='{Suchyta}, E.', ME='E. Suchyta'):

        bibtxt = self.read(files)
        bib = bibtexparser.loads(bibtxt)
        bib = self.AddMonthNum(bib)
        bib.entries = sorted(bib.entries, key=itemgetter('year', 'monthnum'), reverse=True)
        for i in range(len(bib.entries)):
            bib.entries[i]['monthnum'] = str(bib.entries[i]['monthnum'])

        spos = 0
        dec = 0
        for j in range(len(bib.entries)):

            j -= dec
            authors = npchar.strip( bib.entries[j]['author'].split(' and') )

            if len(authors) > num:
                authors = authors[0:num]
                last = 'et~al.'
                if me not in authors:
                    last = '%s (including %s)' % (last,ME)
                authors = np.append(authors, last)

            bib.entries[j]['author'] = ' and '.join(authors)
            bib.entries[j]['author'] = bib.entries[j]['author'].replace("{Fermi-LAT}, T.", "{Fermi-LAT}")
            bib.entries[j]['title'] = bib.entries[j]['title'].replace('$\lt$', '$<$')
            bib.entries[j]['title'] = bib.entries[j]['title'].replace('{\minus}', '$-$')
            bib.entries[j]['title'] = bib.entries[j]['title'].replace('z = 2.7', 'z~=~2.7')

            if ((u'journal' in bib.entries[j].keys()) and (bib.entries[j][u'journal'].lower().find('arxiv') != -1)):
                bib.entries[j][u'journal'] = 'arXiv'
                bib.entries[j][u'volume'] = bib.entries[j]['eprint']

            comp = re.compile('<.+?>')
            bib.entries[j][u'title'] = comp.sub('',bib.entries[j][u'title']).strip()
            comp = re.compile('\\\~\{\}')
            bib.entries[j][u'title'] = comp.sub('$\sim$',bib.entries[j][u'title']).strip()

            omit = self.autoselect(bib, j, use_arxiv)
            if omit:
                del bib.entries[spos]
                dec += 1
            else:
                spos += 1

        self.bib = bib

