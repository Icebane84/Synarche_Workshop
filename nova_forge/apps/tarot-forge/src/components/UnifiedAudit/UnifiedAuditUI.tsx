import React from 'react';
import scanData from '../../engine/data/audit-report.json';
import './UnifiedAuditUI.css';

interface Mismatch {
    id: string;
    file: string;
    type: string;
    expected: string;
    actual: string;
}

interface AuditReport {
    timestamp: string;
    total_scanned: number;
    dissonance_count: number;
    coherence_index: number;
    mismatches: Mismatch[];
}

export const UnifiedAuditUI: React.FC = () => {
    // In a real app, this would be a live fetch.
    // For now we import the JSON directly or utilize a simulated query.
    const report: AuditReport = scanData as AuditReport;

    return (
        <div className="audit-dashboard">
            <div className="audit-header">
                <h1>SYSTEM COHERENCE AUDIT</h1>
                <div className="audit-meta">
                    <span>SCAN_ID: {report.timestamp}</span>
                    <span>TARGET: GVRN_ROOT</span>
                </div>
            </div>

            <div className="coherence-display">
                <div className="coherence-gauge">
                    <svg viewBox="0 0 36 36" className="circular-chart">
                        <path
                            className="circle-bg"
                            d="M18 2.0845
                            a 15.9155 15.9155 0 0 1 0 31.831
                            a 15.9155 15.9155 0 0 1 0 -31.831"
                        />
                        <path
                            className="circle"
                            strokeDasharray={`${report.coherence_index}, 100`}
                            d="M18 2.0845
                            a 15.9155 15.9155 0 0 1 0 31.831
                            a 15.9155 15.9155 0 0 1 0 -31.831"
                        />
                        <text x="18" y="20.35" className="percentage">
                            {report.coherence_index.toFixed(1)}%
                        </text>
                    </svg>
                </div>
                <div className="coherence-stats">
                    <div className="stat-item">
                        <span className="label">PROTOCOLS SCANNED</span>
                        <span className="value">{report.total_scanned}</span>
                    </div>
                    <div className="stat-item">
                        <span className="label">DISSONANCE DETECTED</span>
                        <span className="value error">{report.dissonance_count}</span>
                    </div>
                </div>
            </div>

            <div className="audit-log">
                <h3>DISSONANCE LOG</h3>
                {report.mismatches.length === 0 ? (
                    <div className="log-empty">
                        <span>NO DISSONANCE DETECTED. SYSTEM IS RESONANT.</span>
                    </div>
                ) : (
                    <div className="log-list">
                        {report.mismatches.map((m) => (
                            <div key={`${m.id}-${m.file}`} className="log-entry">
                                <div className="entry-header">
                                    <span className="entry-id">{m.id}</span>
                                    <span className="entry-type">[{m.type}]</span>
                                </div>
                                <div className="entry-details">
                                    <span className="expected">EXP: {m.expected}</span>
                                    <span className="actual">ACT: {m.actual}</span>
                                </div>
                                <div className="entry-file">{m.file}</div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <div className="audit-actions">
                <button
                    className="action-btn reforge"
                    onClick={() => console.log('INITIATE_REFORGE')}
                >
                    INITIATE REFORGE PROTOCOL
                </button>
                <button
                    className="action-btn verify"
                    onClick={() => console.log('VERIFY_INTEGRITY')}
                >
                    VERIFY INTEGRITY
                </button>
            </div>
        </div>
    );
};
