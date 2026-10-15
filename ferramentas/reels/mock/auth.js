const claims = () => (window.__FF_CLAIMS || {});
const user = { uid: 'demo-uid', isAnonymous: false, email: 'demo@loja.modelo',
  getIdToken: async () => 'demo-token', getIdTokenResult: async () => ({ claims: claims(), token: 'demo-token' }) };
const auth = { currentUser: user };
export const getAuth = () => auth;
export const onAuthStateChanged = (a, cb) => { setTimeout(() => cb(auth.currentUser), 0); return () => {}; };
export const signInAnonymously = async () => ({ user });
export const signInWithEmailAndPassword = async () => ({ user });
export const signInWithCustomToken = async () => ({ user });
export const createUserWithEmailAndPassword = async () => ({ user });
export const signOut = async () => {};
export const updatePassword = async () => {};
