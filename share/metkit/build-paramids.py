#!/usr/bin/env python

import yaml
import mysql.connector

with open("paramids.yaml") as f:
    PARAMSIDS = yaml.load(f.read())

db = mysql.connector.connect(host="grib-param-db-prod.ecmwf.int",
                     user="ecmwf_ro",
                     password="ecmwf_ro",
                     database="param")

cursor = db.cursor()

cursor.execute("select * from param")

for data in cursor.fetchall():
    paramid, abbr, longname = data[0], data[1], data[2]

    if abbr == '~':
        continue

    if paramid in PARAMSIDS:
        pass
    else:
        print "new paramid: %s %s %s" % (int(paramid), abbr, longname.lower())
        PARAMSIDS[paramid] = [abbr, longname]

cursor.close()
db.close()

with open("paramids.yaml", "w") as f:
    f.write(yaml.dump(PARAMSIDS, default_flow_style=False))
