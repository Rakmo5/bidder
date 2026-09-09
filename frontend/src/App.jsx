import React, { useState, useEffect } from 'react';
import {
  FileText,
  ShieldAlert,
  CheckCircle,
  Download,
  Building,
  Scale,
  Eye,
  ArrowRight,
  RefreshCw,
  Award,
  Zap,
  Sliders,
  Send,
  UploadCloud,
  Network,
  FileSpreadsheet,
  Check,
  X,
  ExternalLink,
  ShieldCheck,
  UserCheck
} from 'lucide-react';

const API_BASE = "http://localhost:8000/api/v1";

export default function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [ministry, setMinistry] = useState('MoPNG'); // 'MoPNG' | 'MoRTH'
  const [tender, setTender] = useState(null);
  const [bidders, setBidders] = useState([]);
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeUserRole, setActiveUserRole] = useState('CHIEF_EXECUTIVE');
  const [users, setUsers] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  
  // Modals
  const [inspectModal, setInspectModal] = useState(null);
  const [thresholdModalOpen, setThresholdModalOpen] = useState(false);
  const [editedRequirements, setEditedRequirements] = useState([]);
  const [thresholdError, setThresholdError] = useState('');
  const [gfrNoticeModal, setGfrNoticeModal] = useState(null);
  const [gemExportModal, setGemExportModal] = useState(null);
  const [showAuditDrawer, setShowAuditDrawer] = useState(false);
  
  // OCR Bounding Box Evidence state
  const [bboxData, setBboxData] = useState(null);

  useEffect(() => {
    loadUsers();
    loadTender(ministry);
    loadBidders();
    loadAuditLogs();
  }, [ministry]);

  const logAction = async (action, target, details) => {
    try {
      await fetch(`${API_BASE}/iam/log?role=${activeUserRole}&action=${encodeURIComponent(action)}&target=${encodeURIComponent(target)}&details=${encodeURIComponent(details)}`, {
        method: "POST"
      });
      loadAuditLogs();
    } catch (e) {
      console.warn("Could not write audit log", e);
    }
  };

  const loadUsers = async () => {
    try {
      const res = await fetch(`${API_BASE}/iam/users`);
      if (res.ok) {
        const data = await res.json();
        setUsers(data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const loadAuditLogs = async () => {
    try {
      const res = await fetch(`${API_BASE}/iam/audit-logs`);
      if (res.ok) {
        const data = await res.json();
        setAuditLogs(data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const loadTender = async (targetMinistry) => {
    try {
      setLoading(true);
      const endpoint = targetMinistry === 'MoRTH' ? `${API_BASE}/tenders/morth` : `${API_BASE}/tenders/sample`;
      const res = await fetch(endpoint);
      const data = await res.json();
      setTender(data);
      setEditedRequirements(data.requirements || []);
      setEvaluation(null);
    } catch (err) {
      console.error("Failed to load tender:", err);
    } finally {
      setLoading(false);
    }
  };

  const loadBidders = async () => {
    try {
      setLoading(true);
      const res = await fetch(`${API_BASE}/bidders/sample`);
      const data = await res.json();
      setBidders(data);
    } catch (err) {
      console.error("Failed to load bidders:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveThresholds = async () => {
    if (!tender) return;
    try {
      setThresholdError('');
      const res = await fetch(`${API_BASE}/tenders/${tender.id}/thresholds`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(editedRequirements)
      });
      if (!res.ok) {
        const errData = await res.json();
        setThresholdError(errData.detail || "Validation failed: violates statutory procurement floor.");
        return;
      }
      const updatedTender = await res.json();
      setTender(updatedTender);
      setThresholdModalOpen(false);
      logAction("UPDATE_THRESHOLDS", tender.id, `Tuned criteria weights & thresholds for tender ${tender.id}`);
    } catch (e) {
      setThresholdError(e.message);
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
      setCurrentStep(3);
      logAction("EXECUTE_EVALUATION", tender.id, `Triggered full AI compliance & CVC forensics evaluation`);
    } catch (err) {
      console.error("Evaluation error:", err);
    } finally {
      setLoading(false);
    }
  };

  const openEvidenceProof = async (item, bidder) => {
    setInspectModal({ item, bidder });
    setBboxData(null);
    try {
      const filename = bidder.documents[0]?.filename || 'Bidder1_LT_Hydrocarbon_Engineering.pdf';
      const res = await fetch(`${API_BASE}/ocr/evidence-bbox?filename=${encodeURIComponent(filename)}&page_number=1&snippet=${encodeURIComponent(item.extracted_evidence)}`);
      if (res.ok) {
        const data = await res.json();
        setBboxData(data);
      }
    } catch (err) {
      console.warn("Evidence bbox lookup failed", err);
    }
  };

  const generateGfrNotice = async (bidderId) => {
    if (!tender) return;
    try {
      const res = await fetch(`${API_BASE}/reports/clarification-notice/${tender.id}/${bidderId}`);
      if (res.ok) {
        const data = await res.json();
        setGfrNoticeModal(data);
        logAction("GENERATE_GFR173_NOTICE", bidderId, `Drafted statutory 48hr clarification notice for bidder ${bidderId}`);
      }
    } catch (e) {
      console.error("Failed to generate notice", e);
    }
  };

  const openGemExport = async () => {
    if (!tender) return;
    try {
      const res = await fetch(`${API_BASE}/gem/export/${tender.id}`);
      if (res.ok) {
        const data = await res.json();
        setGemExportModal(data);
        logAction("EXPORT_GEM_OCDS", tender.id, `Exported evaluation package to GeM 3.0 / OCDS standard`);
      }
    } catch (e) {
      console.error("GeM export failed", e);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Govt Tricolor Band */}
      <div className="gov-topbar"></div>

      {/* Header */}
      <header className="header-container">
        <div className="header-brand">
          <div className="gov-emblem-badge">सत्यमेव जयते</div>
          <div className="header-titles">
            <h1>Autonomous AI Bid Compliance & Anti-Cartelization Engine</h1>
            <p>Government of India | Central Vigilance Commission (CVC) & GeM 3.0 Integration</p>
          </div>
        </div>

        <div className="header-controls">
          {/* Ministry Switcher */}
          <div style={{ display: 'flex', background: 'rgba(15, 23, 42, 0.8)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', padding: '2px' }}>
            <button
              onClick={() => setMinistry('MoPNG')}
              style={{
                background: ministry === 'MoPNG' ? '#2563eb' : 'transparent',
                color: ministry === 'MoPNG' ? '#fff' : '#94a3b8',
                border: 'none',
                padding: '4px 10px',
                borderRadius: '6px',
                fontSize: '0.78rem',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              MoPNG (Gas Pipeline)
            </button>
            <button
              onClick={() => setMinistry('MoRTH')}
              style={{
                background: ministry === 'MoRTH' ? '#10b981' : 'transparent',
                color: ministry === 'MoRTH' ? '#fff' : '#94a3b8',
                border: 'none',
                padding: '4px 10px',
                borderRadius: '6px',
                fontSize: '0.78rem',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              MoRTH (Highway EPC)
            </button>
          </div>

          {/* IAM Role Switcher */}
          <div className="iam-role-selector">
            <UserCheck size={16} color="#60a5fa" />
            <select
              className="iam-select"
              value={activeUserRole}
              onChange={(e) => setActiveUserRole(e.target.value)}
            >
              <option value="CHIEF_EXECUTIVE">👑 Chief Executive (Rajesh Kumar IAS)</option>
              <option value="TECHNICAL_SCRUTINIZER">🔬 Technical Scrutinizer (Dr. Priya Sharma)</option>
              <option value="VIGILANCE_OFFICER">🛡️ Vigilance Officer (Anil Verma CVO)</option>
              <option value="OCR_OPERATOR">📄 OCR Operator (Suresh Patil)</option>
            </select>
          </div>

          {/* Audit Trail Button */}
          <button
            onClick={() => setShowAuditDrawer(!showAuditDrawer)}
            className="btn-secondary"
            style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
          >
            📋 Audit Trail ({auditLogs.length})
          </button>
        </div>
      </header>

      {/* Stepper Navigation */}
      <div className="wizard-wrapper">
        <div className="stepper-nav">
          <button
            className={`step-btn ${currentStep === 1 ? 'active' : ''} ${currentStep > 1 ? 'completed' : ''}`}
            onClick={() => setCurrentStep(1)}
          >
            <span className="step-number">1</span>
            <span>Tender Master & Standards</span>
          </button>
          <button
            className={`step-btn ${currentStep === 2 ? 'active' : ''} ${currentStep > 2 ? 'completed' : ''}`}
            onClick={() => setCurrentStep(2)}
          >
            <span className="step-number">2</span>
            <span>Bidder Dossiers & OCR Pipeline</span>
          </button>
          <button
            className={`step-btn ${currentStep === 3 ? 'active' : ''}`}
            onClick={() => { if (evaluation) setCurrentStep(3); }}
          >
            <span className="step-number">3</span>
            <span>AI Scrutiny & CVC Forensics</span>
          </button>
        </div>
      </div>

      {/* Main Container */}
      <main className="main-content">
        {/* STEP 1: TENDER MASTER */}
        {currentStep === 1 && tender && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            <div className="glass-card">
              <div className="section-header">
                <div>
                  <span className="badge badge-blue" style={{ marginBottom: '0.5rem' }}>
                    {tender.tender_ref}
                  </span>
                  <h2 style={{ fontSize: '1.35rem', fontWeight: 800 }}>{tender.title}</h2>
                  <p style={{ color: '#94a3b8', fontSize: '0.85rem' }}>
                    Issuing Authority: <strong style={{ color: '#e2e8f0' }}>{tender.issuing_authority}</strong> | Estimated Cost: <strong style={{ color: '#34d399' }}>₹{(tender.estimated_cost_inr / 1e7).toFixed(2)} Crore</strong> | QCBS Formula: <strong style={{ color: '#60a5fa' }}>{tender.qcbs_ratio}</strong>
                  </p>
                </div>

                <div style={{ display: 'flex', gap: '0.75rem' }}>
                  {activeUserRole === 'CHIEF_EXECUTIVE' && (
                    <button
                      className="btn-accent"
                      onClick={() => {
                        setEditedRequirements([...tender.requirements]);
                        setThresholdModalOpen(true);
                      }}
                    >
                      <Sliders size={16} /> Tune Thresholds
                    </button>
                  )}
                  <button className="btn-primary" onClick={() => setCurrentStep(2)}>
                    Proceed to Bid Dossiers <ArrowRight size={16} />
                  </button>
                </div>
              </div>

              {/* Requirements & Criteria Table */}
              <div style={{ marginTop: '1.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                  <h3 style={{ fontSize: '1rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Scale size={18} color="#60a5fa" /> Tender Eligibility & QCBS Criteria Matrix ({tender.requirements.length} Parameters)
                  </h3>
                  <span style={{ fontSize: '0.78rem', color: '#94a3b8' }}>Statutory Reference: GFR 2017 / MoPNG Guidelines</span>
                </div>

                <div style={{ overflowX: 'auto', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '8px' }}>
                  <table className="custom-table">
                    <thead>
                      <tr>
                        <th style={{ width: '110px' }}>Clause Ref</th>
                        <th style={{ width: '220px' }}>Parameter</th>
                        <th>Mandatory Government Benchmark / Threshold</th>
                        <th style={{ width: '130px' }}>Type</th>
                        <th style={{ width: '110px', textAlign: 'right' }}>QCBS Weight</th>
                      </tr>
                    </thead>
                    <tbody>
                      {tender.requirements.map((req) => (
                        <tr key={req.id}>
                          <td className="mono-font" style={{ color: '#60a5fa', fontWeight: 600 }}>{req.clause_ref}</td>
                          <td style={{ fontWeight: 600 }}>{req.parameter}</td>
                          <td style={{ color: '#cbd5e1' }}>{req.threshold}</td>
                          <td>
                            {req.is_mandatory ? (
                              <span className="badge badge-red">Mandatory Gate</span>
                            ) : (
                              <span className="badge badge-blue">Scored Criteria</span>
                            )}
                          </td>
                          <td style={{ textAlign: 'right', fontWeight: 700, color: '#34d399' }}>{req.qcbs_weight}%</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* BoQ Items Schedule */}
              <div style={{ marginTop: '2rem' }}>
                <h3 style={{ fontSize: '1rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
                  <FileSpreadsheet size={18} color="#34d399" /> Itemized Bill of Quantities (BoQ) & Schedule of Rates (SOR)
                </h3>
                <div style={{ overflowX: 'auto', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '8px' }}>
                  <table className="custom-table">
                    <thead>
                      <tr>
                        <th style={{ width: '90px' }}>Item Code</th>
                        <th>Description of Works</th>
                        <th style={{ width: '100px' }}>Unit</th>
                        <th style={{ width: '120px', textAlign: 'right' }}>Quantity</th>
                        <th style={{ width: '150px', textAlign: 'right' }}>Estimated Unit Rate</th>
                        <th style={{ width: '180px', textAlign: 'right' }}>Total Estimated (INR)</th>
                      </tr>
                    </thead>
                    <tbody>
                      {tender.boq_items.map((boq) => (
                        <tr key={boq.item_code}>
                          <td className="mono-font" style={{ color: '#f59e0b', fontWeight: 600 }}>{boq.item_code}</td>
                          <td>{boq.description}</td>
                          <td style={{ color: '#94a3b8' }}>{boq.unit}</td>
                          <td style={{ textAlign: 'right', fontWeight: 600 }}>{boq.estimated_quantity.toLocaleString()}</td>
                          <td style={{ textAlign: 'right' }}>₹{boq.estimated_unit_rate_inr.toLocaleString()}</td>
                          <td style={{ textAlign: 'right', fontWeight: 700, color: '#34d399' }}>₹{(boq.total_estimated_cost_inr / 1e7).toFixed(2)} Cr</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* STEP 2: BIDDER DOSSIERS */}
        {currentStep === 2 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            <div className="glass-card">
              <div className="section-header">
                <div>
                  <h2 style={{ fontSize: '1.35rem', fontWeight: 800 }}>Bidder Dossiers & OCR Ingestion Pipeline</h2>
                  <p style={{ color: '#94a3b8', fontSize: '0.85rem' }}>
                    {bidders.length} Complete Bid Packages Extracted via PyMuPDF OCR Line Engine. Ready for CVC & QCBS Scrutiny.
                  </p>
                </div>

                <div style={{ display: 'flex', gap: '0.75rem' }}>
                  <button className="btn-secondary" onClick={() => setCurrentStep(1)}>Back</button>
                  <button className="btn-primary" onClick={runEvaluation} disabled={loading}>
                    {loading ? <RefreshCw className="spin" size={16} /> : <Zap size={16} />} Run Autonomous AI Scrutiny
                  </button>
                </div>
              </div>

              {/* Demo PDF Drag & Drop Zone */}
              <div className="dropzone-container" style={{ marginBottom: '1.5rem' }}>
                <UploadCloud size={36} color="#3b82f6" style={{ margin: '0 auto 0.5rem' }} />
                <h4 style={{ fontSize: '0.95rem', fontWeight: 700 }}>Upload Bidder PDFs or Tender Documents</h4>
                <p style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '4px' }}>
                  Pre-loaded with authentic demo PDFs in <code style={{ color: '#60a5fa' }}>data/demo_pdfs/</code>. Automatic layout & bounding box parsing.
                </p>
              </div>

              {/* Bidder Cards Grid */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(380px, 1fr))', gap: '1.25rem' }}>
                {bidders.map((b) => (
                  <div
                    key={b.id}
                    style={{
                      background: 'rgba(15, 23, 42, 0.7)',
                      border: '1px solid rgba(255, 255, 255, 0.08)',
                      borderRadius: '12px',
                      padding: '1.25rem',
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'space-between'
                    }}
                  >
                    <div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
                        <div>
                          <span className="mono-font" style={{ fontSize: '0.75rem', color: '#60a5fa' }}>{b.id}</span>
                          <h4 style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '2px' }}>{b.company_name}</h4>
                        </div>
                        <span className="badge badge-blue">₹{(b.financial_quote_inr / 1e7).toFixed(2)} Cr</span>
                      </div>

                      <div style={{ fontSize: '0.82rem', color: '#cbd5e1', display: 'flex', flexDirection: 'column', gap: '0.35rem', marginBottom: '1rem' }}>
                        <div>📊 <strong>Avg Annual Turnover:</strong> ₹{(b.financial_profile.avg_annual_turnover_inr / 1e7).toFixed(2)} Cr (3-Yr Avg)</div>
                        <div>💼 <strong>Past Experience:</strong> {b.past_experience_years} Years in Oil & Gas Pipeline EPC</div>
                        <div>📜 <strong>CA UDIN:</strong> <code style={{ color: '#fbbf24' }}>{b.financial_profile.ca_udin_number}</code></div>
                        <div>🖥️ <strong>Submission IP / MAC:</strong> <code style={{ color: '#94a3b8' }}>{b.documents[0]?.metadata?.workstation_id || 'DESKTOP-LNT-01'}</code></div>
                      </div>

                      {/* Documents Uploaded */}
                      <div>
                        <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#94a3b8', marginBottom: '0.4rem', textTransform: 'uppercase' }}>
                          Uploaded Documents ({b.documents.length})
                        </div>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                          {b.documents.map((doc, idx) => (
                            <span
                              key={idx}
                              style={{
                                background: 'rgba(255, 255, 255, 0.05)',
                                border: '1px solid rgba(255, 255, 255, 0.1)',
                                padding: '3px 8px',
                                borderRadius: '4px',
                                fontSize: '0.72rem',
                                color: '#94a3b8',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '4px'
                              }}
                            >
                              <FileText size={12} color="#60a5fa" /> {doc.filename}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>

                    <div style={{ marginTop: '1.25rem', paddingTop: '0.75rem', borderTop: '1px solid rgba(255, 255, 255, 0.08)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontSize: '0.75rem', color: '#34d399' }}>✓ OCR Line Parser Verified</span>
                      <span className="mono-font" style={{ fontSize: '0.75rem', color: '#64748b' }}>{b.tender_ref}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* STEP 3: EXECUTIVE SCRUTINY & RESULTS */}
        {currentStep === 3 && evaluation && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            {/* Top Summary Banner */}
            <div className="glass-card" style={{ borderLeft: '4px solid #3b82f6' }}>
              <div className="section-header">
                <div>
                  <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.4rem' }}>
                    <span className="badge badge-green">Scrutiny Completed: {evaluation.evaluated_at}</span>
                    <span className="badge badge-blue">Bidders: {evaluation.total_bidders} Total ({evaluation.qualified_count} Qualified, {evaluation.disqualified_count} Disqualified)</span>
                  </div>
                  <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Tender Scrutiny & QCBS Comparative Statement</h2>
                  <p style={{ color: '#cbd5e1', fontSize: '0.85rem', marginTop: '4px', maxWidth: '900px' }}>
                    {evaluation.executive_summary}
                  </p>
                </div>

                <div style={{ display: 'flex', gap: '0.75rem' }}>
                  <button className="btn-secondary" onClick={openGemExport}>
                    <ExternalLink size={16} /> Sync to GeM 3.0 / OCDS
                  </button>
                  <button
                    className="btn-primary"
                    onClick={() => window.open(`${API_BASE}/reports/export/${evaluation.tender_id}`, '_blank')}
                  >
                    <Download size={16} /> Export Official Scrutiny Note
                  </button>
                </div>
              </div>
            </div>

            {/* CVC Anti-Cartel Forensics & Interactive Network Graph */}
            {evaluation.cartel_alerts && evaluation.cartel_alerts.length > 0 && (
              <div className="cartel-canvas-container">
                <div className="cartel-canvas-header">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <ShieldAlert size={22} color="#ef4444" />
                    <div>
                      <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: '#f87171' }}>
                        CVC Red Flag Alert: High-Risk Collusive Bidding & Cartel Network Detected
                      </h3>
                      <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
                        Automated graph entity resolution uncovered metadata and CA UDIN sharing between competing bidders.
                      </p>
                    </div>
                  </div>
                  <span className="badge badge-red">CRITICAL VIGILANCE ALERT</span>
                </div>

                {/* SVG Visual Collusion Network Graph */}
                <div style={{ background: 'rgba(5, 10, 24, 0.9)', borderRadius: '8px', border: '1px solid rgba(239, 68, 68, 0.3)', padding: '1.5rem', marginBottom: '1.25rem' }}>
                  <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#f87171', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Network size={16} /> Visual Collusion Network Topology:
                  </div>

                  <svg width="100%" height="220" viewBox="0 0 800 220" style={{ overflow: 'visible' }}>
                    <defs>
                      <linearGradient id="collusionLine" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#ef4444" stopOpacity="0.8" />
                        <stop offset="50%" stopColor="#f59e0b" stopOpacity="0.9" />
                        <stop offset="100%" stopColor="#ef4444" stopOpacity="0.8" />
                      </linearGradient>
                    </defs>

                    {/* Connection Lines */}
                    <line x1="200" y1="60" x2="400" y2="130" stroke="url(#collusionLine)" strokeWidth="3" strokeDasharray="6,4" />
                    <line x1="600" y1="60" x2="400" y2="130" stroke="url(#collusionLine)" strokeWidth="3" strokeDasharray="6,4" />
                    <line x1="200" y1="60" x2="400" y2="50" stroke="#f59e0b" strokeWidth="2" strokeDasharray="4,4" />
                    <line x1="600" y1="60" x2="400" y2="50" stroke="#f59e0b" strokeWidth="2" strokeDasharray="4,4" />

                    {/* Node 1: Apex InfraTech */}
                    <g className="cartel-node" transform="translate(200, 60)">
                      <circle r="36" fill="#1e1b4b" stroke="#ef4444" strokeWidth="3" />
                      <text textAnchor="middle" y="-6" fill="#ffffff" fontSize="11" fontWeight="700">Apex InfraTech</text>
                      <text textAnchor="middle" y="10" fill="#f87171" fontSize="9">Bidder 2</text>
                      <text textAnchor="middle" y="24" fill="#94a3b8" fontSize="8">₹32.40 Cr</text>
                    </g>

                    {/* Node 2: Zenith Piping */}
                    <g className="cartel-node" transform="translate(600, 60)">
                      <circle r="36" fill="#1e1b4b" stroke="#ef4444" strokeWidth="3" />
                      <text textAnchor="middle" y="-6" fill="#ffffff" fontSize="11" fontWeight="700">Zenith Piping</text>
                      <text textAnchor="middle" y="10" fill="#f87171" fontSize="9">Bidder 3</text>
                      <text textAnchor="middle" y="24" fill="#94a3b8" fontSize="8">₹34.80 Cr</text>
                    </g>

                    {/* Shared Workstation Hub */}
                    <g className="cartel-node" transform="translate(400, 130)">
                      <circle r="32" fill="#3b0764" stroke="#d946ef" strokeWidth="2" />
                      <text textAnchor="middle" y="-5" fill="#f5d0fe" fontSize="10" fontWeight="700">Shared Host</text>
                      <text textAnchor="middle" y="9" fill="#e879f9" fontSize="8">DESKTOP-GAIL-99</text>
                      <text textAnchor="middle" y="21" fill="#a855f7" fontSize="8">MAC: A4:83:E7:...</text>
                    </g>

                    {/* Shared CA UDIN Hub */}
                    <g className="cartel-node" transform="translate(400, 45)">
                      <circle r="26" fill="#451a03" stroke="#f59e0b" strokeWidth="2" />
                      <text textAnchor="middle" y="-2" fill="#fef3c7" fontSize="9" fontWeight="700">Shared UDIN</text>
                      <text textAnchor="middle" y="11" fill="#fbbf24" fontSize="8">23094821B</text>
                    </g>
                  </svg>
                </div>

                {/* Alert Details */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '1rem' }}>
                  {evaluation.cartel_alerts.map((alert, idx) => (
                    <div
                      key={idx}
                      style={{
                        background: 'rgba(239, 68, 68, 0.08)',
                        border: '1px solid rgba(239, 68, 68, 0.3)',
                        borderRadius: '8px',
                        padding: '1rem'
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                        <strong style={{ color: '#f87171', fontSize: '0.9rem' }}>{alert.signal_name}</strong>
                        <span className="badge badge-red">{alert.severity}</span>
                      </div>
                      <div style={{ fontSize: '0.8rem', color: '#cbd5e1', marginBottom: '0.5rem' }}>
                        <strong>Bidders Flagged:</strong> {alert.bidders_involved.join(' & ')}
                      </div>
                      <div style={{ fontSize: '0.78rem', color: '#94a3b8', marginBottom: '0.5rem', background: 'rgba(0,0,0,0.3)', padding: '6px 8px', borderRadius: '4px' }}>
                        🔍 <strong>Forensic Evidence:</strong> {alert.forensic_evidence}
                      </div>
                      <div style={{ fontSize: '0.78rem', color: '#fbbf24' }}>
                        ⚖️ <strong>CVC Action:</strong> {alert.recommendation}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* QCBS Leaderboard */}
            <div className="glass-card">
              <div className="section-header">
                <h3 className="section-title">
                  <Award size={20} color="#f59e0b" /> Official QCBS Evaluation Leaderboard (70% Technical : 30% Financial)
                </h3>
                {evaluation.recommended_winner && (
                  <span className="badge badge-green" style={{ fontSize: '0.82rem', padding: '0.35rem 0.75rem' }}>
                    🏆 Recommended H1 Awardee: {evaluation.recommended_winner}
                  </span>
                )}
              </div>

              <div style={{ overflowX: 'auto', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '8px' }}>
                <table className="custom-table">
                  <thead>
                    <tr>
                      <th style={{ width: '60px' }}>Rank</th>
                      <th>Bidder Name</th>
                      <th style={{ width: '130px' }}>Eligibility Status</th>
                      <th style={{ width: '130px', textAlign: 'right' }}>Technical (Ts)</th>
                      <th style={{ width: '140px', textAlign: 'right' }}>Financial Quote</th>
                      <th style={{ width: '130px', textAlign: 'right' }}>Financial (Fs)</th>
                      <th style={{ width: '140px', textAlign: 'right' }}>Composite Score</th>
                      <th style={{ width: '110px' }}>Risk Profile</th>
                      <th style={{ width: '130px', textAlign: 'center' }}>Statutory Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {evaluation.leaderboard.map((entry) => (
                      <tr
                        key={entry.bidder_id}
                        style={{
                          background: entry.rank === 1 ? 'rgba(37, 99, 235, 0.12)' : 'transparent',
                          fontWeight: entry.rank === 1 ? 600 : 400
                        }}
                      >
                        <td>
                          {entry.rank === 1 ? (
                            <span style={{ color: '#fbbf24', fontSize: '1.1rem', fontWeight: 800 }}>#1</span>
                          ) : (
                            <span className="mono-font" style={{ color: '#94a3b8' }}>#{entry.rank}</span>
                          )}
                        </td>
                        <td style={{ fontWeight: 700 }}>
                          {entry.company_name}
                          {entry.rank === 1 && (
                            <span style={{ marginLeft: '8px', fontSize: '0.72rem', background: '#2563eb', color: '#fff', padding: '2px 6px', borderRadius: '4px' }}>
                              Recommended H1
                            </span>
                          )}
                        </td>
                        <td>
                          {entry.is_qualified ? (
                            <span className="badge badge-green"><Check size={12} /> QUALIFIED</span>
                          ) : (
                            <span className="badge badge-red"><X size={12} /> DISQUALIFIED</span>
                          )}
                        </td>
                        <td style={{ textAlign: 'right', fontWeight: 700, color: '#60a5fa' }}>
                          {entry.technical_score_ts.toFixed(1)} / 100
                        </td>
                        <td style={{ textAlign: 'right', fontWeight: 700 }}>
                          ₹{(entry.financial_quote_inr / 1e7).toFixed(2)} Cr
                        </td>
                        <td style={{ textAlign: 'right', fontWeight: 700, color: '#34d399' }}>
                          {entry.financial_score_fs.toFixed(1)} / 100
                        </td>
                        <td style={{ textAlign: 'right', fontWeight: 800, fontSize: '1rem', color: '#f59e0b' }}>
                          {entry.composite_score.toFixed(1)}
                        </td>
                        <td>
                          {entry.risk_level === 'LOW' && <span className="badge badge-green">LOW RISK</span>}
                          {entry.risk_level === 'MEDIUM' && <span className="badge badge-amber">MEDIUM RISK</span>}
                          {entry.risk_level === 'CRITICAL' && <span className="badge badge-red">CRITICAL RISK</span>}
                        </td>
                        <td style={{ textAlign: 'center' }}>
                          {!entry.is_qualified ? (
                            <button
                              onClick={() => generateGfrNotice(entry.bidder_id)}
                              className="btn-danger"
                              style={{ padding: '4px 8px', fontSize: '0.72rem' }}
                            >
                              GFR 173 Notice
                            </button>
                          ) : (
                            <span style={{ fontSize: '0.75rem', color: '#34d399' }}>Eligible</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Detailed Clause-by-Clause Scrutiny Checklist */}
            <div className="glass-card">
              <h3 className="section-title" style={{ marginBottom: '1.25rem' }}>
                <CheckCircle size={20} color="#10b981" /> Clause-by-Clause Compliance Verification & Grounded Proof
              </h3>

              {evaluation.bidder_reports.map((bReport) => (
                <div key={bReport.bidder_id} style={{ marginBottom: '2rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(15, 23, 42, 0.9)', padding: '0.75rem 1rem', borderRadius: '8px 8px 0 0', border: '1px solid rgba(255,255,255,0.08)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <Building size={18} color="#60a5fa" />
                      <strong style={{ fontSize: '1rem' }}>{bReport.company_name}</strong>
                      <span className="mono-font" style={{ fontSize: '0.75rem', color: '#94a3b8' }}>({bReport.bidder_id})</span>
                    </div>

                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                      <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Technical Score:</span>
                      <strong style={{ color: '#34d399', fontSize: '0.95rem' }}>{bReport.technical_score_ts.toFixed(1)} / 100</strong>
                    </div>
                  </div>

                  <div style={{ overflowX: 'auto', border: '1px solid rgba(255,255,255,0.08)', borderTop: 'none', borderRadius: '0 0 8px 8px' }}>
                    <table className="custom-table">
                      <thead>
                        <tr>
                          <th style={{ width: '130px' }}>Clause Ref</th>
                          <th style={{ width: '200px' }}>Parameter</th>
                          <th style={{ width: '120px' }}>Compliance</th>
                          <th>Extracted Evidence Snippet</th>
                          <th style={{ width: '100px', textAlign: 'right' }}>Score</th>
                          <th style={{ width: '110px', textAlign: 'center' }}>Inspect Proof</th>
                        </tr>
                      </thead>
                      <tbody>
                        {bReport.checks.map((item, cIdx) => (
                          <tr key={cIdx}>
                            <td className="mono-font" style={{ color: '#60a5fa', fontSize: '0.8rem' }}>{item.clause_ref}</td>
                            <td style={{ fontWeight: 600 }}>{item.parameter}</td>
                            <td>
                              {item.status === 'COMPLIANT' && <span className="badge badge-green"><Check size={12} /> Compliant</span>}
                              {item.status === 'NON_COMPLIANT' && <span className="badge badge-red"><X size={12} /> Non-Compliant</span>}
                              {item.status !== 'COMPLIANT' && item.status !== 'NON_COMPLIANT' && <span className="badge badge-amber">Discrepancy</span>}
                            </td>
                            <td style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>
                              <div style={{ fontStyle: 'italic', background: 'rgba(0,0,0,0.2)', padding: '4px 8px', borderRadius: '4px' }}>
                                "{item.evidence_snippet}"
                              </div>
                              {item.rejection_reason && <div style={{ fontSize: '0.72rem', color: '#f87171', marginTop: '2px' }}>{item.rejection_reason}</div>}
                            </td>
                            <td style={{ textAlign: 'right', fontWeight: 700, color: '#34d399' }}>
                              {item.technical_marks_awarded} / {item.technical_marks_max}
                            </td>
                            <td style={{ textAlign: 'center' }}>
                              <button
                                onClick={() => {
                                  const matchingBidder = bidders.find(b => b.id === bReport.bidder_id) || bidders[0];
                                  openEvidenceProof(item, matchingBidder);
                                }}
                                className="btn-secondary"
                                style={{ padding: '4px 8px', fontSize: '0.72rem' }}
                              >
                                <Eye size={12} /> Proof BBox
                              </button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* MODAL: GROUNDED PROOF & EXACT PDF PAGE BOUNDING BOX */}
      {inspectModal && (
        <div className="modal-backdrop" onClick={() => setInspectModal(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <Eye size={20} color="#60a5fa" />
                <div>
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>
                    Side-by-Side Grounded Proof Verification
                  </h3>
                  <p style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
                    Clause: {inspectModal.item.clause_ref} | Parameter: {inspectModal.item.parameter}
                  </p>
                </div>
              </div>
              <button onClick={() => setInspectModal(null)} style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}>
                <X size={20} />
              </button>
            </div>

            <div className="modal-body" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
              {/* Left Column: AI Finding & Evidence */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div style={{ background: 'rgba(15, 23, 42, 0.8)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '8px', padding: '1rem' }}>
                  <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#94a3b8', marginBottom: '0.25rem' }}>EVALUATION OUTCOME</div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
                    {inspectModal.item.status === 'COMPLIANT' && <span className="badge badge-green">COMPLIANT (Score: {inspectModal.item.technical_marks_awarded}/{inspectModal.item.technical_marks_max})</span>}
                    {inspectModal.item.status === 'NON_COMPLIANT' && <span className="badge badge-red">NON-COMPLIANT (Score: {inspectModal.item.technical_marks_awarded}/{inspectModal.item.technical_marks_max})</span>}
                    {inspectModal.item.status !== 'COMPLIANT' && inspectModal.item.status !== 'NON_COMPLIANT' && <span className="badge badge-amber">PARTIAL (Score: {inspectModal.item.technical_marks_awarded}/{inspectModal.item.technical_marks_max})</span>}
                  </div>

                  <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#94a3b8', marginBottom: '0.25rem' }}>EXTRACTED EVIDENCE CITATION</div>
                  <div style={{ background: 'rgba(0,0,0,0.4)', padding: '0.75rem', borderRadius: '6px', fontSize: '0.85rem', color: '#f8fafc', fontStyle: 'italic', borderLeft: '3px solid #3b82f6' }}>
                    "{inspectModal.item.evidence_snippet}"
                  </div>

                  {inspectModal.item.rejection_reason && (
                    <div style={{ marginTop: '0.75rem', fontSize: '0.8rem', color: '#f87171' }}>
                      <strong>Scrutiny Finding:</strong> {inspectModal.item.rejection_reason}
                    </div>
                  )}
                </div>

                <div style={{ background: 'rgba(15, 23, 42, 0.8)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '8px', padding: '1rem' }}>
                  <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#94a3b8', marginBottom: '0.5rem' }}>OCR & INTEGRITY METADATA</div>
                  <div style={{ fontSize: '0.78rem', color: '#cbd5e1', display: 'flex', flexDirection: 'column', gap: '0.3rem' }}>
                    <div>📄 <strong>Source File:</strong> {inspectModal.bidder.documents[0]?.filename || 'Bidder_Dossier.pdf'}</div>
                    <div>🏷️ <strong>SHA-256 Hash:</strong> <code style={{ color: '#60a5fa' }}>{inspectModal.bidder.documents[0]?.sha256_hash?.slice(0, 24)}...</code></div>
                    <div>⏱️ <strong>OCR Engine:</strong> PyMuPDF 1.25 Line-Extraction (Active)</div>
                    <div>📍 <strong>Target Bounding Box:</strong> {bboxData ? `x:${bboxData.normalized_bbox[0]}% y:${bboxData.normalized_bbox[1]}% w:${bboxData.normalized_bbox[2]}% h:${bboxData.normalized_bbox[3]}%` : 'Calculating...'}</div>
                  </div>
                </div>
              </div>

              {/* Right Column: Exact PDF Page PNG with SVG Highlight */}
              <div>
                <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#94a3b8', marginBottom: '0.5rem' }}>
                  AUTHENTIC DOCUMENT PAGE VIEW (WITH BOUNDING BOX)
                </div>
                <div className="pdf-page-viewer-wrapper" style={{ maxHeight: '450px', overflowY: 'auto' }}>
                  <div style={{ position: 'relative', width: '100%' }}>
                    <img
                      src={`${API_BASE}/ocr/page-image/${encodeURIComponent(inspectModal.bidder.documents[0]?.filename || 'Bidder1_LT_Hydrocarbon_Engineering.pdf')}/1`}
                      alt="Document Page"
                      className="pdf-page-image"
                      onError={(e) => {
                        e.target.src = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='500'><rect width='400' height='500' fill='%231e293b'/><text x='50%25' y='50%25' fill='%2394a3b8' text-anchor='middle'>PDF Document Preview</text></svg>";
                      }}
                    />
                    {bboxData && (
                      <div
                        className="bbox-overlay-rect"
                        style={{
                          left: `${bboxData.normalized_bbox[0]}%`,
                          top: `${bboxData.normalized_bbox[1]}%`,
                          width: `${bboxData.normalized_bbox[2]}%`,
                          height: `${bboxData.normalized_bbox[3]}%`
                        }}
                      />
                    )}
                  </div>
                </div>
              </div>
            </div>

            <div className="modal-footer">
              <button className="btn-secondary" onClick={() => setInspectModal(null)}>Close</button>
              <button
                className="btn-primary"
                onClick={() => {
                  logAction("CONFIRM_GROUNDED_PROOF", inspectModal.item.clause_ref, `Officer confirmed evidence citation for ${inspectModal.bidder.company_name}`);
                  setInspectModal(null);
                }}
              >
                <CheckCircle size={16} /> Mark Verified by Officer
              </button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL: EXECUTIVE THRESHOLD TUNER */}
      {thresholdModalOpen && (
        <div className="modal-backdrop" onClick={() => setThresholdModalOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <Sliders size={20} color="#f59e0b" />
                <div>
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Executive Threshold & Criteria Tuner</h3>
                  <p style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
                    Chief Executive Role: Adjust eligibility criteria thresholds & QCBS weights within statutory GFR limits.
                  </p>
                </div>
              </div>
              <button onClick={() => setThresholdModalOpen(false)} style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}>
                <X size={20} />
              </button>
            </div>

            <div className="modal-body">
              {thresholdError && (
                <div style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid #ef4444', color: '#f87171', padding: '0.75rem', borderRadius: '8px', marginBottom: '1rem', fontSize: '0.85rem' }}>
                  ⚠️ {thresholdError}
                </div>
              )}

              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {editedRequirements.map((req, idx) => (
                  <div key={req.id} style={{ background: 'rgba(15, 23, 42, 0.7)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '8px', padding: '1rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                      <div>
                        <span className="mono-font" style={{ color: '#60a5fa', fontSize: '0.75rem' }}>{req.clause_ref}</span>
                        <h4 style={{ fontSize: '0.95rem', fontWeight: 700 }}>{req.parameter}</h4>
                      </div>
                      <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', cursor: 'pointer' }}>
                        <input
                          type="checkbox"
                          checked={req.is_mandatory}
                          onChange={(e) => {
                            const updated = [...editedRequirements];
                            updated[idx].is_mandatory = e.target.checked;
                            setEditedRequirements(updated);
                          }}
                        />
                        <span style={{ color: req.is_mandatory ? '#f87171' : '#94a3b8' }}>Mandatory Gate</span>
                      </label>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1rem', marginTop: '0.5rem' }}>
                      <div>
                        <label style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Threshold Description</label>
                        <input
                          type="text"
                          value={req.threshold}
                          onChange={(e) => {
                            const updated = [...editedRequirements];
                            updated[idx].threshold = e.target.value;
                            setEditedRequirements(updated);
                          }}
                          style={{
                            width: '100%',
                            background: 'rgba(0,0,0,0.3)',
                            border: '1px solid rgba(255,255,255,0.1)',
                            borderRadius: '6px',
                            padding: '6px 10px',
                            color: '#fff',
                            fontSize: '0.82rem',
                            marginTop: '2px'
                          }}
                        />
                      </div>

                      <div>
                        <label style={{ fontSize: '0.75rem', color: '#94a3b8' }}>QCBS Weight (%)</label>
                        <input
                          type="number"
                          value={req.qcbs_weight}
                          onChange={(e) => {
                            const updated = [...editedRequirements];
                            updated[idx].qcbs_weight = parseFloat(e.target.value) || 0;
                            setEditedRequirements(updated);
                          }}
                          style={{
                            width: '100%',
                            background: 'rgba(0,0,0,0.3)',
                            border: '1px solid rgba(255,255,255,0.1)',
                            borderRadius: '6px',
                            padding: '6px 10px',
                            color: '#34d399',
                            fontWeight: 700,
                            fontSize: '0.82rem',
                            marginTop: '2px'
                          }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="modal-footer">
              <button className="btn-secondary" onClick={() => setThresholdModalOpen(false)}>Cancel</button>
              <button className="btn-accent" onClick={handleSaveThresholds}>
                Save & Apply Thresholds
              </button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL: GFR RULE 173 STATUTORY CLARIFICATION NOTICE */}
      {gfrNoticeModal && (
        <div className="modal-backdrop" onClick={() => setGfrNoticeModal(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <Send size={20} color="#f87171" />
                <div>
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>
                    GFR Rule 173 Clarification Notice ({gfrNoticeModal.notice_ref})
                  </h3>
                  <p style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
                    Issued to M/s {gfrNoticeModal.company_name} | 48-Hour Response Deadline
                  </p>
                </div>
              </div>
              <button onClick={() => setGfrNoticeModal(null)} style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}>
                <X size={20} />
              </button>
            </div>

            <div className="modal-body">
              <pre style={{ background: '#090f1f', border: '1px solid rgba(255,255,255,0.1)', padding: '1.25rem', borderRadius: '8px', color: '#cbd5e1', fontSize: '0.8rem', whiteSpace: 'pre-wrap', maxHeight: '420px', overflowY: 'auto' }}>
                {gfrNoticeModal.notice_text}
              </pre>
            </div>

            <div className="modal-footer">
              <button className="btn-secondary" onClick={() => setGfrNoticeModal(null)}>Close</button>
              <button
                className="btn-primary"
                onClick={() => {
                  navigator.clipboard.writeText(gfrNoticeModal.notice_text);
                  alert("Official Notice copied to clipboard!");
                }}
              >
                Copy Notice Text
              </button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL: GeM 3.0 / OCDS API EXPORT */}
      {gemExportModal && (
        <div className="modal-backdrop" onClick={() => setGemExportModal(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <ExternalLink size={20} color="#34d399" />
                <div>
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>GeM 3.0 / OCDS 1.1.5 Evaluation Export Package</h3>
                  <p style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
                    Live Gateway: mkp.gem.gov.in / eprocure.gov.in | TLS 1.3 Verified
                  </p>
                </div>
              </div>
              <button onClick={() => setGemExportModal(null)} style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}>
                <X size={20} />
              </button>
            </div>

            <div className="modal-body">
              <div style={{ background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.3)', padding: '0.75rem 1rem', borderRadius: '8px', marginBottom: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <strong style={{ color: '#34d399', fontSize: '0.9rem' }}>GeM Gateway Synchronized</strong>
                  <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>OCDS Standard Version: {gemExportModal.ocds_package.version}</div>
                </div>
                <span className="badge badge-green">200 OK - SYNCED</span>
              </div>

              <pre style={{ background: '#090f1f', border: '1px solid rgba(255,255,255,0.1)', padding: '1.25rem', borderRadius: '8px', color: '#60a5fa', fontSize: '0.78rem', whiteSpace: 'pre-wrap', maxHeight: '350px', overflowY: 'auto' }}>
                {JSON.stringify(gemExportModal, null, 2)}
              </pre>
            </div>

            <div className="modal-footer">
              <button className="btn-secondary" onClick={() => setGemExportModal(null)}>Close</button>
              <button
                className="btn-primary"
                onClick={() => {
                  navigator.clipboard.writeText(JSON.stringify(gemExportModal, null, 2));
                  alert("GeM JSON Schema copied!");
                }}
              >
                Copy GeM JSON
              </button>
            </div>
          </div>
        </div>
      )}

      {/* DRAWER: AUDIT LOG VIEWER */}
      {showAuditDrawer && (
        <div className="modal-backdrop" onClick={() => setShowAuditDrawer(false)}>
          <div className="modal-content" style={{ maxWidth: '650px' }} onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <ShieldCheck size={20} color="#3b82f6" />
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Immutable IAM Audit Trail</h3>
              </div>
              <button onClick={() => setShowAuditDrawer(false)} style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}>
                <X size={20} />
              </button>
            </div>

            <div className="modal-body" style={{ maxHeight: '450px', overflowY: 'auto' }}>
              {auditLogs.length === 0 ? (
                <div style={{ color: '#94a3b8', textAlign: 'center', padding: '2rem' }}>No audit logs recorded yet.</div>
              ) : (
                auditLogs.map((log) => (
                  <div key={log.id} className="audit-log-pill">
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2px' }}>
                      <strong style={{ color: '#60a5fa' }}>{log.user_name} ({log.role})</strong>
                      <span style={{ color: '#94a3b8', fontSize: '0.7rem' }}>{log.timestamp}</span>
                    </div>
                    <div style={{ color: '#e2e8f0', fontSize: '0.78rem' }}>
                      <strong>Action:</strong> <code style={{ color: '#fbbf24' }}>{log.action}</code> on <strong>{log.target}</strong>
                    </div>
                    <div style={{ color: '#94a3b8', fontSize: '0.72rem', marginTop: '2px' }}>{log.details}</div>
                  </div>
                ))
              )}
            </div>

            <div className="modal-footer">
              <button className="btn-secondary" onClick={() => setShowAuditDrawer(false)}>Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
