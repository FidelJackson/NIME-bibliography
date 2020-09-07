#!/usr/local/bin/python3
"""
Loads a NIME Proceedings Bibtex File and adds or removes fields. Formatting standards are set out in utils.py
"""
import glob
import bibtexparser
import utils
import sys
import argparse

parser = argparse.ArgumentParser(description='Loads a NIME Proceedings Bibtex File and harmonises the fields, entry order, and formatting with the standards set out in utils.py, then saves back to the same file.')
parser.add_argument('year', action='store', type=int, help='the NIME year to load: 2001 will load nime2001.bib')
parser.add_argument('--add_field', action='store_true', help='adds a field to all entries in one bibtex file')
parser.add_argument('--id_order', action='store_true', help='sorts the output by entry ID/key (default: sort by article/page number)')
parser.add_argument('--field_key', action='store', type=str, help='Field key to add/remove.')
parser.add_argument('--field_value', action='store', type=str, help='Field value to add.')
args = parser.parse_args()

nime_year = args.year
nime_file = f"../paper_proceedings/nime{nime_year}.bib"

'''
Add a key:value pair to every entry in a database.
'''
def add_field_to_database(db, key, value):
    for e in db.entries:
        e[key] = value
    return db

## Load
print(f"Going to load: {nime_file}, hope that's ok.")

with open(nime_file) as bibtex_file:
    bib_database = bibtexparser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)
    
print(f"Loaded {len(bib_database.entries)} entries.")

## Edit
if args.add_field:
    bib_database = add_field_to_database(bib_database, args.field_key, args.field_value)


## Write
# set ordering property:
if (args.id_order):
    utils.writer.order_entries_by = ("ID")
    print("ordering by ID")
else:
    print("using default order:", utils.writer.order_entries_by)
# else, canonical order: #utils.writer.order_entries_by = ("articleno", "url", "ID")

# Write back to the bibtex file
with open(nime_file, 'w') as bibtex_file:
    bibtex_file.write(utils.writer.write(bib_database))
    
print(f"Saved new entried to: {nime_file}, hope that's ok.")
sys.exit(0)
