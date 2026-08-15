import React, { useState } from 'react';
import './CrystallineCognition.css';

export const CrystallineCognition: React.FC = () => {
    const [inputQuery, setInputQuery] = useState('');
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [facets, setFacets] = useState<{ name: string; score: number; status: string }[]>([
        { name: 'ETHICAL', score: 0, status: 'IDLE' },
        { name: 'TECHNICAL', score: 0, status: 'IDLE' },
        { name: 'AESTHETIC', score: 0, status: 'IDLE' },
        { name: 'STRUCTURAL', score: 0, status: 'IDLE' },
    ]);

    const handleAnalyze = () => {
        setIsAnalyzing(true);
        const newFacets = facets.map((f) => ({ ...f, score: 0, status: 'REFRACTING...' }));
        setFacets(newFacets);

        // Simulate Analysis
        setTimeout(() => {
            const results = facets.map((f) => ({
                name: f.name,
                score: Math.floor(Math.random() * 20) + 80, // Random 80-100
                status: 'RESOLVED',
            }));
            setFacets(results);
            setIsAnalyzing(false);
        }, 2000);
    };

    return (
        <div className="crystal-container">
            <div className="prism-stage">
                <div className={`crystal-core ${isAnalyzing ? 'pulsing' : ''}`}>
                    <div className="facet front"></div>
                    <div className="facet back"></div>
                    <div className="facet left"></div>
                    <div className="facet right"></div>
                    <div className="facet top"></div>
                    <div className="facet bottom"></div>
                </div>
                {isAnalyzing && <div className="beam-of-light"></div>}
            </div>

            <div className="analysis-panel">
                <div className="input-group">
                    <input
                        type="text"
                        placeholder="Enter Artifact ID to Refract..."
                        value={inputQuery}
                        onChange={(e) => setInputQuery(e.target.value)}
                        disabled={isAnalyzing}
                    />
                    <button onClick={handleAnalyze} disabled={isAnalyzing || !inputQuery}>
                        {isAnalyzing ? 'REFRACTING...' : 'REFRACT'}
                    </button>
                </div>

                <div className="facet-grid">
                    {facets.map((facet) => (
                        <div
                            key={facet.name}
                            className={`facet-card ${facet.status.toLowerCase()}`}
                        >
                            <div className="facet-header">
                                <span className="facet-name">{facet.name}</span>
                                <span className="facet-score">{facet.score}%</span>
                            </div>
                            <div className="progress-bar">
                                <div
                                    className="progress-fill"
                                    style={{
                                        width: `${facet.status === 'IDLE' ? 0 : facet.score}%`,
                                    }}
                                ></div>
                            </div>
                            <div className="facet-status">{facet.status}</div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};
