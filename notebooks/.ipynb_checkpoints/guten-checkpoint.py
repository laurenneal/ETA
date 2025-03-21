import pandas as pd
import glob
import re
import rdflib

gut_url = 'https://www.gutenberg.org/ebooks/{}'
gut_txt = 'https://www.gutenberg.org/ebooks/{}.txt.utf-8'

data_dir = '/home/rca2t/Public/ETA/data/gutenberg/cache/epub'
epub_path = data_dir + '/{0}/pg{0}.rdf'
TAG = re.compile(r'<[^>]+>')

gids = [int(path.split('/')[-1]) for path in glob.glob(data_dir+'/*')]

gids = sorted(gids)

df = pd.DataFrame(gids,  columns=['gut_id'])

def get_element(df, kw, str_col='line'):
    try:
        el = df[df[str_col].str.contains(kw)][str_col].str.replace(TAG, '').values[0].strip()
    except IndexError:
        el = None
    return el
    
sample = df.gut_id.sample(20)
for gid in sample:
    path = epub_path.format(gid)

    g = rdflib.Graph()
    g.load(path)
    print('-' * 80)
    for s,p,o in g:
        if re.search(r'dc/terms/subject', p):
            print('S:', s)
            print('P:', p)
            print('O:', o)
            print('---')
    
    with open(path, 'r') as epub_file:
        epub = pd.DataFrame(epub_file.readlines(), columns=['line'])
        title = get_element(epub, 'dcterms:title', 'line')
        creator = get_element(epub, 'pgterms:name', 'line')
        row = (gid, title, creator)
        print(row)
        
