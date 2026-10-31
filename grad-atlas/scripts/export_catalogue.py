#!/usr/bin/env python3
"""Read-only export of public research fields; never exports source blobs/audit history."""
import argparse, sqlite3, json, re, hashlib, collections
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit
p=argparse.ArgumentParser();p.add_argument('database');p.add_argument('--output',default='data/catalogue.json');a=p.parse_args()
c=sqlite3.connect('file:'+str(Path(a.database).resolve())+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
PRIVATE_HOSTS={'drive.google.com','docs.google.com','mail.google.com','chatgpt.com','github.com','oaiusercontent.com'}
URL=re.compile(r'https?://[^\s<>"\]\[{}]+')
DROP=re.compile(r'(?:password|secret|token|cookie|authorization|email|personal_|for_user|raw_html|response_headers|local_path|file_path|source_revision|source_payload|source_file|source_registry|candidate_file|report$|report_path|json_pointer|workspace|private|actor|audit_context)',re.I)
def safeurl(v):
 try:
  u=urlsplit(v.rstrip('.,;)')); host=(u.hostname or '').lower()
  if u.scheme not in ('https','http') or not host or any(host==x or host.endswith('.'+x) for x in PRIVATE_HOSTS) or 'localhost' in host: return None
  if re.search('token|secret|key|signature|auth|session',u.query,re.I):return None
  return urlunsplit((u.scheme,u.netloc,u.path,u.query,u.fragment))
 except ValueError:return None
def cleanstr(s):
 s=URL.sub(lambda m:safeurl(m.group()) or '[private reference omitted]',s)
 s=re.sub(r'(?<![A-Za-z0-9:/])/(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_./-]+','[internal path omitted]',s)
 s=re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}','[email omitted]',s)
 return s
def clean(v):
 if isinstance(v,dict):return {k:clean(x) for k,x in v.items() if not DROP.search(k)}
 if isinstance(v,list):return [clean(x) for x in v]
 if isinstance(v,str):return cleanstr(v)
 return v
def urls(v):
 if isinstance(v,dict):
  for x in v.values():yield from urls(x)
 elif isinstance(v,list):
  for x in v:yield from urls(x)
 elif isinstance(v,str):
  for x in URL.findall(v):
   u=safeurl(x)
   if u:yield u
def sources(v):return [{'url':u,'title':urlsplit(u).hostname} for u in dict.fromkeys(urls(v))]
def display(v):
 if v is None:return ''
 if isinstance(v,str):return v
 if isinstance(v,list):return '; '.join(display(x) for x in v)
 if isinstance(v,dict):return '; '.join(k.replace('_',' ')+': '+display(x) for k,x in v.items())
 return str(v)
def first(d,*keys):
 for k in keys:
  if d.get(k):return display(d[k])
 return ''
def country(d):
 s=first(d,'country','awarding_institution_country')
 if not s and d.get('source_batch') in ['regional','hku-cuhk','hkust-cityu']:s='Hong Kong'
 return {'Hong Kong SAR':'Hong Kong','Hong Kong SAR, China':'Hong Kong','USA':'United States','US':'United States','UK':'United Kingdom','United States of America':'United States'}.get(s,s or 'Unspecified')
def date(d):return first(d,'checked_at','checked_date','reviewed_date','retrieved_date','review_date','reviewed_at_utc','reviewed_utc')[:10] or None
records=[]
for row in c.execute('select p.*,i.name institution from programmes p left join institutions i on p.institution_id=i.id order by p.id'):
 d=dict(row);pid=d['id']; fs=[dict(r) for r in c.execute('select kind,text,verification_status from facts where programme_id=?',(pid,))]
 obs=[dict(r) for r in c.execute('select id,kind,raw_json,checked_date from observations where programme_id=?',(pid,))]
 observations=[{'kind':r['kind'],'checkedAt':r['checked_date'],'data':clean(json.loads(r['raw_json']))} for r in obs]
 sections=[{'label':r['kind'].replace('_',' ').title(),'text':cleanstr(r['text']),'status':r['verification_status']} for r in fs]
 # Repeated imports may preserve equivalent prose. Display once without deleting underlying facts.
 sections=list({json.dumps(s,sort_keys=True):s for s in sections}.values())
 ev=[r[0] for r in c.execute('select distinct e.url from evidence e join observation_evidence oe on oe.evidence_id=e.id join observations o on oe.observation_id=o.id where o.programme_id=?',(pid,))]
 checked=max([r['checked_date'] for r in obs if r['checked_date']]+['']) or None
 conflicts=[dict(r) for r in c.execute('select summary,status,resolution from conflicts where programme_id=?',(pid,))]
 institution_fallback={'24d7237c-b861-5cb8-97f3-26987b6da870':'Boston University','3149e53c-5253-5108-b735-77487518b410':'Simon Fraser','41433563-9ab9-5fb5-bdea-a7e9fad0becb':'Auckland and Waikato','ac3e031f-9bc1-551d-8b4b-1d454c0c7f00':'Bristol / UWE','fe8b5d10-adf0-5786-9025-7ac1b31c7ab5':'Northeastern'}
 records.append({'id':pid,'kind':'programme','title':d['programme_name'] or d['title'],'institution':d['institution'] or institution_fallback.get(pid,''), 'country':country(d),'field':d['field'] or 'Unspecified','status':d['status'],'checkedAt':checked,'latestRegional':any(r['kind']=='regional_review_20261030' for r in obs),'sources':sources([ev,fs,observations]),'sections':sections,'details':{'observations':observations,'conflicts':clean(conflicts)}})
for r in c.execute("select * from observations where kind='candidates' order by id"):
 d=json.loads(r['raw_json']);d=d if isinstance(d,dict) else {'notes':d};sd=clean(d)
 records.append({'id':'candidate-'+r['id'],'kind':'candidate','title':first(d,'program','programme_name','programme_title','programme','academic_programme','award') or 'Unnamed research candidate','institution':first(d,'university','institution','award_provider'),'country':country(d),'field':first(d,'field','source_field','field_group','index_field_group','fields') or 'Unspecified','status':'candidate','checkedAt':r['checked_date'] or date(d),'latestRegional':r['checked_date']=='2026-10-30','sources':sources([d,[e[0] for e in c.execute('select e.url from evidence e join observation_evidence oe on oe.evidence_id=e.id where oe.observation_id=?',(r['id'],))]]),'sections':[{'label':k.replace('_',' ').title(),'text':display(sd[k]),'status':'source_reported'} for k in ['eligibility','subject_access','entry','language','intake_and_deadline','tuition','caveats','navigation_summary','as_published_facts'] if sd.get(k)],'details':sd})
# Leads remain a separate category, including negative screens, never counted as programmes.
for r in c.execute('select * from leads order by id'):
 d=json.loads(r['raw_json']);d=d if isinstance(d,dict) else {'notes':d};sd=clean(d)
 records.append({'id':'lead-'+r['id'],'kind':'lead','title':first(d,'program','programme','programme_name','title','award','name') or 'Unspecified research lead','institution':first(d,'university','institution'),'country':country(d),'field':first(d,'field','field_group') or 'Unspecified','status':r['disposition'],'checkedAt':date(d),'latestRegional':False,'sources':sources(d),'sections':[{'label':'Research disposition','text':first(sd,'reason','notes','status','rationale'),'status':'unverified'}],'details':sd})
# Mark explicit pure-maths exclusions, without rejecting applied/financial mathematics.
for r in records:
 r['pureMaths']=bool(re.search(r'\bpure math(?:ematic)?s?\b',re.sub(r'not pure mathematics','',r['title']+' '+r['field'],flags=re.I),re.I))
 if r['pureMaths']:r['status']='excluded'
 r['sourceLinkStatus']='linked' if r['sources'] else 'not_resolved_in_scoped_archive'
 if not r['sources']:r['sections'].append({'label':'Source limitation','text':'This archived record retains research notes but no resolved direct official URL in this export. Verify the original institution before relying on it.','status':'unverified'})
counts=dict(collections.Counter(r['kind'] for r in records))
data={'meta':{'schemaVersion':1,'asOf':'2026-10-30','exportedAt':'2026-10-31','counts':counts,'canonicalProgrammeCount':counts['programme'],'candidateObservationCount':counts['candidate'],'leadCount':counts['lead'],'latestRegionalRecordCount':sum(r['latestRegional'] for r in records),'sourceDatabaseSHA256':hashlib.sha256(Path(a.database).read_bytes()).hexdigest(),'caveats':['This is a research archive, not an admissions or eligibility guarantee.','Programme, candidate and lead records are different units; their sum is not a unique programme count. Candidates and leads can overlap or revisit existing awards.','Checked dates are historical source-check dates, not a claim every field was verified then. Unknown dates remain null.','Fees, eligibility and deadlines retain their original cycle and uncertainty. Confirm with the linked institution before applying.','The latest Singapore/Hong Kong batch contains 64 routes; 10 refresh existing programme records and 54 are candidate observations. Independent source spot checks covered 27 main routes, not every field.','Pure mathematics is outside the positive search scope. Excluded leads are retained only to explain screening decisions.','Private evidence captures, source blobs, account information and audit history are not published.'],'sourceScope':'649 canonical programmes, 214 candidate observations, 450 leads from the verified October30 research snapshot. Public research fields only.'},'records':records}
out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
print(json.dumps({'counts':counts,'records':len(records),'bytes':out.stat().st_size,'regional':data['meta']['latestRegionalRecordCount'],'pureMaths':sum(r['pureMaths'] for r in records)},indent=2))
