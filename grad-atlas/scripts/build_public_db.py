#!/usr/bin/env python3
"""Create a standalone PUBLIC SQLite database from sanitized JSON only."""
import json,sqlite3,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--input',default='data/catalogue.json');p.add_argument('--output',default='data/catalogue.sqlite');a=p.parse_args()
d=json.loads(Path(a.input).read_text());out=Path(a.output)
if out.exists():out.unlink()
c=sqlite3.connect(out)
c.executescript('''CREATE TABLE metadata(key TEXT PRIMARY KEY,value_json TEXT NOT NULL); CREATE TABLE records(id TEXT PRIMARY KEY,kind TEXT NOT NULL,title TEXT NOT NULL,institution TEXT,country TEXT,field TEXT,status TEXT,checked_at TEXT,latest_regional INTEGER,pure_maths INTEGER,source_link_status TEXT,details_json TEXT NOT NULL); CREATE TABLE sections(record_id TEXT NOT NULL REFERENCES records(id),position INTEGER NOT NULL,label TEXT,text TEXT,status TEXT,PRIMARY KEY(record_id,position)); CREATE TABLE sources(record_id TEXT NOT NULL REFERENCES records(id),position INTEGER NOT NULL,url TEXT NOT NULL,title TEXT,PRIMARY KEY(record_id,position)); CREATE INDEX records_country ON records(country); CREATE INDEX records_kind ON records(kind);''')
c.executemany('insert into metadata values(?,?)',[(k,json.dumps(v,ensure_ascii=False,separators=(',',':'))) for k,v in sorted(d['meta'].items())])
for r in d['records']:
 c.execute('insert into records values(?,?,?,?,?,?,?,?,?,?,?,?)',(r['id'],r['kind'],r['title'],r['institution'],r['country'],r['field'],r['status'],r['checkedAt'],int(r['latestRegional']),int(r['pureMaths']),r['sourceLinkStatus'],json.dumps(r['details'],ensure_ascii=False,separators=(',',':'))))
 c.executemany('insert into sections values(?,?,?,?,?)',[(r['id'],i,s['label'],s['text'],s.get('status')) for i,s in enumerate(r['sections'])])
 c.executemany('insert into sources values(?,?,?,?)',[(r['id'],i,s['url'],s.get('title')) for i,s in enumerate(r['sources'])])
c.commit();c.execute('VACUUM');assert c.execute('pragma integrity_check').fetchone()[0]=='ok';assert not c.execute('pragma foreign_key_check').fetchall();print(out,out.stat().st_size)
