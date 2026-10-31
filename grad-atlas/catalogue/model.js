export const normalize = value => String(value ?? '').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
export function filterRecords(records, filters, saved = new Set()) {
 const terms = normalize(filters.query).split(/\s+/).filter(Boolean);
 return records.filter(r => {
  if (filters.savedOnly && !saved.has(r.id)) return false;
  if (filters.kind ? r.kind !== filters.kind : r.kind === 'lead' || r.pureMaths) return false;
  if (filters.country && r.country !== filters.country) return false;
  if (filters.field && r.field !== filters.field) return false;
  if (filters.institution && r.institution !== filters.institution) return false;
  if (filters.regional && !/singapore|hong kong/i.test(r.country)) return false;
  if (filters.latest && !r.latestRegional) return false;
  const haystack = r._search ?? normalize([r.title,r.institution,r.country,r.field,JSON.stringify(r.sections),JSON.stringify(r.details)].join(' '));
  return terms.every(t => haystack.includes(t));
 });
}
export function sortRecords(records, key) {
 return [...records].sort((a,b) => {
  if (key === 'recent') return (b.checkedAt || '').localeCompare(a.checkedAt || '') || Number(b.latestRegional)-Number(a.latestRegional) || a.title.localeCompare(b.title);
  return (a[key] || '').localeCompare(b[key] || '') || a.title.localeCompare(b.title);
 });
}
export {safeURL,sourceWarning} from '../model.js?v=sourcesafety1';
export function readSaved(storage) {try {const a=JSON.parse(storage.getItem('grad-atlas-shortlist-v1') || '[]');return new Set(Array.isArray(a)?a.filter(x=>typeof x==='string'):[]);}catch{return new Set();}}
