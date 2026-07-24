#!/usr/bin/env python3
"""
Competitive Intelligence Report Generator
Cozzian Enterprises L.L.C.
Generates formatted HTML report with comparison table, radar chart, gap analysis,
and strategic recommendations. Matplotlib radar chart embedded as base64 PNG.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import base64
import io
from datetime import datetime

# =============================================================================
# EMBEDDED DATASET — Cozzian + 5 Competitors
# =============================================================================
DATASET = {
    "company": "Cozzian Enterprises L.L.C.",
    "company_slug": "cozzian",
    "report_date": datetime.now().strftime("%B %d, %Y"),
    "competitors": [
        {
            "name": "Cozzian Enterprises L.L.C.",
            "url": "cozzian.com",
            "is_self": True,
            "pricing_model": "Custom per-project + value-tier pricing",
            "moq": "50 units (R&D); 500 units (production)",
            "lead_times": "R&D: 2–4 weeks; Production: 6–8 weeks",
            "differentiators": [
                "Full-spectrum formulation: cosmetics, nutraceuticals, pharma, food & bev",
                "In-house regulatory compliance (FDA, EU, ISO 22716)",
                "Rapid prototyping with agile iteration cycles",
                "End-to-end from concept → compliant → market-ready",
                "Sustainability-first ingredient sourcing"
            ],
            "metrics": {
                "formulation_speed": 9.0,
                "production_speed": 7.5,
                "moq_flexibility": 9.5,
                "regulatory_support": 9.0,
                "sustainability": 8.5
            },
            "strengths": ["Broad category expertise", "Fast R&D turnaround", "Strong compliance"],
            "weaknesses": ["Smaller brand recognition vs legacy CMOs", "Narrower production capacity"]
        },
        {
            "name": "Lonza Group",
            "url": "lonza.com",
            "is_self": False,
            "pricing_model": "Premium contract manufacturing; volume-based tiers",
            "moq": "10,000+ units",
            "lead_times": "R&D: 6–12 weeks; Production: 10–16 weeks",
            "differentiators": [
                "Global GMP manufacturing network",
                "Deep biologics & pharma infrastructure",
                "Massive scale (50+ global sites)"
            ],
            "metrics": {
                "formulation_speed": 5.0,
                "production_speed": 9.0,
                "moq_flexibility": 2.0,
                "regulatory_support": 7.0,
                "sustainability": 6.0
            },
            "strengths": ["Global scale & reach", "Deep pharma expertise", "Established brand"],
            "weaknesses": ["Very high MOQ (not startup-friendly)", "Slow R&D iteration", "Premium pricing excludes small brands"]
        },
        {
            "name": "Catalent",
            "url": "catalent.com",
            "is_self": False,
            "pricing_model": "Fee-for-service + milestone-based pricing",
            "moq": "5,000+ units",
            "lead_times": "R&D: 8–14 weeks; Production: 8–12 weeks",
            "differentiators": [
                "Drug delivery tech (Zydis, OptiShell)",
                "Strong biologics & cell/gene therapy",
                "Integrated supply chain solutions"
            ],
            "metrics": {
                "formulation_speed": 4.5,
                "production_speed": 8.0,
                "moq_flexibility": 3.0,
                "regulatory_support": 7.5,
                "sustainability": 5.5
            },
            "strengths": ["Proprietary delivery technologies", "Strong regulatory track record", "Global logistics"],
            "weaknesses": ["Long R&D cycle", "High MOQ barrier", "Pharma-focused — limited cosmetics/food"]
        },
        {
            "name": "Eurofins (Lancaster Labs)",
            "url": "eurofins.com",
            "is_self": False,
            "pricing_model": "Testing fee + hourly consulting; formulation at premium",
            "moq": "1,000+ units (formulation); no MOQ for testing",
            "lead_times": "R&D: 4–8 weeks; Testing: 2–4 weeks",
            "differentiators": [
                "World-class analytical testing & microbiology",
                "Strong cosmetic & pharma testing reputation",
                "Global laboratory network"
            ],
            "metrics": {
                "formulation_speed": 6.5,
                "production_speed": 5.0,
                "moq_flexibility": 6.0,
                "regulatory_support": 8.5,
                "sustainability": 5.0
            },
            "strengths": ["Testing & compliance authority", "Low MOQ for testing services", "Broad geographic presence"],
            "weaknesses": ["Weaker production capabilities", "Formulation is secondary offering", "Testing-centric — not end-to-end"]
        },
        {
            "name": "Alibaba 1688 / Contract Manufacturers",
            "url": "1688.com",
            "is_self": False,
            "pricing_model": "Low per-unit cost; up-front mold/tooling fees",
            "moq": "500–1,000 units (varies by factory)",
            "lead_times": "R&D: 4–8 weeks (sample revisions); Production: 8–14 weeks (incl. shipping)",
            "differentiators": [
                "Rock-bottom unit pricing at high volumes",
                "Massive variety of packaging formats",
                "Direct factory relationships"
            ],
            "metrics": {
                "formulation_speed": 5.5,
                "production_speed": 7.0,
                "moq_flexibility": 7.0,
                "regulatory_support": 2.0,
                "sustainability": 3.0
            },
            "strengths": ["Lowest cost at scale", "Huge packaging library", "Fast high-volume production"],
            "weaknesses": ["Minimal regulatory/compliance support", "Quality inconsistency", "Long shipping lead times", "Language/timezone barriers"]
        },
        {
            "name": "HydraPharm / Boutique Nutra Labs",
            "url": "hydrapharm.com",
            "is_self": False,
            "pricing_model": "Mid-range per-unit; formula development fee + royalty",
            "moq": "200–500 units",
            "lead_times": "R&D: 3–6 weeks; Production: 4–6 weeks",
            "differentiators": [
                "Boutique nutraceutical specialization",
                "Flexible small-batch runs",
                "Personalized customer relationships"
            ],
            "metrics": {
                "formulation_speed": 7.0,
                "production_speed": 6.5,
                "moq_flexibility": 8.5,
                "regulatory_support": 5.5,
                "sustainability": 6.0
            },
            "strengths": ["Startup-friendly MOQ", "Agile turnaround", "Personalized service"],
            "weaknesses": ["Limited to nutraceuticals only", "No in-house pharma/food expertise", "Smaller scale limits cost efficiency at volume"]
        }
    ]
}


def create_radar_chart(competitors):
    """Generate a radar chart comparing competitors on key metrics.
    Returns base64-encoded PNG string."""
    categories = [
        'Formulation\nSpeed',
        'Production\nSpeed',
        'MOQ\nFlexibility',
        'Regulatory\nSupport',
        'Sustainability'
    ]
    metric_keys = ['formulation_speed', 'production_speed', 'moq_flexibility',
                   'regulatory_support', 'sustainability']

    # Sort: Cozzian first, then others
    cozzian = [c for c in competitors if c['is_self']]
    others = [c for c in competitors if not c['is_self']]
    ordered = cozzian + others

    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#f8f9fa')

    # Color palette
    colors = {
        'Cozzian Enterprises L.L.C.': '#2563eb',
        'Lonza Group': '#64748b',
        'Catalent': '#94a3b8',
        'Eurofins (Lancaster Labs)': '#cbd5e1',
        'Alibaba 1688 / Contract Manufacturers': '#f87171',
        'HydraPharm / Boutique Nutra Labs': '#34d399'
    }

    # Plot each competitor
    for comp in ordered:
        name = comp['name']
        values = [comp['metrics'][k] for k in metric_keys]
        values += values[:1]
        color = colors.get(name, '#6b7280')
        linewidth = 3 if comp['is_self'] else 1.5
        alpha = 1.0 if comp['is_self'] else 0.7
        marker = 'o' if comp['is_self'] else ''
        linestyle = '-' if comp['is_self'] else '--'

        ax.plot(angles, values, linestyle, linewidth=linewidth, color=color,
                alpha=alpha, label=name, marker=marker, markersize=8)
        if comp['is_self']:
            ax.fill(angles, values, color=color, alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10, fontweight='bold')
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=8, color='gray')
    ax.set_title('Competitive Intelligence — Key Metrics Radar (Score / 10)',
                 fontsize=14, fontweight='bold', pad=20, color='#1e293b')

    # Grid styling
    ax.grid(True, color='#e2e8f0', linestyle='-', linewidth=0.8)
    ax.spines['polar'].set_color('#e2e8f0')

    legend = ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1),
                       fontsize=9, framealpha=0.9, edgecolor='#e2e8f0')
    legend.get_frame().set_linewidth(0.5)

    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_b64


def generate_comparison_rows(competitors):
    """Build HTML table rows for the comparison table."""
    rows = []
    for comp in competitors:
        name = comp['name']
        if comp['is_self']:
            name = f'<strong>⭐ {name}</strong>'
        diff_html = '<ul class="diff-list">'
        for d in comp['differentiators']:
            diff_html += f'<li>{d}</li>'
        diff_html += '</ul>'

        row_class = 'self-row' if comp['is_self'] else ''
        rows.append(f'''        <tr class="{row_class}">
            <td class="company-cell">{name}</td>
            <td>{comp['pricing_model']}</td>
            <td>{comp['moq']}</td>
            <td>{comp['lead_times']}</td>
            <td class="diff-cell">{diff_html}</td>
        </tr>''')
    return '\n'.join(rows)


def generate_gap_analysis(competitors):
    """Generate gap analysis section — Cozzian's advantages vs each competitor."""
    cozzian = [c for c in competitors if c['is_self']][0]
    others = [c for c in competitors if not c['is_self']]

    sections = []
    for comp in others:
        cozzian_adv = []
        for k in cozzian['metrics']:
            diff = cozzian['metrics'][k] - comp['metrics'][k]
            if diff > 1.0:
                label = k.replace('_', ' ').title()
                cozzian_adv.append(f'{label} (+{diff:.1f})')

        sections.append(f'''
    <div class="gap-card">
        <h3>Cozzian vs. {comp['name']}</h3>
        <div class="gap-grid">
            <div class="gap-adv">
                <h4>✅ Cozzian Advantages</h4>
                <ul>
                    {''.join(f'<li>{a}</li>' for a in cozzian_adv) if cozzian_adv else '<li>Comparable — no decisive advantage</li>'}
                </ul>
            </div>
            <div class="gap-adv competitor-adv">
                <h4>⚠️ {comp['name']} Advantages</h4>
                <ul>
                    {''.join(f'<li>{s}</li>' for s in comp['strengths'])}
                </ul>
            </div>
        </div>
        <p class="gap-insight"><strong>Insight:</strong> {
            _generate_insight(cozzian, comp)
        }</p>
    </div>''')
    return '\n'.join(sections)


def _generate_insight(cozzian, competitor):
    """Generate a specific strategic insight for the gap with a competitor."""
    name = competitor['name']

    if 'Lonza' in name:
        return ("Cozzian outpaces Lonza in formulation speed (+4.0), MOQ flexibility (+7.5), "
                "and sustainability (+2.5). While Lonza dominates in production scale, Cozzian's "
                "low-Moq, agile R&D model is ideal for emerging brands that Lonza's minimums exclude. "
                "Cozzian should position as 'the high-agility alternative to global legacy CMOs.'")
    elif 'Catalent' in name:
        return ("Cozzian leads Catalent in formulation speed (+4.5), MOQ flexibility (+6.5), "
                "and sustainability (+3.0). Catalent's drug-delivery IP is unmatched, but their "
                "8–14 week R&D cycle and 5K+ MOQ is prohibitive for small/mid brands. Cozzian's "
                "cross-category expertise (cosmetics + food + nutra) also gives a unique edge vs. "
                "Catalent's pharma-only focus.")
    elif 'Eurofins' in name:
        return ("Cozzian beats Eurofins in production speed (+2.5), sustainability (+3.5), and "
                "offers true end-to-end service (vs. Eurofins' testing-centric model). However, "
                "Eurofins' regulatory support (8.5) is nearly at par. Cozzian should partner or "
                "cross-refer with Eurofins for third-party testing validation while owning the "
                "formulation-to-production pipeline.")
    elif 'Alibaba' in name or '1688' in name:
        return ("Cozzian utterly dominates in regulatory support (+7.0), formulation speed (+3.5), "
                "and sustainability (+5.5). Alibaba factories win on pure unit cost at scale, but "
                "Co zian's compliant, quality-assured, sustainable process is a premium differentiator "
                "for brands that cannot risk regulatory non-compliance or quality inconsistency. "
                "Market to 'brand-safe formulation sourcing.'")
    elif 'HydraPharm' in name or 'Boutique' in name:
        return ("Cozzian leads in formulation speed (+2.0), production speed (+1.0), regulatory "
                "support (+3.5), and sustainability (+2.5). HydraPharm matches MOQ flexibility but "
                "is confined to nutraceuticals. Cozzian's multi-category capability is a clear "
                "advantage for brands diversifying across cosmetics, food, and supplements. "
                "Position Cozzian as 'the one-stop multi-category formulation partner.'")
    return "Cozzian holds a strong competitive position across multiple dimensions."


def generate_recommendations(competitors):
    """Generate strategic recommendations based on the analysis."""
    recommendations = [
        {
            "title": "1. Own the 'Startup-to-Scale' Positioning",
            "body": (
                "Cozzian's MOQ flexibility (avg 9.5/10) is its #1 competitive differentiator. "
                "No competitor offers R&D batches of 50 units and production runs of 500 units "
                "while maintaining regulatory compliance. Target early-stage CPG, cosmetic, and "
                "nutraceutical brands that have outgrown kitchen-batch but are blocked by "
                "Lonza/Catalent's 5K–10K minimums. Build landing pages, case studies, and ROI "
                "calculators around this 'growth bridge' narrative."
            )
        },
        {
            "title": "2. Double Down on Regulatory-as-a-Service",
            "body": (
                "Cozzian's regulatory support score (9.0) is tied with Eurofins and well ahead of "
                "Alibaba (2.0) and HydraPharm (5.5). Make regulatory compliance a visible, "
                "standalone offering — not a footnote. Publish 'Compliance Guides' (FDA, EU, ISO "
                "22716), offer free compliance audits for new clients, and use this as the wedge "
                "that Alibaba competitors cannot match."
            )
        },
        {
            "title": "3. Cross-Category Expansion Play",
            "body": (
                "Cozzian is the only player with active capability across cosmetics, nutraceuticals, "
                "pharmaceuticals, AND food & beverage. Competitors are siloed: Lonza/Catalent in "
                "pharma, HydraPharm in nutra, Eurofins in testing. Build bundled 'Cross-Category "
                "Launch Packages' that let a brand formulate a supplement, a topical, and a functional "
                "beverage under one project — saving coordination cost and time."
            )
        },
        {
            "title": "4. Sustainability Certification Investment",
            "body": (
                "Cozzian's sustainability score (8.5) is strong but not fully monetized. Pursue "
                "formal certifications (USDA Organic, Ecocert, B Corp, Carbon Neutral certification) "
                "and prominently display them in all sales collateral. This directly counters Alibaba's "
                "weakness (3.0) and matches growing consumer demand for verifiable sustainable sourcing "
                "— allowing Cozzian to charge a sustainability premium."
            )
        },
        {
            "title": "5. Production Speed Improvement Target",
            "body": (
                "At 7.5/10, production speed trails Lonza (9.0) and Catalent (8.0). While Cozzian's "
                "value prop is flexibility and speed of R&D iteration, improving production throughput "
                "by even 15–20% (optimizing batch scheduling, adding partner lab capacity) would make "
                "Cozzian the undisputed leader on 4 of 5 metrics. Consider a lean/Six Sigma initiative "
                "in the production workflow."
            )
        },
        {
            "title": "6. Build a Partner Network for Scale",
            "body": (
                "For clients that outgrow Cozzian's production capacity (e.g., >50K units/month), "
                "establish preferred partnerships with a contract manufacturer (e.g., a mid-tier "
                "co-packer) so clients can 'graduate' without leaving the Cozzian ecosystem. This "
                "retains the client relationship and generates referral fees — turning capacity "
                "limits into a revenue channel rather than a churn risk."
            )
        }
    ]
    return recommendations


def build_html(dataset):
    """Build the full HTML report."""
    competitors = dataset['competitors']
    radar_b64 = create_radar_chart(competitors)
    comparison_rows = generate_comparison_rows(competitors)
    gap_sections = generate_gap_analysis(competitors)
    recommendations = generate_recommendations(competitors)

    rec_html = ''
    for rec in recommendations:
        rec_html += f'''
    <div class="rec-card">
        <h3>{rec['title']}</h3>
        <p>{rec['body']}</p>
    </div>'''

    # Build the report
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Competitive Intelligence Report — {dataset['company']}</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        background: #f1f5f9;
        color: #1e293b;
        line-height: 1.6;
    }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}
    .header {{
        background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 24px rgba(37, 99, 235, 0.2);
    }}
    .header h1 {{ font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem; }}
    .header .subtitle {{ font-size: 1.1rem; opacity: 0.9; }}
    .header .date {{ margin-top: 1rem; font-size: 0.9rem; opacity: 0.7; }}
    .section {{
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}
    .section h2 {{
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e3a5f;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #2563eb;
        display: inline-block;
    }}
    table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        overflow-x: auto;
        display: block;
    }}
    th {{
        background: #1e3a5f;
        color: white;
        padding: 12px 16px;
        text-align: left;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        white-space: nowrap;
    }}
    th:first-child {{ border-radius: 8px 0 0 0; }}
    th:last-child {{ border-radius: 0 8px 0 0; }}
    td {{
        padding: 12px 16px;
        font-size: 0.9rem;
        border-bottom: 1px solid #e2e8f0;
        vertical-align: top;
    }}
    .company-cell {{ font-weight: 600; }}
    .self-row {{ background-color: #eff6ff; }}
    .self-row td {{ border-bottom-color: #bfdbfe; }}
    .diff-cell {{ min-width: 240px; }}
    .diff-list {{ margin: 0; padding-left: 1.2rem; }}
    .diff-list li {{ margin-bottom: 4px; font-size: 0.85rem; }}
    .chart-container {{
        text-align: center;
        margin: 1rem 0;
    }}
    .chart-container img {{
        max-width: 700px;
        width: 100%;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }}
    .gap-card {{
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        transition: box-shadow 0.2s;
    }}
    .gap-card:hover {{ box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
    .gap-card h3 {{
        font-size: 1.1rem;
        color: #1e3a5f;
        margin-bottom: 1rem;
    }}
    .gap-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 1rem;
    }}
    @media (max-width: 768px) {{
        .gap-grid {{ grid-template-columns: 1fr; }}
    }}
    .gap-adv h4 {{
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
        color: #334155;
    }}
    .gap-adv ul {{
        padding-left: 1.2rem;
    }}
    .gap-adv li {{
        font-size: 0.88rem;
        margin-bottom: 0.3rem;
    }}
    .competitor-adv h4 {{ color: #dc2626; }}
    .gap-insight {{
        background: #eff6ff;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        border-left: 4px solid #2563eb;
        font-size: 0.9rem;
        line-height: 1.5;
    }}
    .rec-card {{
        background: linear-gradient(135deg, #f0f9ff 0%, #eff6ff 100%);
        border: 1px solid #bfdbfe;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }}
    .rec-card h3 {{
        font-size: 1.05rem;
        color: #1e3a5f;
        margin-bottom: 0.5rem;
    }}
    .rec-card p {{
        font-size: 0.9rem;
        color: #334155;
        line-height: 1.6;
    }}
    .footer {{
        text-align: center;
        padding: 2rem;
        color: #94a3b8;
        font-size: 0.85rem;
    }}
    .score-badge {{
        display: inline-block;
        background: #dbeafe;
        color: #1e3a5f;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🏢 Competitive Intelligence Report</h1>
        <div class="subtitle">{dataset['company']}</div>
        <div class="date">Generated: {dataset['report_date']}</div>
    </div>

    <div class="section">
        <h2>📊 Company Comparison Table</h2>
        <p style="margin-bottom:1rem;color:#475569;font-size:0.95rem;">
            Side-by-side comparison of Cozzian and key competitors across pricing model,
            minimum order quantities (MOQ), lead times, and core differentiators.
        </p>
        <table>
            <thead>
                <tr>
                    <th>Company</th>
                    <th>Pricing Model</th>
                    <th>MOQ</th>
                    <th>Lead Times</th>
                    <th>Key Differentiators</th>
                </tr>
            </thead>
            <tbody>
{comparison_rows}
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>📈 Radar Chart — Competitive Metric Comparison</h2>
        <p style="margin-bottom:1rem;color:#475569;font-size:0.95rem;">
            Each competitor scored 1–10 across five key dimensions. Cozzian (blue) shown
            with filled area for emphasis.
        </p>
        <div class="chart-container">
            <img src="data:image/png;base64,{radar_b64}"
                 alt="Competitive Intelligence Radar Chart">
        </div>
    </div>

    <div class="section">
        <h2>🔍 Gap Analysis — Cozzian vs. Competitors</h2>
        <p style="margin-bottom:1rem;color:#475569;font-size:0.95rem;">
            Head-to-head analysis identifying where Cozzian holds advantages and where
            competitors pose a threat, with strategic insight for each.
        </p>
        {gap_sections}
    </div>

    <div class="section">
        <h2>🎯 Strategic Recommendations</h2>
        <p style="margin-bottom:1rem;color:#475569;font-size:0.95rem;">
            Six actionable recommendations based on the competitive landscape analysis.
        </p>
        {rec_html}
    </div>

    <div class="footer">
        <p>Confidential — Cozzian Enterprises L.L.C. | Competitive Intelligence Report</p>
        <p style="margin-top:0.3rem;">Generated: {dataset['report_date']} by automated competitive intel pipeline</p>
    </div>
</div>
</body>
</html>'''

    return html


def main():
    """Generate the competitive intel report HTML and save to file."""
    print("=" * 60)
    print("Cozzian Enterprises — Competitive Intelligence Report Generator")
    print("=" * 60)
    print(f"\n📅 Report Date: {DATASET['report_date']}")
    print(f"🏢 Company: {DATASET['company']}")
    print(f"👥 Competitors analyzed: {len(DATASET['competitors'])}")

    print("\n📊 Generating radar chart (Agg/matplotlib)...")
    print("\n🔨 Building HTML report...")
    html_content = build_html(DATASET)

    output_path = 'competitive_intel_report.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    file_size = len(html_content.encode('utf-8'))
    print(f"\n✅ Report saved: {output_path}")
    print(f"   File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print("\n📁 Report sections:")
    print("   1. Company Comparison Table")
    print("   2. Radar Chart (metrics comparison)")
    print("   3. Gap Analysis (Cozzian vs each competitor)")
    print("   4. Strategic Recommendations (6 items)")
    print("\n" + "=" * 60)
    print("✅ Report generation complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()