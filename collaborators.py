import bibtexparser
import pandas as pd
import datetime
import itertools

parser =  bibtexparser.bparser.BibTexParser(common_strings=True,
                                            homogenize_fields=True)
with open('references.bib') as bibtex_file:
    bib_database = parser.parse_file(bibtex_file)

df = pd.DataFrame(bib_database.entries).convert_objects(convert_numeric=True)
nyears = 4
# subset to only include my articles
df_recent = df[df.author.str.contains('Abernathey', na=False) &
               (df.year > (datetime.datetime.now().year - nyears))]


def homogenize_authorname(name):
    # strip weird latex
    name = name.translate(dict.fromkeys(map(ord, "'`{\}"), None))
    
    # assume it's last name first if there is a comma
    if ',' in name:
        last_name, rest = name.split(',')
    else:
        segments = name.split()
        last_name = segments[-1]
        rest = segments[:-1]
    if type(rest) is str:
        rest = [rest.strip()]
    rest_abbrv = [r[0] + '.' for r in rest]
    return [last_name] +  [' '.join(rest_abbrv)]

all_coauthors = list(itertools.chain(*df_recent.author.str.split('\s+and\s+')))
# remove myself
other_coauthors = [homogenize_authorname(author)
                   for author in all_coauthors if 'Abernathey' not in author]
author_df = pd.DataFrame(other_coauthors, columns=['last', 'first'])
author_df = author_df.drop_duplicates('last').sort_values('last')
author_list = author_df['last'].str.cat(author_df['first'], sep=', ').str.cat(sep='; ')
print(author_list)