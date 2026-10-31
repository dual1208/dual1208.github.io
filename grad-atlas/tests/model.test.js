import test from 'node:test';import assert from 'node:assert/strict';import {validDate,exactDate,windowState,endpoint,adapt,filterRows,sortRows,coverage,safeURL,dateTypeLabel,splitScopeCoverage,deadlineMeaning}from '../model.js';
const now=new Date('2026-10-31T12:00:00Z');const w={start_date:'2026-10-01',start_status:'exact',end_date:'2027-02-28',end_status:'exact',window_type:'application'};const p={id:'x',title:'Programme',country:'Singapore',field:'Hardware',classification:'programme',record_kinds:['programme'],windows:[w],requirements:[]};
test('strict dates reject impossible days',()=>{assert.equal(validDate('2027-02-29'),false);assert.equal(validDate('2028-02-29'),true);});
test('annual date never promoted exact',()=>assert.equal(exactDate({...w,end_status:'annual'},'end'),null));
test('unknown endpoint conspicuous',()=>assert.equal(endpoint({end_status:'not_verified'},'end').primary,'NOT VERIFIED'));
test('no opening does not claim open',()=>assert.equal(windowState({...w,start_status:'not_verified'},now).key,'upcoming'));
test('rolling does not claim always open',()=>assert.match(windowState({end_status:'rolling'},now).label,/confirm/));
test('deadline today is not assumed closed at midnight',()=>assert.equal(windowState({...w,end_date:'2026-10-31'},now).key,'today'));
test('past deadline labelled',()=>assert.equal(windowState({...w,end_date:'2026-10-30'},now).key,'closed'));
test('unknown programme retains row',()=>assert.equal(adapt({programmes:[{...p,windows:[]}]}).length,1));
test('all rounds kept',()=>assert.equal(adapt({programmes:[{...p,windows:[w,w]}]}).length,2));
test('leads excluded by default and available in archive',()=>{const rows=adapt({programmes:[p,{...p,id:'lead',classification:'research_lead'}]});assert.equal(filterRows(rows,{scope:'programmes'},now).length,1);assert.equal(filterRows(rows,{scope:'all'},now).length,2);});
test('requirements filter honest',()=>assert.equal(filterRows(adapt({programmes:[p]}),{requirements:'verified'},now).length,0));
test('programme coverage not window count',()=>{const c=coverage(adapt({programmes:[{...p,windows:[w,w]}]}));assert.equal(c.programmes,1);assert.equal(c.windows,2);});
test('safe URLs exclude scripts',()=>assert.equal(safeURL('javascript:alert(1)'),null));
test('upcoming exact deadline sorts before missing and past',()=>{const a=adapt({programmes:[p,{...p,id:'missing',windows:[]},{...p,id:'past',windows:[{...w,end_date:'2026-01-01'}]}]});assert.deepEqual(sortRows(a,'end',now).map(r=>r.programme.id),['x','missing','past']);});
test('not offered overrides future date status',()=>assert.equal(windowState({...w,availability_status:'not_offered'},now).key,'unavailable'));

test('non-application event labels cannot say application',()=>{assert.equal(dateTypeLabel('scholarship'),'Scholarship');assert.equal(dateTypeLabel('supporting_documents'),'Supporting documents');});
test('programme coverage excludes research leads and supplemental event rows',()=>{const rows=adapt({programmes:[{...p,windows:[w,{...w,window_type:'scholarship'}]},{...p,id:'lead',classification:'research_lead',windows:[w]}]});const c=splitScopeCoverage(rows);assert.equal(c.positive.programmes,1);assert.equal(c.positive.windows,1);assert.equal(c.leadIdentities,1);});

test('database download explicitly names lossless gzip format',async()=>{const {readFile}=await import('node:fs/promises');const html=await readFile(new URL('../index.html',import.meta.url),'utf8');assert.match(html,/href="data\/programmes\.sqlite\.gz" download>Download database \(\.sqlite\.gz\)/);});

test('unspecified end never asserts final closure',()=>{assert.match(deadlineMeaning(w).label,/closure not confirmed/);assert.doesNotMatch(windowState(w,now).label,/Open|closed/);});
test('priority funding recommendation remain scoped before and after date',()=>{for(const [meaning,word] of [['priority_consideration','priority'],['funding_consideration','funding'],['recommended_submission','recommended']]){const a={...w,deadline_semantics:meaning};assert.match(deadlineMeaning(a).label,/not.*closure/i);assert.ok(windowState(a,now).label.includes(word));assert.ok(windowState({...a,end_date:'2026-10-30'},now).label.includes(word));assert.ok(windowState({...a,end_date:'2026-10-31'},now).label.includes(word));}});
test('round deadline does not imply final intake closure',()=>assert.match(deadlineMeaning({...w,deadline_semantics:'round_deadline'}).label,/later rounds may exist/));
test('only explicit final closure labelled final',()=>assert.equal(deadlineMeaning({...w,deadline_semantics:'final_closure'}).label,'Final application closure'));
test('document and scholarship deadlines remain contextual',()=>{assert.match(deadlineMeaning({...w,deadline_semantics:'document_deadline'}).label,/documents/);assert.match(deadlineMeaning({...w,deadline_semantics:'scholarship_deadline'}).label,/Scholarship/);});
