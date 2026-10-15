// Firestore em memória para a demonstração do FORTÍS FLOW (dados fictícios).
const STORE = (window.__FF_DB = window.__FF_DB || new Map()); // path -> objeto
const LISTENERS = new Set();
let autoN = 0;
const clone = (o) => (o === undefined ? undefined : JSON.parse(JSON.stringify(o)));

let __loaded=false;
if (window.__FF_PERSIST) { try { const raw = localStorage.getItem('ff_mock_db'); if (raw) { for (const [p, d] of JSON.parse(raw)) STORE.set(p, d); __loaded = true; window.__FF_SEEDED = true; } } catch (e) {} }
if (!__loaded && window.__FF_SEED && !window.__FF_SEEDED) {
  for (const [p, d] of Object.entries(window.__FF_SEED)) STORE.set(p, d);
  window.__FF_SEEDED = true;
}

class Sentinel { constructor(kind, v) { this.kind = kind; this.v = v; } }
export const serverTimestamp = () => new Sentinel('ts');
export const deleteField = () => new Sentinel('del');
export const arrayUnion = (...v) => new Sentinel('union', v);
export const arrayRemove = (...v) => new Sentinel('remove', v);
export const increment = (n) => new Sentinel('inc', n);

export class Timestamp {
  constructor(s, ns) { this.seconds = s; this.nanoseconds = ns || 0; }
  static now() { return Timestamp.fromDate(new Date()); }
  static fromDate(d) { return new Timestamp(Math.floor(d.getTime() / 1000), 0); }
  static fromMillis(m) { return new Timestamp(Math.floor(m / 1000), 0); }
  toDate() { return new Date(this.seconds * 1000); }
  toMillis() { return this.seconds * 1000; }
}

const join = (parts) => parts.filter((x) => x !== undefined && x !== null && x !== '').join('/');
function baseOf(x) { return x && x.__path !== undefined ? x.__path : ''; }

export function collection(parent, ...segs) {
  const path = join([baseOf(parent), ...segs]);
  return { __type: 'col', __path: path, id: path.split('/').pop(), path };
}
export function collectionGroup(db, id) { return { __type: 'group', __group: id, __path: '' }; }
export function doc(parent, ...segs) {
  let path;
  if (parent && parent.__type === 'col' && segs.length === 0) path = parent.__path + '/' + 'demo' + Date.now().toString(36) + (autoN++);
  else path = join([baseOf(parent), ...segs]);
  const parts = path.split('/');
  return { __type: 'doc', __path: path, id: parts[parts.length - 1], path, parent: { __type: 'col', __path: parts.slice(0, -1).join('/'), id: parts[parts.length - 2] } };
}

function getField(o, f) {
  if (f === '__name__') return o.__id;
  return f.split('.').reduce((a, k) => (a == null ? undefined : a[k]), o);
}
function applyValue(cur, v) {
  if (v instanceof Sentinel) {
    if (v.kind === 'ts') return new Date().toISOString();
    if (v.kind === 'union') { const a = Array.isArray(cur) ? cur.slice() : []; v.v.forEach((x) => { if (!a.some((y) => JSON.stringify(y) === JSON.stringify(x))) a.push(x); }); return a; }
    if (v.kind === 'remove') { const a = Array.isArray(cur) ? cur : []; return a.filter((y) => !v.v.some((x) => JSON.stringify(x) === JSON.stringify(y))); }
    if (v.kind === 'inc') return (Number(cur) || 0) + v.v;
  }
  if (v instanceof Timestamp) return v.toDate().toISOString();
  if (v && typeof v === 'object' && !Array.isArray(v)) {
    const o = {}; for (const [k, x] of Object.entries(v)) { if (x instanceof Sentinel && x.kind === 'del') continue; o[k] = applyValue(cur ? cur[k] : undefined, x); } return o;
  }
  if (Array.isArray(v)) return v.map((x) => applyValue(undefined, x));
  return v;
}
function setPath(o, f, v) {
  const ks = f.split('.'); let t = o;
  for (let i = 0; i < ks.length - 1; i++) { if (typeof t[ks[i]] !== 'object' || t[ks[i]] === null) t[ks[i]] = {}; t = t[ks[i]]; }
  const last = ks[ks.length - 1];
  if (v instanceof Sentinel && v.kind === 'del') delete t[last]; else t[last] = applyValue(t[last], v);
}

class DocSnap {
  constructor(ref, data) { this.ref = ref; this.id = ref.id; this._d = data; this.metadata = { fromCache: false, hasPendingWrites: false }; }
  exists() { return this._d !== undefined; }
  data() { return clone(this._d); }
  get(f) { return this._d ? getField(this._d, f) : undefined; }
}
export const DocumentSnapshot = DocSnap;
class QuerySnap {
  constructor(docs) { this.docs = docs; this.size = docs.length; this.empty = docs.length === 0; this.metadata = { fromCache: false, hasPendingWrites: false }; }
  forEach(fn) { this.docs.forEach(fn); }
  docChanges() { return this.docs.map((d) => ({ type: 'added', doc: d })); }
}

export const where = (f, op, v) => ({ k: 'where', f: typeof f === 'object' ? '__name__' : f, op, v });
export const orderBy = (f, dir) => ({ k: 'order', f, dir: dir || 'asc' });
export const limit = (n) => ({ k: 'limit', n });
export const limitToLast = (n) => ({ k: 'limit', n });
export const startAfter = () => ({ k: 'noop' });
export const documentId = () => ({ __docId: true });
export function query(ref, ...cs) { return { __type: 'query', __base: ref, __cs: [...(ref.__cs || []), ...cs], __path: ref.__path }; }

function cmp(a, b) { if (a === b) return 0; if (a === undefined) return -1; if (b === undefined) return 1; return a < b ? -1 : 1; }
function match(o, c) {
  const x = getField(o, c.f), v = c.v;
  switch (c.op) {
    case '==': return x === v; case '!=': return x !== v && x !== undefined;
    case '<': return x < v; case '<=': return x <= v; case '>': return x > v; case '>=': return x >= v;
    case 'in': return Array.isArray(v) && v.includes(x); case 'not-in': return Array.isArray(v) && !v.includes(x);
    case 'array-contains': return Array.isArray(x) && x.includes(v);
    case 'array-contains-any': return Array.isArray(x) && x.some((y) => v.includes(y));
  }
  return true;
}
function runQuery(q) {
  const base = q.__type === 'query' ? q.__base : q; const cs = q.__cs || [];
  let rows = [];
  for (const [p, d] of STORE) {
    const parts = p.split('/');
    const ok = base.__type === 'group' ? parts.length >= 2 && parts[parts.length - 2] === base.__group && parts.length % 2 === 0
      : parts.slice(0, -1).join('/') === base.__path;
    if (ok) rows.push({ p, d: { ...d, __id: parts[parts.length - 1] } });
  }
  for (const c of cs) if (c.k === 'where') rows = rows.filter((r) => match(r.d, c));
  const orders = cs.filter((c) => c.k === 'order');
  if (orders.length) rows.sort((a, b) => { for (const o of orders) { const r = cmp(getField(a.d, o.f), getField(b.d, o.f)); if (r) return o.dir === 'desc' ? -r : r; } return 0; });
  const lim = cs.find((c) => c.k === 'limit'); if (lim) rows = rows.slice(0, lim.n);
  return new QuerySnap(rows.map((r) => { const { __id, ...d } = r.d; return new DocSnap(doc({ __path: '' }, r.p), d); }));
}
function persist() { if (window.__FF_PERSIST) try { localStorage.setItem('ff_mock_db', JSON.stringify([...STORE])); } catch (e) {} }
function notify() { persist(); for (const l of LISTENERS) { try { l(); } catch (e) { console.error('mock listener', e); } } }

export async function getDoc(ref) { return new DocSnap(ref, clone(STORE.get(ref.__path))); }
export const getDocFromCache = getDoc, getDocFromServer = getDoc;
export async function getDocs(q) { return runQuery(q); }
export async function getDocsFromCache(q) { return runQuery(q); }
export const getDocsFromServer = getDocs;
export async function setDoc(ref, data, opts) {
  const cur = opts && opts.merge ? clone(STORE.get(ref.__path)) || {} : {};
  for (const [k, v] of Object.entries(data)) setPath(cur, k, v);
  STORE.set(ref.__path, cur); notify();
}
export async function addDoc(col, data) { const r = doc(col); await setDoc(r, data); return r; }
export async function updateDoc(ref, a, ...rest) {
  const cur = clone(STORE.get(ref.__path)); if (!cur) throw new Error('No document to update: ' + ref.__path);
  const data = typeof a === 'string' ? Object.fromEntries([[a, rest[0]], ...rest.slice(1).reduce((acc, x, i, arr) => (i % 2 ? acc : [...acc, [x, arr[i + 1]]]), [])]) : a;
  for (const [k, v] of Object.entries(data)) setPath(cur, k, v);
  STORE.set(ref.__path, cur); notify();
}
export async function deleteDoc(ref) { STORE.delete(ref.__path); notify(); }
export function onSnapshot(ref, ...args) {
  const opts = args[0] && typeof args[0] === 'object' && !args[0].next && typeof args[0] !== 'function' ? args.shift() : null;
  let next = args[0], err = args[1];
  if (next && typeof next === 'object') { err = next.error; next = next.next; }
  const fire = () => { try { next(ref.__type === 'doc' ? new DocSnap(ref, clone(STORE.get(ref.__path))) : runQuery(ref)); } catch (e) { console.error('onSnapshot cb', e); } };
  const l = () => setTimeout(fire, 0); LISTENERS.add(l); setTimeout(fire, 0);
  return () => LISTENERS.delete(l);
}
export async function runTransaction(db, fn) {
  const tx = { get: getDoc, set: (r, d, o) => { setDoc(r, d, o); return tx; }, update: (r, d) => { updateDoc(r, d); return tx; }, delete: (r) => { deleteDoc(r); return tx; } };
  return fn(tx);
}
export function writeBatch() {
  const ops = []; const b = { set: (r, d, o) => (ops.push(() => setDoc(r, d, o)), b), update: (r, d) => (ops.push(() => updateDoc(r, d)), b), delete: (r) => (ops.push(() => deleteDoc(r)), b), commit: async () => { for (const o of ops) await o(); } };
  return b;
}
export async function getCountFromServer(q) { const s = runQuery(q); return { data: () => ({ count: s.size }) }; }
export const getFirestore = () => ({ __path: '' });
export const initializeFirestore = () => ({ __path: '' });
export const persistentLocalCache = () => ({});
export const persistentMultipleTabManager = () => ({});
export const enableNetwork = async () => {}; export const disableNetwork = async () => {};
export const waitForPendingWrites = async () => {};
export const enableIndexedDbPersistence = async () => {};
