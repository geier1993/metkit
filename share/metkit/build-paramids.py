#!/usr/bin/env python
import MySQLdb
import yaml
import re
import os


db = MySQLdb.connect("grib-param-db-prod.ecmwf.int",
                     "ecmwf_ro",
                     "ecmwf_ro",
                     "param")

PRODGEN = {}
if os.path.exists("prodgen-paramids.yaml"):
    with open("prodgen-paramids.yaml") as f:
        PRODGEN = yaml.load(f.read())

PARAMSIDS = {}
if os.path.exists("paramids.yaml"):
    with open("paramids.yaml") as f:
        PARAMSIDS = yaml.load(f.read())

cursor = db.cursor()

cursor.execute("select * from param")

for data in cursor.fetchall():
    paramid, abbr, longname = int(data[0]), data[1].lower(), data[2].lower()

    if abbr == '~':
        continue

    abbr = re.sub(r'\W', '_', abbr)
    abbr = re.sub(r'_+', '_', abbr)
    abbr = re.sub(r'^_', '', abbr)
    abbr = re.sub(r'_$', '', abbr)

    entry = [abbr, longname]

    if paramid in PRODGEN:
        pgen = [str(x).lower() for x in PRODGEN[paramid]]
        p = []
        for n in pgen:
            if n not in entry and (' ' not in n) and ('.' not in n) and ('-' not in n):
                entry.append(n)
                p.append(n)

    entry = tuple(entry)

    if paramid in PARAMSIDS:
        before = tuple(PARAMSIDS[paramid])
        if before != entry:
            print("WARNING! updated paramid: {},  {} => {}".format(paramid, before, entry))
            PARAMSIDS[paramid] = list(entry)
    else:
        print("new paramid: {} {}".format(paramid, entry))
        PARAMSIDS[paramid] = list(entry)

cursor.close()
db.close()


for paramid, entry in PRODGEN.items():
    if paramid not in PARAMSIDS:
        print("WARNING! adding pseudo-paramid: {},  {}".format(paramid, tuple(entry)))
        PARAMSIDS[paramid] = entry

with open("paramids.yaml", "w") as f:
    f.write(yaml.safe_dump(PARAMSIDS, default_flow_style=False))
