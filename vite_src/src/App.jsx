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
    <div style={{ minHeight: '100vh', background: '#0b0a1a' }}>
      <nav style={{
        position: 'fixed', top: 0, left: 0, right: 0, zIndex: 100,
        background: scrollY > 50 ? 'rgba(11,10,26,0.95)' : 'transparent',
        backdropFilter: scrollY > 50 ? 'blur(12px)' : 'none',
        borderBottom: scrollY > 50 ? '1px solid rgba(139,92,246,0.2)' : '1px solid transparent',
        transition: 'all 0.3s ease'
      }}>
        <div style={{ maxWidth: 1280, margin: '0 auto', padding: '16px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div style={{ width: 40, height: 40, borderRadius: 10, background: 'linear-gradient(135deg, #7c3aed, #3b82f6)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Beaker size={20} color="#ffffff" />
            </div>
            <span style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: 22, fontWeight: 700, color: '#e0e7ff' }}>Cozzian LabSync</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 32 }}>
            <div style={{ display: 'none', gap: 28, '@media (min-width:768px)': { display: 'flex' } }}>
              {['Features', 'Impact', 'Pricing'].map(item => (
                <a key={item} href={`#${item.toLowerCase()}`} style={{ color: '#c4b5fd', textDecoration: 'none', fontSize: 14, fontWeight: 500, opacity: 0.8, transition: 'opacity 0.2s', ':hover': { opacity: 1 } }}>{item}</a>
              ))}
            </div>
            <button onClick={onLogin} style={{
              padding: '10px 24px', borderRadius: 8, border: '1px solid #7c3aed', background: 'transparent',
              color: '#c4b5fd', fontWeight: 600, fontSize: 14, cursor: 'pointer', transition: 'all 0.2s'
            }} onMouseEnter={e => { e.target.style.background = '#7c3aed'; e.target.style.color = '#ffffff'; }}
            onMouseLeave={e => { e.target.style.background = 'transparent'; e.target.style.color = '#c4b5fd'; }}>Sign in</button>
            <button onClick={() => setShowMobile(!showMobile)} style={{ background: 'none', border: 'none', color: '#e0e7ff', cursor: 'pointer', display: 'none' }}>
              {showMobile ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </nav>

      <section style={{ padding: '140px 24px 80px', maxWidth: 1280, margin: '0 auto' }}>
        <div className="fade-up" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 60, alignItems: 'center' }}>
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, padding: '6px 14px', background: 'rgba(124,58,237,0.15)', borderRadius: 100, marginBottom: 24, border: '1px solid rgba(124,58,237,0.3)' }}>
              <Leaf size={14} color="#a78bfa" />
              <span style={{ color: '#a78bfa', fontSize: 13, fontWeight: 600 }}>Science-led innovation</span>
            </div>
            <h1 style={{ fontSize: 52, fontWeight: 700, color: '#e0e7ff', lineHeight: 1.1, marginBottom: 20 }}>
              From concept to <span style={{ background: 'linear-gradient(135deg, #7c3aed, #3b82f6)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>compliant product</span> in 45 days
            </h1>
            <p style={{ fontSize: 18, color: '#a5b4fc', lineHeight: 1.6, marginBottom: 32, maxWidth: 480 }}>
              Expert formulation science and R&D prototyping for cosmetics, nutraceutical, pharmaceutical, and food & beverage brands — turning concepts into compliant, market-ready products.
            </p>
            <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
              <button onClick={onGetStarted} style={{
                padding: '16px 32px', borderRadius: 10, border: 'none', background: '#7c3aed',
                color: '#ffffff', fontWeight: 700, fontSize: 16, cursor: 'pointer',
                transition: 'all 0.3s', display: 'flex', alignItems: 'center', gap: 8
              }}
              onMouseEnter={e => { e.target.style.background = '#3b82f6'; e.target.style.color = '#ffffff'; }}
              onMouseLeave={e => { e.target.style.background = '#7c3aed'; e.target.style.color = '#ffffff'; }}>
                Start your project <ChevronRight size={18} />
              </button>
              <button onClick={onLogin} style={{
                padding: '16px 32px', borderRadius: 10, border: '2px solid #7c3aed', background: 'transparent',
                color: '#a78bfa', fontWeight: 600, fontSize: 16, cursor: 'pointer', transition: 'all 0.3s'
              }}
              onMouseEnter={e => { e.target.style.borderColor = '#3b82f6'; e.target.style.color = '#3b82f6'; }}
              onMouseLeave={e => { e.target.style.borderColor = '#7c3aed'; e.target.style.color = '#a78bfa'; }}>
                See client portal
              </button>
            </div>
          </div>
          <div style={{ position: 'relative', height: 400 }}>
            <div className="float-anim" style={{
              position: 'absolute',
              top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
              width: 320, height: 320, borderRadius: '50%',
              background: 'radial-gradient(circle, rgba(124,58,237,0.08) 0%, rgba(59,130,246,0.05) 100%)',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <div style={{
                width: 240, height: 240, borderRadius: '50%',
                background: 'radial-gradient(circle, rgba(124,58,237,0.12) 0%, rgba(59,130,246,0.08) 100%)',
                display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 8
              }}>
                <div style={{ width: 60, height: 60, borderRadius: 14, background: '#7c3aed', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Beaker size={30} color="#a78bfa" />
                </div>
                <span style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: 18, fontWeight: 700, color: '#e0e7ff' }}>LabSync</span>
                <span style={{ fontSize: 12, color: '#a5b4fc', fontWeight: 500 }}>R&D Accelerator</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="features" style={{ padding: '40px 24px 80px', maxWidth: 1280, margin: '0 auto' }}>
        <div className="fade-up" style={{ textAlign: 'center', marginBottom: 56 }}>
          <span style={{ color: '#a78bfa', fontSize: 14, fontWeight: 600, textTransform: 'uppercase', letterSpacing: 2 }}>Scientific Capabilities</span>
          <h2 style={{ fontSize: 38, fontWeight: 700, color: '#e0e7ff', marginTop: 12 }}>End-to-end formulation expertise</h2>
          <p style={{ color: '#a5b4fc', fontSize: 16, marginTop: 12, maxWidth: 600, margin: '12px auto 0' }}>Four integrated pillars of R&D excellence that compress your development timeline.</p>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(270px, 1fr))', gap: 24 }}>
          {(features || []).map((f, i) => (
            <div key={i} className="card-hover" style={{
              padding: 28, borderRadius: 14, background: '#12122a',
              border: '1px solid #1e1e3a',
              transition: 'all 0.3s'
            }}>
              <div style={{ width: 44, height: 44, borderRadius: 10, background: 'rgba(124,58,237,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#a78bfa', marginBottom: 16 }}>
                {f.icon}
              </div>
              <h3 style={{ fontSize: 18, fontWeight: 600, color: '#e0e7ff', marginBottom: 8 }}>{f.title}</h3>
              <p style={{ color: '#a5b4fc', fontSize: 14, lineHeight: 1.6 }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section style={{ padding: '60px 24px', background: 'linear-gradient(135deg, #7c3aed, #3b82f6)' }}>
        <div style={{ maxWidth: 1280, margin: '0 auto' }}>
          <div className="fade-up" style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 40 }}>
            {(stats || []).map((s, i) => (
              <div key={i} style={{ textAlign: 'center' }}>
                <div style={{ fontSize: 52, fontWeight: 700, fontFamily: "'Space Grotesk', sans-serif", color: '#ffffff', marginBottom: 8 }}>{s.value}</div>
                <div style={{ fontSize: 15, color: 'rgba(255,255,255,0.8)', fontWeight: 500 }}>{s.label}</div>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 40, textAlign: 'center' }}>
            <button onClick={onGetStarted} style={{
              padding: '14px 28px', borderRadius: 10, border: 'none', background: '#ffffff',
              color: '#7c3aed', fontWeight: 700, fontSize: 15, cursor: 'pointer',
              transition: 'all 0.3s'
            }}
            onMouseEnter={e => { e.target.style.background = '#e0e7ff'; e.target.style.color = '#7c3aed'; }}
            onMouseLeave={e => { e.target.style.background = '#ffffff'; e.target.style.color = '#7c3aed'; }}>
              Accelerate your R&D — Get started
            </button>
          </div>
        </div>
      </section>

      {/* Competitive advantage section — from competitive intel analysis */}
      <section id="why-cozzian" style={{ padding: '80px 24px', maxWidth: 1280, margin: '0 auto' }}>
        <div className="fade-up" style={{ textAlign: 'center', marginBottom: 56 }}>
          <span style={{ color: '#a78bfa', fontSize: 14, fontWeight: 600, textTransform: 'uppercase', letterSpacing: 2 }}>Why Cozzian</span>
          <h2 style={{ fontSize: 38, fontWeight: 700, color: '#e0e7ff', marginTop: 12 }}>Outpacing the competition</h2>
          <p style={{ color: '#a5b4fc', fontSize: 16, marginTop: 12, maxWidth: 600, margin: '12px auto 0' }}>
            Three advantages no other contract manufacturer can match — proven by competitive intelligence.
          </p>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 24 }}>
          {[
            {
              icon: <TrendingUp size={24} />,
              title: 'Startup-to-Scale MOQ Bridge',
              stat: '50&rarr;500',
              statLabel: 'R&D to production units',
              highlights: [
                '50-unit R&D batches — the industry\'s lowest minimum',
                '500-unit production runs — no manufacturer swap needed',
                'Lonza demands 10K+ units; Catalent demands 5K+',
                'Full FDA/EU compliance from batch one, not an upsell'
              ]
            },
            {
              icon: <ShieldCheck size={24} />,
              title: 'Speed &times; Compliance',
              stat: '99%',
              statLabel: 'First-pass compliance rate',
              highlights: [
                '2–4 week R&D turnaround with compliance baked in',
                'Alibaba: cheap units but 2/10 regulatory score — costly rejections',
                'Avg reformulation cost after failed customs: $5K–$15K',
                'Cozzian: 9/10 formulation speed + 9/10 regulatory support'
              ]
            },
            {
              icon: <Activity size={24} />,
              title: 'One-Stop Cross-Category',
              stat: '4',
              statLabel: 'Categories under one roof',
              highlights: [
                'Cosmetics, nutraceuticals, pharma, food & beverage',
                'HydraPharm: nutra only. Lonza: pharma only.',
                'Bundle a serum, supplement & functional beverage — one partner',
                'Save 40% on coordination vs using separate manufacturers'
              ]
            }
          ].map((item, i) => (
            <div key={i} className="card-hover" style={{
              padding: 28, borderRadius: 14, background: '#12122a',
              border: '1px solid #1e1e3a',
              transition: 'all 0.3s'
            }}>
              <div style={{ width: 44, height: 44, borderRadius: 10, background: 'rgba(124,58,237,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#a78bfa', marginBottom: 16 }}>
                {item.icon}
              </div>
              <h3 style={{ fontSize: 18, fontWeight: 600, color: '#e0e7ff', marginBottom: 4 }}>{item.title}</h3>
              <div style={{ fontSize: 36, fontWeight: 700, fontFamily: "'Space Grotesk', sans-serif", color: '#a78bfa', marginTop: 8, marginBottom: 2 }}>{item.stat}</div>
              <div style={{ color: '#a5b4fc', fontSize: 12, marginBottom: 16, letterSpacing: 0.5 }}>{item.statLabel}</div>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                {(item.highlights || []).map((h, j) => (
                  <li key={j} style={{
                    display: 'flex', alignItems: 'flex-start', gap: 8, marginBottom: 10,
                    color: '#a5b4fc', fontSize: 13, lineHeight: 1.5
                  }}>
                    <span style={{ color: '#7c3aed', marginTop: 2, flexShrink: 0 }}>&#9656;</span>
                    {h}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div style={{ textAlign: 'center', marginTop: 40 }}>
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: 8,
            padding: '10px 20px', background: 'rgba(124,58,237,0.1)',
            borderRadius: 10, border: '1px solid rgba(124,58,237,0.2)'
          }}>
            <span style={{ color: '#a5b4fc', fontSize: 13 }}>
              &#128202; Based on competitive intelligence analysis vs Lonza, Catalent, Eurofins, Alibaba &amp; HydraPharm
            </span>
          </div>
        </div>
      </section>

      <section id="pricing" style={{ padding: '80px 24px', maxWidth: 1280, margin: '0 auto' }}>
        <div className="fade-up" style={{ textAlign: 'center', marginBottom: 48 }}>
          <span style={{ color: '#a78bfa', fontSize: 14, fontWeight: 600, textTransform: 'uppercase', letterSpacing: 2 }}>Transparent pricing</span>
          <h2 style={{ fontSize: 38, fontWeight: 700, color: '#e0e7ff', marginTop: 12 }}>Plans that scale with your pipeline</h2>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 24 }}>
          {[
            { name: 'Starter', price: '$499', desc: 'For emerging brands testing their first concepts', features: ['2 active projects', 'Basic ingredient library', 'Formulation templates', 'Email support'] },
            { name: 'Professional', price: '$1,299', desc: 'For growing brands with multiple active projects', features: ['10 active projects', 'Full ingredient library', 'Compliance reports', 'Priority support', 'API access'] },
            { name: 'Enterprise', price: 'Custom', desc: 'For established brands requiring dedicated support', features: ['Unlimited projects', 'Dedicated formulation scientist', 'Custom ingredient sourcing', 'Regulatory consulting', 'White-label reports'] }
          ].map((tier, i) => (
            <div key={i} className="card-hover" style={{
              padding: 32, borderRadius: 14, background: i === 1 ? '#1e1e3a' : '#12122a',
              border: '1px solid rgba(124,58,237,0.2)',
              position: 'relative'
            }}>
              {i === 1 && <div style={{ position: 'absolute', top: -12, left: '50%', transform: 'translateX(-50%)', background: '#7c3aed', color: '#ffffff', padding: '4px 16px', borderRadius: 100, fontSize: 12, fontWeight: 700 }}>Most popular</div>}
              <h3 style={{ fontSize: 20, fontWeight: 600, color: '#e0e7ff', marginBottom: 6 }}>{tier.name}</h3>
              <p style={{ color: '#a5b4fc', fontSize: 14, marginBottom: 20 }}>{tier.desc}</p>
              <div style={{ fontSize: 40, fontWeight: 700, fontFamily: "'Space Grotesk', sans-serif", color: '#a78bfa', marginBottom: 4 }}>{tier.price}<span style={{ fontSize: 16, fontWeight: 400 }}>{tier.price !== 'Custom' ? '/mo' : ''}</span></div>
              <div style={{ margin: '24px 0', borderTop: '1px solid rgba(124,58,237,0.15)', paddingTop: 20 }}>
                {tier.features.map((f, j) => (
                  <div key={j} style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 12, color: '#a5b4fc', fontSize: 14 }}>
                    <Check size={16} color="#7c3aed" />
                    {f}
                  </div>
                ))}
              </div>
              <button onClick={onGetStarted} style={{
                width: '100%', padding: '14px', borderRadius: 10, border: 'none',
                background: i === 1 ? '#7c3aed' : '#7c3aed',
                color: '#ffffff', fontWeight: 700, fontSize: 15, cursor: 'pointer',
                transition: 'all 0.3s'
              }}
              onMouseEnter={e => { e.target.style.background = '#3b82f6'; e.target.style.color = '#ffffff'; }}
              onMouseLeave={e => { e.target.style.background = '#7c3aed'; e.target.style.color = '#ffffff'; }}>
                {tier.price === 'Custom' ? 'Contact sales' : 'Start free trial'}
              </button>
            </div>
          ))}
        </div>
      </section>

      <footer style={{ background: '#0d0d24', padding: '40px 24px 24px', borderTop: '1px solid rgba(124,58,237,0.2)' }}>
        <div style={{ maxWidth: 1280, margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 20 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <Beaker size={20} color="#a78bfa" />
            <span style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: 18, fontWeight: 700, color: '#e0e7ff' }}>Cozzian LabSync</span>
          </div>
          <div style={{ display: 'flex', gap: 24 }}>
            {['Terms', 'Privacy', 'Contact'].map(l => (
              <span key={l} style={{ color: 'rgba(165,180,252,0.6)', fontSize: 13, cursor: 'pointer', transition: 'color 0.2s', ':hover': { color: '#a78bfa' } }}>{l}</span>
            ))}
          </div>
          <span style={{ color: 'rgba(165,180,252,0.4)', fontSize: 13 }}>© 2025 Cozzian Enterprises L.L.C.</span>
        </div>
      </footer>
    </div>
  );
}

function ProductApp({ user, onLogout }) {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const BASE = window.__BACKEND_URL__ || 'http://localhost:8000';
    fetch(BASE + '/api/projects')
      .then(r => r.json())
      .then(data => setProjects(data?.projects ?? data ?? []))
      .catch(() => setProjects([]))
      .finally(() => setLoading(false));
  }, []);

  const projectList = (projects ?? []).map(p => (
    <div key={p.id} style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '14px 18px', background: '#12172b', borderRadius: 10,
      border: '1px solid #1e2740', marginBottom: 10
    }}>
      <div>
        <div style={{ fontWeight: 600, color: '#e6eaf2' }}>{p.name || 'Untitled'}</div>
        <div style={{ fontSize: 13, color: '#9aa6bd', marginTop: 4 }}>Status: {p.status || 'draft'}</div>
      </div>
      <a href={'/projects/' + p.id} style={{
        color: '#C8A96E', textDecoration: 'none', fontSize: 14, fontWeight: 600
      }}>View Details →</a>
    </div>
  ));

  return (
    <div style={{ minHeight: '100vh', background: '#0a0d18', color: '#e6eaf2', padding: 24 }}>
      <div style={{ maxWidth: 720, margin: '0 auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
          <h1 style={{ fontSize: 24, fontWeight: 800, margin: 0 }}>Welcome, {user?.name || user?.email || 'there'} 👋</h1>
          <button onClick={onLogout} style={{ padding: '8px 16px', borderRadius: 10, border: '1px solid #2a3350', background: 'transparent', color: '#e6eaf2', fontWeight: 600, cursor: 'pointer', fontSize: 13 }}>Log out</button>
        </div>
        <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 16, color: '#C8A96E' }}>Projects</h2>
        {loading ? (
          <p style={{ color: '#9aa6bd' }}>Loading projects...</p>
        ) : projectList.length === 0 ? (
          <p style={{ color: '#9aa6bd' }}>No projects yet.</p>
        ) : (
          projectList
        )}
      </div>
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
