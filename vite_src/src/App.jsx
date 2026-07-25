import { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { Beaker, Leaf, ChevronRight, TrendingUp, ShieldCheck, Library, Clock, Menu, X, Bell, LogOut, User, Plus, Search, ArrowUpDown, Check, AlertCircle, BarChart3, Activity } from 'lucide-react';

const BASE = window.__BACKEND_URL__ || '';
async function apiFetch(path, opts = {}) {
  const BASE = window.__BACKEND_URL__ || '';
  for (let i = 0; i < 5; i++) {
    try {
      const r = await fetch(BASE + path, opts);
      if (r.ok) return r.json();
    } catch (_) {}
    await new Promise(r => setTimeout(r, 1500));
  }
  return null;
}

function LandingPage({ onGetStarted, onLogin, onSignup }) {
  const [showMobile, setShowMobile] = useState(false);
  const [scrollY, setScrollY] = useState(0);
  useEffect(() => {
    const s = document.createElement('style');
    s.textContent = `@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'DM Sans', sans-serif; background: #F7F4EF; }
    h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif; }
    .fade-up { opacity: 0; transform: translateY(30px); transition: all 0.6s ease-out; }
    .fade-up.show { opacity: 1; transform: translateY(0); }
    .gradient-text { background: linear-gradient(135deg, #0B3D2E, #C8A96E); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .gold-shimmer { background: linear-gradient(135deg, #C8A96E, #E8D5A3, #C8A96E); background-size: 200% 200%; animation: shimmer 3s ease infinite; }
    @keyframes shimmer { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    @keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
    .float-anim { animation: float 4s ease-in-out infinite; }
    .card-hover { transition: all 0.3s cubic-bezier(0.4,0,0.2,1); }
    .card-hover:hover { transform: translateY(-6px); box-shadow: 0 20px 40px -12px rgba(11,61,46,0.15); }
    `;
    document.head.appendChild(s);
    return () => s.remove();
  }, []);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('show'); });
    }, { threshold: 0.1 });
    document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));
    return () => { window.removeEventListener('scroll', handleScroll); observer.disconnect(); };
  }, []);

  const features = [
    { icon: <Beaker size={24} />, title: 'Formulation Science', desc: 'Expert chemists develop stable, effective formulations using our proprietary database of 200+ validated ingredients.' },
    { icon: <Activity size={24} />, title: 'R&D Prototyping', desc: 'Rapid iteration from concept to physical prototype in under 2 weeks with full sensory and stability testing.' },
    { icon: <ShieldCheck size={24} />, title: 'Compliance-Ready', desc: '99% first-pass compliance rate across FDA, EU, and global regulatory frameworks — no surprises.' },
    { icon: <TrendingUp size={24} />, title: 'Market-Ready Acceleration', desc: 'Scale from lab bench to production floor in 45 days — 30% faster than industry benchmarks.' },
  ];

  const stats = [
    { value: '30%', label: 'Faster time-to-market', color: '#0B3D2E' },
    { value: '99%', label: 'Compliance pass rate', color: '#C8A96E' },
    { value: '200+', label: 'Ingredients in library', color: '#0B3D2E' },
  ];

  return (
    <div className="bg-[#F7F4EF]" style={{ minHeight: '100vh' }}>
      <nav style={{
        position: 'fixed', top: 0, left: 0, right: 0, zIndex: 100,
        background: scrollY > 50 ? 'rgba(247,244,239,0.95)' : 'transparent',
        backdropFilter: scrollY > 50 ? 'blur(12px)' : 'none',
        borderBottom: scrollY > 50 ? '1px solid rgba(11,61,46,0.08)' : '1px solid transparent',
        transition: 'all 0.3s ease'
      }}>
        <div style={{ maxWidth: 1280, margin: '0 auto', padding: '16px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div style={{ width: 40, height: 40, borderRadius: 10, background: 'linear-gradient(135deg, #0B3D2E, #C8A96E)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Beaker size={20} color="#F7F4EF" />
            </div>
            <span style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: 22, fontWeight: 700, color: '#0B3D2E' }}>Cozzian LabSync</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 32 }}>
            <div style={{ display: 'none', gap: 28, '@media (min-width:768px)': { display: 'flex' } }}>
              {['Features', 'Impact', 'Pricing'].map(item => (
                <a key={item} href={`#${item.toLowerCase()}`} style={{ color: '#0B3D2E', textDecoration: 'none', fontSize: 14, fontWeight: 500, opacity: 0.7, transition: 'opacity 0.2s', ':hover': { opacity: 1 } }}>{item}</a>
              ))}
            </div>
            <button onClick={onLogin} style={{
              padding: '10px 24px', borderRadius: 8, border: '1px solid #0B3D2E', background: 'transparent',
              color: '#0B3D2E', fontWeight: 600, fontSize: 14, cursor: 'pointer', transition: 'all 0.2s'
            }} onMouseEnter={e => { e.target.style.background = '#0B3D2E'; e.target.style.color = '#F7F4EF'; }}
            onMouseLeave={e => { e.target.style.background = 'transparent'; e.target.style.color = '#0B3D2E'; }}>Sign in</button>
            <button onClick={() => setShowMobile(!showMobile)} style={{ background: 'none', border: 'none', color: '#0B3D2E', cursor: 'pointer', display: 'none' }}>
              {showMobile ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </nav>

      <section style={{ padding: '140px 24px 80px', maxWidth: 1280, margin: '0 auto' }}>
        <div className="fade-up" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 60, alignItems: 'center' }}>
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, padding: '6px 14px', background: 'rgba(200,169,110,0.15)', borderRadius: 100, marginBottom: 24, border: '1px solid rgba(200,169,110,0.3)' }}>
              <Leaf size={14} color="#C8A96E" />
              <span style={{ color: '#C8A96E', fontSize: 13, fontWeight: 600 }}>Science-led innovation</span>
            </div>
            <h1 style={{ fontSize: 52, fontWeight: 700, color: '#0B3D2E', lineHeight: 1.1, marginBottom: 20 }}>
              From concept to <span className="gradient-text">compliant product</span> in 45 days
            </h1>
            <p style={{ fontSize: 18, color: '#4A5B50', lineHeight: 1.6, marginBottom: 32, maxWidth: 480 }}>
              Expert formulation science and R&D prototyping for cosmetics, nutraceutical, pharmaceutical, and food & beverage brands — turning concepts into compliant, market-ready products.
            </p>
            <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
              <button onClick={onGetStarted} style={{
                padding: '16px 32px', borderRadius: 10, border: 'none', background: '#0B3D2E',
                color: '#F7F4EF', fontWeight: 700, fontSize: 16, cursor: 'pointer',
                transition: 'all 0.3s', display: 'flex', alignItems: 'center', gap: 8
              }}
              onMouseEnter={e => { e.target.style.background = '#C8A96E'; e.target.style.color = '#0B3D2E'; }}
              onMouseLeave={e => { e.target.style.background = '#0B3D2E'; e.target.style.color = '#F7F4EF'; }}>
                Start your project <ChevronRight size={18} />
              </button>
              <button onClick={onLogin} style={{
                padding: '16px 32px', borderRadius: 10, border: '2px solid #0B3D2E', background: 'transparent',
                color: '#0B3D2E', fontWeight: 600, fontSize: 16, cursor: 'pointer', transition: 'all 0.3s'
              }}
              onMouseEnter={e => { e.target.style.borderColor = '#C8A96E'; e.target.style.color = '#C8A96E'; }}
              onMouseLeave={e => { e.target.style.borderColor = '#0B3D2E'; e.target.style.color = '#0B3D2E'; }}>
                See client portal
              </button>
            </div>
          </div>
          <div style={{ position: 'relative', height: 400 }}>
            <div className="float-anim" style={{
              position: 'absolute',
              top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
              width: 320, height: 320, borderRadius: '50%',
              background: 'radial-gradient(circle, rgba(11,61,46,0.08) 0%, rgba(200,169,110,0.05) 100%)',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <div style={{
                width: 240, height: 240, borderRadius: '50%',
                background: 'radial-gradient(circle, rgba(11,61,46,0.12) 0%, rgba(200,169,110,0.08) 100%)',
                display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 8
              }}>
                <div style={{ width: 60, height: 60, borderRadius: 14, background: '#0B3D2E', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Beaker size={30} color="#C8A96E" />
                </div>
                <span style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: 18, fontWeight: 700, color: '#0B3D2E' }}>LabSync</span>
                <span style={{ fontSize: 12, color: '#4A5B50', fontWeight: 500 }}>R&D Accelerator</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="features" style={{ padding: '40px 24px 80px', maxWidth: 1280, margin: '0 auto' }}>
        <div className="fade-up" style={{ textAlign: 'center', marginBottom: 56 }}>
          <span style={{ color: '#C8A96E', fontSize: 14, fontWeight: 600, textTransform: 'uppercase', letterSpacing: 2 }}>Scientific Capabilities</span>
          <h2 style={{ fontSize: 38, fontWeight: 700, color: '#0B3D2E', marginTop: 12 }}>End-to-end formulation expertise</h2>
          <p style={{ color: '#4A5B50', fontSize: 16, marginTop: 12, maxWidth: 600, margin: '12px auto 0' }}>Four integrated pillars of R&D excellence that compress your development timeline.</p>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(270px, 1fr))', gap: 24 }}>
          {(features || []).map((f, i) => (
            <div key={i} className="card-hover" style={{
              padding: 28, borderRadius: 14, background: '#fff',
              border: '1px solid rgba(11,61,46,0.08)',
              transition: 'all 0.3s'
            }}>
              <div style={{ width: 44, height: 44, borderRadius: 10, background: 'rgba(11,61,46,0.08)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#0B3D2E', marginBottom: 16 }}>
                {f.icon}
              </div>
              <h3 style={{ fontSize: 18, fontWeight: 600, color: '#0B3D2E', marginBottom: 8 }}>{f.title}</h3>
              <p style={{ color: '#4A5B50', fontSize: 14, lineHeight: 1.6 }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section style={{ padding: '60px 24px', background: '#0B3D2E' }}>
        <div style={{ maxWidth: 1280, margin: '0 auto' }}>
          <div className="fade-up" style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 40 }}>
            {(stats || []).map((s, i) => (
              <div key={i} style={{ textAlign: 'center' }}>
                <div style={{ fontSize: 52, fontWeight: 700, fontFamily: "'Space Grotesk', sans-serif", color: '#C8A96E', marginBottom: 8 }}>{s.value}</div>
                <div style={{ fontSize: 15, color: 'rgba(247,244,239,0.8)', fontWeight: 500 }}>{s.label}</div>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 40, textAlign: 'center' }}>
            <button onClick={onGetStarted} style={{
              padding: '14px 28px', borderRadius: 10, border: 'none', background: '#C8A96E',
              color: '#0B3D2E', fontWeight: 700, fontSize: 15, cursor: 'pointer',
              transition: 'all 0.3s'
            }}
            onMouseEnter={e => { e.target.style.background = '#F7F4EF'; e.target.style.color = '#0B3D2E'; }}
            onMouseLeave={e => { e.target.style.background = '#C8A96E'; e.target.style.color = '#0B3D2E'; }}>
              Accelerate your R&D — Get started
            </button>
          </div>
        </div>
      </section>

      <section id="pricing" style={{ padding: '80px 24px', maxWidth: 1280, margin: '0 auto' }}>
        <div className="fade-up" style={{ textAlign: 'center', marginBottom: 48 }}>
          <span style={{ color: '#C8A96E', fontSize: 14, fontWeight: 600, textTransform: 'uppercase', letterSpacing: 2 }}>Transparent pricing</span>
          <h2 style={{ fontSize: 38, fontWeight: 700, color: '#0B3D2E', marginTop: 12 }}>Plans that scale with your pipeline</h2>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 24 }}>
          {[
            { name: 'Starter', price: '$499', desc: 'For emerging brands testing their first concepts', features: ['2 active projects', 'Basic ingredient library', 'Formulation templates', 'Email support'] },
            { name: 'Professional', price: '$1,299', desc: 'For growing brands with multiple active projects', features: ['10 active projects', 'Full ingredient library', 'Compliance reports', 'Priority support', 'API access'] },
            { name: 'Enterprise', price: 'Custom', desc: 'For established brands requiring dedicated support', features: ['Unlimited projects', 'Dedicated formulation scientist', 'Custom ingredient sourcing', 'Regulatory consulting', 'White-label reports'] }
          ].map((tier, i) => (
            <div key={i} className="card-hover" style={{
              padding: 32, borderRadius: 14, background: i === 1 ? '#0B3D2E' : '#fff',
              border: i === 1 ? 'none' : '1px solid rgba(11,61,46,0.08)',
              position: 'relative'
            }}>
              {i === 1 && <div style={{ position: 'absolute', top: -12, left: '50%', transform: 'translateX(-50%)', background: '#C8A96E', color: '#0B3D2E', padding: '4px 16px', borderRadius: 100, fontSize: 12, fontWeight: 700 }}>Most popular</div>}
              <h3 style={{ fontSize: 20, fontWeight: 600, color: i === 1 ? '#F7F4EF' : '#0B3D2E', marginBottom: 6 }}>{tier.name}</h3>
              <p style={{ color: i === 1 ? 'rgba(247,244,239,0.7)' : '#4A5B50', fontSize: 14, marginBottom: 20 }}>{tier.desc}</p>
              <div style={{ fontSize: 40, fontWeight: 700, fontFamily: "'Space Grotesk', sans-serif", color: i === 1 ? '#C8A96E' : '#0B3D2E', marginBottom: 4 }}>{tier.price}<span style={{ fontSize: 16, fontWeight: 400 }}>{tier.price !== 'Custom' ? '/mo' : ''}</span></div>
              <div style={{ margin: '24px 0', borderTop: `1px solid ${i === 1 ? 'rgba(247,244,239,0.15)' : 'rgba(11,61,46,0.08)'}`, paddingTop: 20 }}>
                {tier.features.map((f, j) => (
                  <div key={j} style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 12, color: i === 1 ? 'rgba(247,244,239,0.8)' : '#4A5B50', fontSize: 14 }}>
                    <Check size={16} color={i === 1 ? '#C8A96E' : '#0B3D2E'} />
                    {f}
                  </div>
                ))}
              </div>
              <button onClick={onGetStarted} style={{
                width: '100%', padding: '14px', borderRadius: 10, border: 'none',
                background: i === 1 ? '#C8A96E' : '#0B3D2E',
                color: i === 1 ? '#0B3D2E' : '#F7F4EF', fontWeight: 700, fontSize: 15, cursor: 'pointer',
                transition: 'all 0.3s'
              }}
              onMouseEnter={e => { e.target.style.background = i === 1 ? '#F7F4EF' : '#C8A96E'; e.target.style.color = '#0B3D2E'; }}
              onMouseLeave={e => { e.target.style.background = i === 1 ? '#C8A96E' : '#0B3D2E'; e.target.style.color = i === 1 ? '#0B3D2E' : '#F7F4EF'; }}>
                {tier.price === 'Custom' ? 'Contact sales' : 'Start free trial'}
              </button>
            </div>
          ))}
        </div>
      </section>

      <footer style={{ background: '#0B3D2E', padding: '40px 24px 24px' }}>
        <div style={{ maxWidth: 1280, margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 20 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <Beaker size={20} color="#C8A96E" />
            <span style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: 18, fontWeight: 700, color: '#F7F4EF' }}>Cozzian LabSync</span>
          </div>
          <div style={{ display: 'flex', gap: 24 }}>
            {['Terms', 'Privacy', 'Contact'].map(l => (
              <span key={l} style={{ color: 'rgba(247,244,239,0.6)', fontSize: 13, cursor: 'pointer', transition: 'color 0.2s', ':hover': { color: '#C8A96E' } }}>{l}</span>
            ))}
          </div>
          <span style={{ color: 'rgba(247,244,239,0.4)', fontSize: 13 }}>© 2025 Cozzian Enterprises L.L.C.</span>
        </div>
      </footer>
    </div>
  );
}

function ProductApp({ user, onLogout }) {
  /* NC_PLACEHOLDER_DASHBOARD — replaced by the real dashboard in Phase 2 */
  return (
    <div style={{ minHeight: '100vh', background: '#0a0d18', color: '#e6eaf2', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 16, padding: 24, textAlign: 'center' }}>
      <h1 style={{ fontSize: 28, fontWeight: 800, margin: 0 }}>Welcome, {user?.name || user?.email || 'there'} 👋</h1>
      <p style={{ color: '#9aa6bd', maxWidth: 460, lineHeight: 1.5, margin: 0 }}>Your account is ready. Your dashboard is being set up and will appear here shortly.</p>
      <button onClick={onLogout} style={{ marginTop: 8, padding: '10px 18px', borderRadius: 10, border: '1px solid #2a3350', background: 'transparent', color: '#e6eaf2', fontWeight: 600, cursor: 'pointer' }}>Log out</button>
    </div>
  );
}

function AuthGate({ onAuth, onClose }) {
  const [mode, setMode] = useState('signup');
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const _ip = { width: '100%', padding: '11px 13px', margin: '6px 0', borderRadius: 9, border: '1px solid #2a3350', background: '#0b1020', color: '#e6eaf2', fontSize: 14, outline: 'none', boxSizing: 'border-box' };
  const submit = async (e) => {
    e.preventDefault();
    if (!form.email || !form.password) return;
    if (mode === 'signup') {
      const pw = form.password;
      if (pw.length < 8 || !/[A-Z]/.test(pw) || !/\d/.test(pw)) {
        setPasswordError('Password must be at least 8 characters, include an uppercase letter, and a digit.');
        setLoading(false); return;
      } else { setPasswordError(''); }
    }
    setLoading(true); setError('');
    const _b = window.__NC_BASE__ || ''; const _s = window.__COMPANY_SLUG__ || '';
    const body = JSON.stringify({ email: form.email, password: form.password, name: form.name });
    const _call = () => fetch(`${_b}/api/c/${_s}/auth/${mode}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body });
    try {
      let res; try { res = await _call(); } catch { await new Promise(r => setTimeout(r, 2500)); res = await _call(); }
      const json = await res.json();
      if (!json.ok) { setError(json.error || 'Authentication failed — please try again'); setLoading(false); return; }
      onAuth(json);
    } catch { setError('Connection error — please try again in a moment.'); setLoading(false); }
  };
  return (
    <div onClick={onClose} style={{ position: 'fixed', inset: 0, background: 'rgba(2,6,18,.7)', backdropFilter: 'blur(4px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
      <form onClick={(e) => e.stopPropagation()} onSubmit={submit} style={{ background: '#0f1424', border: '1px solid #232b45', padding: 28, borderRadius: 16, width: 360, maxWidth: '90vw', color: '#e6eaf2' }}>
        <h3 style={{ margin: '0 0 16px', fontSize: 20, fontWeight: 700 }}>{mode === 'signup' ? 'Create your account' : 'Welcome back'}</h3>
        {mode === 'signup' && <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Your name" style={_ip} />}
        <input value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} placeholder="Work email" type="email" required style={_ip} />
        <input value={form.password} onChange={(e) => { setForm({ ...form, password: e.target.value }); setPasswordError(''); }} placeholder="Password" type="password" required style={_ip} />
        {passwordError && <p style={{ color: '#fbbf24', fontSize: 12, margin: '2px 0 0', textAlign: 'left' }}>{passwordError}</p>}
        {error && <p style={{ color: '#f87171', fontSize: 13, margin: '6px 0 0' }}>{error}</p>}
        <button type="submit" disabled={loading} style={{ width: '100%', marginTop: 10, padding: '12px', borderRadius: 9, border: 'none', background: loading ? '#4b50b8' : '#6366f1', color: '#fff', fontWeight: 700, fontSize: 15, cursor: loading ? 'default' : 'pointer' }}>
          {loading ? '…' : mode === 'signup' ? 'Get started free' : 'Log in'}
        </button>
        <p onClick={() => { setMode(mode === 'signup' ? 'login' : 'signup'); setError(''); }} style={{ marginTop: 14, fontSize: 13, color: '#9aa6bd', cursor: 'pointer', textAlign: 'center' }}>
          {mode === 'signup' ? 'Already have an account? Log in' : 'New here? Create an account'}
        </p>
      </form>
    </div>
  );
}

function App() {
  const [auth, setAuth] = useState(() => {
    try {
      if (localStorage.getItem('nc_user') && !localStorage.getItem('nc_auth')) localStorage.removeItem('nc_user');
      const a = JSON.parse(localStorage.getItem('nc_auth') || 'null');
      return (a && a.token && a.user && typeof a.user.email === 'string') ? a : null;
    } catch { return null; }
  });
  const [showAuth, setShowAuth] = useState(false);
  useEffect(() => {
    if (!auth?.token) return;
    const _b = window.__NC_BASE__ || ''; const _s = window.__COMPANY_SLUG__ || '';
    fetch(`${_b}/api/c/${_s}/auth/me`, { headers: { Authorization: `Bearer ${auth.token}` } })
      .then(r => r.json()).then(d => { if (!d.ok) { localStorage.removeItem('nc_auth'); setAuth(null); } }).catch(() => {});
  }, []);
  const onAuth = (data) => { localStorage.setItem('nc_auth', JSON.stringify(data)); setAuth(data); setShowAuth(false); };
  const onLogout = () => { localStorage.removeItem('nc_auth'); setAuth(null); };
  if (auth?.user) return <ProductApp user={auth.user} token={auth.token} onLogout={onLogout} />;
  return (
    <>
      <LandingPage onGetStarted={() => setShowAuth(true)} onSignup={() => setShowAuth(true)} onLogin={() => setShowAuth(true)} />
      {/* Fallback entry point (bottom-right so it never overlaps the nav) — guarantees a
          working login even if the landing's own buttons aren't wired to the auth modal. */}
      <button onClick={() => setShowAuth(true)} style={{ position: 'fixed', bottom: 20, right: 20, zIndex: 999, background: '#6366f1', color: '#fff', border: 'none', padding: '10px 18px', borderRadius: 999, fontWeight: 600, fontSize: 14, cursor: 'pointer', boxShadow: '0 6px 20px rgba(99,102,241,.45)' }}>Sign in</button>
      {showAuth && <AuthGate onAuth={onAuth} onClose={() => setShowAuth(false)} />}
    </>
  );
}

export default App;
