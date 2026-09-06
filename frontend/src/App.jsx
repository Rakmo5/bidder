import React, { useState, useEffect } from 'react';
import {
  FileText,
  ShieldAlert,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Download,
  Building,
  Scale,
  Eye,
  ArrowRight,
  RefreshCw,
  Award,
  Zap
} from 'lucide-react';

const API_BASE = "http://localhost:8000/api/v1";

export default function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [tender, setTender] = useState(null);
  const [bidders, setBidders] = useState([]);
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [inspectModal, setInspectModal] = useState(null);

  // Load sample data automatically on mount for instant zero-friction demo
  useEffect(() => {
    loadSampleTender();
    loadSampleBidders();
  }, []);

  const loadSampleTender = async () => {
    try {
      setLoading(true);
      const res = await fetch(`${API_BASE}/tenders/sample`);
      const data = await res.json();
      setTender(data);
    } catch (err) {
      console.error("Failed to load sample tender:", err);
    } finally {
      setLoading(false);
    }
  };

  const loadSampleBidders = async () => {
    try {
      setLoading(true);
      const res = await fetch(`${API_BASE}/bidders/sample`);
      const data = await res.json();
      setBidders(data);
    } catch (err) {
      console.error("Failed to load sample bidders:", err);
    } finally {
      setLoading(false);
    }
  };

  const runEvaluation = async () => {
    if (!tender) return;
    try {
      setLoading(true);
      const res = await fetch(`${API_BASE}/evaluate/run?tender_id=${tender.id}`, {
        method: "POST"
      });
      const data = await res.json();
      setEvaluation(data);
      setCurrentStep(3); // Auto transition to results
    } catch (err) {
      console.error("Evaluation error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = () => {
    if (!tender) return;
    window.open(`${API_BASE}/reports/export/${tender.id}`, '_blank');
  };

  return (
    <div>
      {/* Top Govt Color Band */}
      <div className="gov-topbar"></div>

      {/* Header */}
      <header className="header-container">
        <div className="header-brand">
          <div className="gov-emblem-badge">सत्यमेव जयते</div>
          <div className="header-titles">
            <h1>AI Bid Compliance & Procurement Intelligence System</h1>
            <p>Ministry of Petroleum & Natural Gas (MoPNG) | Vigilance & Technical Scrutiny Division</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <span style={{ fontSize: '0.8rem', background: 'rgba(255,255,255,0.2)', padding: '4px 10px', borderRadius: '20px' }}>
            ⚡ CVC & GFR 2017 Mode Active
          </span>
        </div>
      </header>

      {/* Stepper Navigation */}
      <div className="wizard-wrapper">
        <nav className="stepper-nav">
          <div
            className={`step-item ${currentStep === 1 ? 'active' : ''} ${tender ? 'done' : ''}`}
            onClick={() => setCurrentStep(1)}
          >
            <div className="step-num">1</div>
            <div>
              <div className="step-title">Tender Document</div>
              <div className="step-desc">MoPNG Pipeline Criteria & Rules</div>
            </div>
          </div>

          <div
            className={`step-item ${currentStep === 2 ? 'active' : ''} ${bidders.length ? 'done' : ''}`}
            onClick={() => setCurrentStep(2)}
          >
            <div className="step-num">2</div>
            <div>
              <div className="step-title">Bidder Submissions</div>
              <div className="step-desc">{bidders.length} Dossiers Registered</div>
            </div>
          </div>

          <div
            className={`step-item ${currentStep === 3 ? 'active' : ''} ${evaluation ? 'done' : ''}`}
            onClick={() => setCurrentStep(3)}
          >
            <div className="step-num">3</div>
            <div>
              <div className="step-title">Scrutiny & Intelligence</div>
              <div className="step-desc">Compliance, Forensics & QCBS</div>
            </div>
          </div>
        </nav>
      </div>

      {/* Main Content Area */}
      <main className="main-content">
        {/* STEP 1: TENDER REQUIREMENTS */}
        {currentStep === 1 && (
          <div className="gov-card">
            <div className="card-header">
              <h2><FileText size={22} /> Tender Specifications & Mandatory Clauses</h2>
              <button className="btn-action-sample" onClick={loadSampleTender} disabled={loading}>
                <RefreshCw size={16} /> Reload MoPNG Sample Tender
              </button>
            </div>

            {tender && (
              <div>
                <div style={{ background: '#f1f5f9', padding: '1rem', borderRadius: '8px', marginBottom: '1.5rem' }}>
                  <h3 style={{ fontSize: '1.1rem', color: '#123769', marginBottom: '0.25rem' }}>{tender.title}</h3>
                  <div style={{ display: 'flex', gap: '2rem', fontSize: '0.85rem', color: '#475569', marginTop: '0.5rem' }}>
                    <div><strong>Tender Ref:</strong> {tender.tender_ref}</div>
                    <div><strong>Authority:</strong> {tender.issuing_authority}</div>
                    <div><strong>Estimate:</strong> ₹{(tender.estimated_cost_inr / 1e7).toFixed(2)} Crore</div>
                    <div><strong>QCBS Ratio:</strong> {tender.qcbs_ratio} (Quality:Price)</div>
                  </div>
                </div>

                <h4 style={{ marginBottom: '0.75rem', fontWeight: 600 }}>Extracted Scrutiny Matrix ({tender.requirements.length} Criteria):</h4>
                <table className="gov-table">
                  <thead>
                    <tr>
                      <th>Clause Ref</th>
                      <th>Category</th>
                      <th>Parameter</th>
                      <th>Condition / Threshold</th>
                      <th>Mandatory Gate?</th>
                      <th>QCBS Marks</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tender.requirements.map((req) => (
                      <tr key={req.id}>
                        <td><strong>{req.clause_ref}</strong></td>
                        <td>
                          <span style={{ fontSize: '0.75rem', padding: '2px 8px', borderRadius: '4px', background: '#e0f2fe', color: '#0369a1', fontWeight: 600 }}>
                            {req.category}
                          </span>
                        </td>
                        <td>{req.parameter}</td>
                        <td style={{ maxWidth: '350px' }}>{req.threshold}</td>
                        <td>
                          {req.is_mandatory ? (
                            <span style={{ color: '#dc2626', fontWeight: 700 }}>YES (Hard Disqualification)</span>
                          ) : (
                            <span style={{ color: '#64748b' }}>No (Scored Only)</span>
                          )}
                        </td>
                        <td><strong>{req.qcbs_weight} pts</strong></td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                <div style={{ marginTop: '1.5rem', textAlign: 'right' }}>
                  <button className="btn-primary" onClick={() => setCurrentStep(2)}>
                    Proceed to Bidder Dossiers <ArrowRight size={18} />
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* STEP 2: BIDDER SUBMISSIONS */}
        {currentStep === 2 && (
          <div className="gov-card">
            <div className="card-header">
              <h2><Building size={22} /> Competing Bidder Submissions ({bidders.length} Registered)</h2>
              <button className="btn-action-sample" onClick={loadSampleBidders} disabled={loading}>
                <RefreshCw size={16} /> Reset Sample Bidders
              </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1rem' }}>
              {bidders.map((b) => (
                <div key={b.id} style={{ border: '1px solid #cbd5e1', borderRadius: '10px', padding: '1.25rem', background: '#ffffff' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#1e293b' }}>{b.company_name}</h3>
                    <span style={{ fontSize: '0.75rem', background: '#f1f5f9', padding: '2px 8px', borderRadius: '4px' }}>
                      {b.id}
                    </span>
                  </div>

                  <div style={{ marginTop: '0.75rem', fontSize: '0.85rem', lineHeight: 1.8 }}>
                    <div><strong>Quoted Bid Amount:</strong> <span style={{ color: '#0f4c81', fontSize: '1rem', fontWeight: 700 }}>₹{(b.total_bid_amount_inr / 1e7).toFixed(2)} Cr</span></div>
                    <div><strong>Years of Experience:</strong> {b.years_experience} Years</div>
                    <div><strong>Audited 3-Yr Turnover:</strong> ₹{(b.financial_profile.average_turnover_inr / 1e7).toFixed(2)} Cr/yr</div>
                    <div><strong>Statutory CA UDIN:</strong> <code style={{ fontSize: '0.8rem' }}>{b.financial_profile.ca_udin || "Not Provided"}</code></div>
                    <div><strong>Active Certificates:</strong> {b.certificates.map(c => c.name).join(", ") || "None"}</div>
                    {b.documents_metadata[0] && (
                      <div style={{ marginTop: '0.5rem', fontSize: '0.75rem', color: '#64748b' }}>
                        📄 {b.documents_metadata[0].filename} ({b.documents_metadata[0].page_count} pages)
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            <div style={{ marginTop: '2rem', textAlign: 'center', background: '#eff6ff', padding: '1.5rem', borderRadius: '12px' }}>
              <h3 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>Ready for Committee Scrutiny</h3>
              <p style={{ fontSize: '0.9rem', color: '#475569', marginBottom: '1.25rem' }}>
                The AI engine will execute compliance cross-verification, forensic cartel detection, and GFR 2017 QCBS ranking in seconds.
              </p>
              <button className="btn-success" onClick={runEvaluation} disabled={loading}>
                {loading ? <RefreshCw className="animate-spin" size={20} /> : <Zap size={20} />}
                Run Full AI Scrutiny & Forensics
              </button>
            </div>
          </div>
        )}

        {/* STEP 3: RESULTS & INTELLIGENCE */}
        {currentStep === 3 && evaluation && (
          <div>
            {/* Cartel Alert Banner */}
            {evaluation.cartel_alerts.length > 0 && (
              <div className="alert-cartel">
                <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                  <ShieldAlert size={26} color="#dc2626" style={{ flexShrink: 0, marginTop: '2px' }} />
                  <div>
                    <h3 style={{ color: '#991b1b', fontSize: '1.05rem', fontWeight: 700 }}>
                      CRITICAL: Cartelization & Procurement Collusion Signals Detected ({evaluation.cartel_alerts.length})
                    </h3>
                    {evaluation.cartel_alerts.map((alert, idx) => (
                      <div key={idx} style={{ marginTop: '0.5rem', fontSize: '0.88rem', color: '#7f1d1d' }}>
                        <div><strong>Signal:</strong> {alert.signal_name} across bidders: <strong>{alert.bidders_involved.join(" & ")}</strong></div>
                        <div><strong>Forensic Finding:</strong> {alert.forensic_evidence}</div>
                        <div style={{ marginTop: '2px', color: '#b91c1c' }}><strong>Action:</strong> {alert.recommendation}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Abnormally Low Tender (ALT) / Critical Infrastructure Safety Shield */}
            {evaluation.leaderboard.some(e => e.alt_flag) && (
              <div className="alert-alt-risk">
                <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                  <AlertTriangle size={26} color="#d97706" style={{ flexShrink: 0, marginTop: '2px' }} />
                  <div>
                    <h3 style={{ color: '#92400e', fontSize: '1.05rem', fontWeight: 700 }}>
                      Critical Infrastructure Safety Shield — Abnormally Low Tender (ALT) Alert
                    </h3>
                    <p style={{ fontSize: '0.88rem', color: '#78350f', marginTop: '0.25rem' }}>
                      CVC Guidelines Section 5.3: Bids quoted &gt; 20% below engineering benchmark risk contractor abandonment, substandard welding/bitumen, or massive delayed variation claims.
                    </p>
                    {evaluation.leaderboard.filter(e => e.alt_flag).map((e, idx) => (
                      <div key={idx} style={{ marginTop: '0.4rem', fontSize: '0.85rem', color: '#92400e' }}>
                        ⚠️ <strong>{e.company_name}</strong> quoted ₹{(e.financial_quote_inr / 1e7).toFixed(2)} Cr (<strong>{e.alt_discount_pct}% below benchmark</strong>).
                        Predicted 5-year Life-Cycle Failure Risk: ₹{(e.lifecycle_cost_adjusted_inr / 1e7).toFixed(2)} Cr.
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* QCBS Ranked Leaderboard Card */}
            <div className="gov-card">
              <div className="card-header">
                <h2><Award size={22} /> Final QCBS Scrutiny & Contract Recommendation</h2>
                <button className="btn-secondary" onClick={handleDownloadReport}>
                  <Download size={16} /> Export Official Scrutiny Note (.txt)
                </button>
              </div>

              <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', marginBottom: '1rem', fontSize: '0.9rem' }}>
                <strong>Tender Evaluation Committee Recommendation:</strong> {evaluation.recommended_winner || "None (Re-tender recommended)"}
              </div>

              <table className="gov-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Bidder</th>
                    <th>Eligibility Gate</th>
                    <th>Tech Score (Ts)</th>
                    <th>Quoted Price</th>
                    <th>Fin Score (Fs)</th>
                    <th>QCBS Combined</th>
                    <th>Risk Profile</th>
                  </tr>
                </thead>
                <tbody>
                  {evaluation.leaderboard.map((row) => (
                    <tr key={row.bidder_id} style={{ background: row.rank === 1 && row.is_qualified ? '#f0fdf4' : 'inherit' }}>
                      <td>
                        <span style={{ fontWeight: 800, fontSize: '1.1rem', color: row.rank === 1 ? '#15803d' : '#64748b' }}>
                          #{row.rank}
                        </span>
                      </td>
                      <td>
                        <strong>{row.company_name}</strong>
                        {row.rank === 1 && row.is_qualified && (
                          <span style={{ marginLeft: '8px', fontSize: '0.72rem', background: '#dcfce7', color: '#166534', padding: '2px 6px', borderRadius: '4px', fontWeight: 700 }}>
                            RECOMMENDED H1
                          </span>
                        )}
                        {row.disqualification_reason && (
                          <div style={{ fontSize: '0.75rem', color: '#dc2626', marginTop: '2px' }}>
                            {row.disqualification_reason}
                          </div>
                        )}
                      </td>
                      <td>
                        {row.is_qualified ? (
                          <span className="badge-compliant"><CheckCircle size={12} /> QUALIFIED</span>
                        ) : (
                          <span className="badge-rejected"><XCircle size={12} /> DISQUALIFIED</span>
                        )}
                      </td>
                      <td><strong>{row.technical_score_ts} / 100</strong></td>
                      <td>₹{(row.financial_quote_inr / 1e7).toFixed(2)} Cr</td>
                      <td>{row.financial_score_fs > 0 ? `${row.financial_score_fs} pts` : '-'}</td>
                      <td>
                        <strong style={{ fontSize: '1.05rem', color: row.is_qualified ? '#0f4c81' : '#94a3b8' }}>
                          {row.composite_score > 0 ? row.composite_score : 'N/A'}
                        </strong>
                      </td>
                      <td>
                        {row.risk_level === 'LOW' && <span className="badge-compliant">LOW RISK</span>}
                        {row.risk_level === 'ELEVATED' && <span className="badge-warning">ALT ELEVATED</span>}
                        {row.risk_level === 'CRITICAL' && <span className="badge-rejected">CRITICAL RISK</span>}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Compliance Matrix Table with Proof Buttons */}
            <div className="gov-card">
              <div className="card-header">
                <h2><Scale size={22} /> Granular Compliance Matrix & Audit Evidence</h2>
                <span style={{ fontSize: '0.85rem', color: '#64748b' }}>Click any badge to view grounded source evidence</span>
              </div>

              {evaluation.bidder_reports.map((rep) => (
                <div key={rep.bidder_id} style={{ marginBottom: '2rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                    <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#1e293b' }}>
                      {rep.company_name} — Scrutiny Status: {rep.hard_gate_passed ? (
                        <span style={{ color: '#166534' }}>All Mandatory Gates Cleared (Tech: {rep.technical_score_ts}%)</span>
                      ) : (
                        <span style={{ color: '#dc2626' }}>Disqualified on Mandatory Gate</span>
                      )}
                    </h3>
                  </div>

                  <table className="gov-table">
                    <thead>
                      <tr>
                        <th>Tender Requirement</th>
                        <th>Clause Ref</th>
                        <th>Claimed Verification</th>
                        <th>Compliance Status</th>
                        <th>Audit Evidence</th>
                      </tr>
                    </thead>
                    <tbody>
                      {rep.checks.map((check, idx) => (
                        <tr key={idx}>
                          <td><strong>{check.parameter}</strong></td>
                          <td><code>{check.clause_ref}</code></td>
                          <td style={{ fontSize: '0.85rem', maxWidth: '300px' }}>{check.claimed_value}</td>
                          <td>
                            {check.status === 'COMPLIANT' && (
                              <span className="badge-compliant"><CheckCircle size={12} /> Compliant</span>
                            )}
                            {check.status === 'NON_COMPLIANT' && (
                              <span className="badge-rejected"><XCircle size={12} /> Non-Compliant</span>
                            )}
                            {check.status === 'PARTIAL_DISCREPANCY' && (
                              <span className="badge-warning"><AlertTriangle size={12} /> Discrepancy</span>
                            )}
                          </td>
                          <td>
                            <button
                              className="btn-secondary"
                              style={{ padding: '4px 8px', fontSize: '0.78rem' }}
                              onClick={() => setInspectModal({ check, bidderName: rep.company_name })}
                            >
                              <Eye size={13} /> View Proof
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* Side-by-Side Evidence Inspection Modal */}
      {inspectModal && (
        <div className="modal-backdrop" onClick={() => setInspectModal(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #e2e8f0', paddingBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '1.1rem', color: '#123769', fontWeight: 700 }}>
                Audit Proof Inspector — {inspectModal.check.parameter}
              </h3>
              <button
                onClick={() => setInspectModal(null)}
                style={{ background: 'none', border: 'none', fontSize: '1.25rem', cursor: 'pointer', color: '#64748b' }}
              >
                ✕
              </button>
            </div>

            <div style={{ marginTop: '0.75rem', fontSize: '0.85rem', color: '#64748b' }}>
              Bidder: <strong>{inspectModal.bidderName}</strong> | Verification Confidence: <strong>{(inspectModal.check.confidence_score * 100).toFixed(0)}%</strong>
            </div>

            <div className="split-evidence">
              {/* Left Pane: Tender Requirement */}
              <div className="evidence-pane tender">
                <h4>📄 Tender Requirement Clause</h4>
                <div style={{ fontSize: '0.85rem', color: '#1e293b' }}>
                  <strong>Reference:</strong> {inspectModal.check.clause_ref}
                </div>
                <div className="evidence-quote">
                  {inspectModal.check.is_mandatory ? "MANDATORY REQUIREMENT: " : "TECHNICAL CRITERION: "}
                  {inspectModal.check.parameter}
                </div>
                <div style={{ fontSize: '0.8rem', color: '#64748b' }}>
                  Max QCBS Weightage: <strong>{inspectModal.check.technical_marks_max} Marks</strong>
                </div>
              </div>

              {/* Right Pane: Bidder Submission Evidence */}
              <div className={`evidence-pane bidder ${inspectModal.check.status !== 'COMPLIANT' ? 'non-compliant' : ''}`}>
                <h4>📑 Bidder Submitted Proof</h4>
                <div style={{ fontSize: '0.85rem', color: '#1e293b' }}>
                  <strong>Source Document:</strong> {inspectModal.check.evidence_document} (Page {inspectModal.check.evidence_page})
                </div>
                <div className="evidence-quote">
                  "{inspectModal.check.evidence_snippet}"
                </div>
                <div style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>
                  <strong>Status:</strong>{" "}
                  {inspectModal.check.status === 'COMPLIANT' ? (
                    <span style={{ color: '#166534', fontWeight: 700 }}>Verified & Accepted ({inspectModal.check.technical_marks_awarded} Marks)</span>
                  ) : (
                    <span style={{ color: '#dc2626', fontWeight: 700 }}>
                      Rejected: {inspectModal.check.rejection_reason || "Criterion not fulfilled"}
                    </span>
                  )}
                </div>
              </div>
            </div>

            <div style={{ marginTop: '1.5rem', textAlign: 'right' }}>
              <button className="btn-primary" onClick={() => setInspectModal(null)}>
                Close Inspector
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
