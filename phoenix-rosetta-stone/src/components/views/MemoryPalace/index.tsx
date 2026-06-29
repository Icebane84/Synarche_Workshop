import React, { useState } from "react";
import { useMemoryFeed } from "@/core/hooks/useMemoryFeed";
import { DataTable } from "@/components/ui/DataTable";
import { LivePill } from "@/components/ui/LivePill";

export const MemoryPalaceView: React.FC = () => {
  const {
    memories,
    total,
    isLoading,
    error,
    page,
    setPage,
    setFilters,
    insert,
    updateState,
    archive,
    remove,
    checkResonance,
  } = useMemoryFeed();

  // Insert form state
  const [newContent, setNewContent] = useState("");
  const [newDomain, setNewDomain] = useState("Axiom");
  const [newLayer, setNewLayer] = useState(1);
  const [isInserting, setIsInserting] = useState(false);

  // Filter state
  const [domainFilter, setDomainFilter] = useState("");
  const [stateFilter, setStateFilter] = useState("");
  const [searchFilter, setSearchFilter] = useState("");

  // Resonance Auditor modal state
  const [auditItem, setAuditItem] = useState<any | null>(null);
  const [auditResult, setAuditResult] = useState<any | null>(null);
  const [isAuditing, setIsAuditing] = useState(false);

  const handleInsert = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newContent.trim()) return;

    setIsInserting(true);
    try {
      await insert({
        content: newContent,
        domain: newDomain,
        memory_layer: newLayer,
      });
      setNewContent("");
    } catch (err) {
      console.error(err);
    } finally {
      setIsInserting(false);
    }
  };

  const handleFilterChange = (domain: string, state: string, search: string) => {
    setDomainFilter(domain);
    setStateFilter(state);
    setSearchFilter(search);

    setFilters({
      domain: domain || undefined,
      state: (state as any) || undefined,
      search: search || undefined,
    });
  };

  const handleTestResonance = async (row: any) => {
    setAuditItem(row);
    setAuditResult(null);
    setIsAuditing(true);
    try {
      const result = await checkResonance(`MEMORY_CHIP_${row.id}`, row.content);
      setAuditResult(result);
    } catch (err: any) {
      setAuditResult({ error: err.message || "Failed to run resonance audit." });
    } finally {
      setIsAuditing(false);
    }
  };

  const handleExportCSV = () => {
    if (!memories.length) return;
    const headers = ["ID", "Domain", "Memory Layer", "State", "Content"];
    const rows = memories.map((m) => [
      m.id,
      `"${m.domain}"`,
      m.memory_layer ?? 1,
      `"${m.state}"`,
      `"${(m.content || "").replace(/"/g, '""')}"`,
    ]);
    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map((r) => r.join(","))].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `memory_palace_export_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const columns = [
    {
      header: "ID",
      accessor: (row: any) => <span className="text-[10px] text-white/40">#{row.id}</span>,
      className: "w-12",
    },
    {
      header: "Domain",
      accessor: (row: any) => <LivePill label={row.domain} type="info" />,
      className: "w-24",
    },
    {
      header: "Memory Content",
      accessor: (row: any) => <span className="font-sans text-xs text-white/90 break-words">{row.content}</span>,
    },
    {
      header: "Layer",
      accessor: (row: any) => <span className="text-white/60">L{row.memory_layer ?? 1}</span>,
      className: "w-14",
    },
    {
      header: "State",
      accessor: (row: any) => (
        <select
          value={row.state}
          onChange={(e) => updateState(row.id, e.target.value as any)}
          className="bg-deep-space border border-white/10 rounded px-1.5 py-0.5 text-[11px] text-white/80 focus:outline-none cursor-pointer"
        >
          <option value="Active">Active</option>
          <option value="Fading">Fading</option>
          <option value="Consolidated">Consolidated</option>
          <option value="Archived">Archived</option>
        </select>
      ),
      className: "w-28",
    },
    {
      header: "Actions",
      accessor: (row: any) => (
        <div className="flex items-center gap-1.5">
          <button
            onClick={() => handleTestResonance(row)}
            className="px-2 py-0.5 border border-celestial-blue/30 hover:border-celestial-blue rounded bg-celestial-blue/10 hover:bg-celestial-blue/20 text-[10px] text-celestial-blue transition-colors cursor-pointer"
            title="Run Sentinel Resonance Audit"
          >
            Audit
          </button>
          {row.state !== "Archived" && (
            <button
              onClick={() => archive(row.id)}
              className="px-2 py-0.5 border border-white/10 hover:border-chris-amber/40 rounded bg-white/5 hover:bg-chris-amber/10 text-[10px] text-white/50 hover:text-chris-amber transition-colors cursor-pointer"
            >
              Archive
            </button>
          )}
          <button
            onClick={() => remove(row.id)}
            className="px-2 py-0.5 border border-white/10 hover:border-red-500/40 rounded bg-white/5 hover:bg-red-500/10 text-[10px] text-white/50 hover:text-red-500 transition-colors cursor-pointer"
          >
            Delete
          </button>
        </div>
      ),
      className: "w-40",
    },
  ];

  return (
    <div className="space-y-6 animate-appear">
      {/* View Header */}
      <div className="flex items-center justify-between border-b border-white/5 pb-4">
        <div>
          <h2 className="text-sm font-bold tracking-[0.25em] text-white uppercase flex items-center gap-2">
            <span>MEMORY PALACE</span>
            <span className="text-[10px] bg-celestial-blue/20 text-celestial-blue px-2 py-0.5 rounded border border-celestial-blue/30 font-mono">
              INTERACTIVE COGNITION
            </span>
          </h2>
          <p className="text-[11px] text-white/40 font-mono mt-0.5">
            Full-spectrum CRUD access, interactive cognitive state switching, and Sentinel resonance auditing
          </p>
        </div>
        <div className="flex items-center gap-4">
          <button
            onClick={handleExportCSV}
            className="px-3 py-1.5 bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 text-white/80 rounded text-xs font-mono transition-all cursor-pointer flex items-center gap-1.5"
          >
            <span>📥</span> EXPORT MATRIX
          </button>
          <div className="text-right font-mono text-[10px] text-white/40">
            Total Nodes: <span className="text-celestial-blue font-bold">{total}</span>
          </div>
        </div>
      </div>

      {/* Grid: Left - Insert Form; Right - Table */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Insert Panel */}
        <div className="bg-panel-bg/40 border border-white/5 p-4 rounded-lg space-y-4 font-mono">
          <h3 className="text-xs font-semibold text-white/70 uppercase tracking-wider">
            ENGRAVE MEMORY CHIP
          </h3>
          <form onSubmit={handleInsert} className="space-y-3">
            <div>
              <label className="block text-[10px] text-chrome mb-1">Domain</label>
              <select
                value={newDomain}
                onChange={(e) => setNewDomain(e.target.value)}
                className="w-full bg-deep-space border border-white/10 rounded px-2.5 py-1.5 text-xs text-white/80 focus:border-celestial-blue/50 focus:outline-none"
              >
                <option value="Axiom">Axiom</option>
                <option value="Epistemic">Epistemic</option>
                <option value="RPG">RPG</option>
                <option value="Substrate">Substrate</option>
              </select>
            </div>

            <div>
              <label className="block text-[10px] text-chrome mb-1">Layer Depth</label>
              <input
                type="number"
                min={1}
                max={9}
                value={newLayer}
                onChange={(e) => setNewLayer(Number(e.target.value))}
                className="w-full bg-deep-space border border-white/10 rounded px-2.5 py-1.5 text-xs text-white/80 focus:border-celestial-blue/50 focus:outline-none font-mono"
              />
            </div>

            <div>
              <label className="block text-[10px] text-chrome mb-1">Content</label>
              <textarea
                value={newContent}
                onChange={(e) => setNewContent(e.target.value)}
                placeholder="Log memory context details..."
                rows={4}
                className="w-full bg-deep-space border border-white/10 rounded px-2.5 py-1.5 text-xs text-white/80 focus:border-celestial-blue/50 focus:outline-none font-sans"
              />
            </div>

            <button
              type="submit"
              disabled={isInserting || !newContent.trim()}
              className="w-full py-2 bg-celestial-blue/15 hover:bg-celestial-blue/25 border border-celestial-blue/40 hover:border-celestial-blue/60 text-celestial-blue rounded text-xs tracking-widest font-semibold transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              {isInserting ? "ENGRAVING..." : "ENGRAVE CHIP"}
            </button>
          </form>
        </div>

        {/* Table & Filter Panel */}
        <div className="lg:col-span-3 space-y-4">
          {/* Filters Bar */}
          <div className="flex flex-wrap gap-3 bg-panel-bg/20 border border-white/5 p-3 rounded-lg font-mono text-xs">
            <div className="flex items-center gap-2">
              <span className="text-white/40">Domain:</span>
              <select
                value={domainFilter}
                onChange={(e) => handleFilterChange(e.target.value, stateFilter, searchFilter)}
                className="bg-deep-space border border-white/10 rounded px-2 py-1 text-white/80"
              >
                <option value="">ALL DOMAINS</option>
                <option value="Axiom">AXIOM</option>
                <option value="Epistemic">EPISTEMIC</option>
                <option value="RPG">RPG</option>
                <option value="Substrate">SUBSTRATE</option>
              </select>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-white/40">State:</span>
              <select
                value={stateFilter}
                onChange={(e) => handleFilterChange(domainFilter, e.target.value, searchFilter)}
                className="bg-deep-space border border-white/10 rounded px-2 py-1 text-white/80"
              >
                <option value="">ALL STATES</option>
                <option value="Active">ACTIVE</option>
                <option value="Fading">FADING</option>
                <option value="Consolidated">CONSOLIDATED</option>
                <option value="Archived">ARCHIVED</option>
              </select>
            </div>

            <div className="flex-1 min-w-[200px] flex items-center gap-2 border border-white/10 rounded bg-deep-space px-2">
              <span className="text-white/30">🔍</span>
              <input
                type="text"
                value={searchFilter}
                onChange={(e) => handleFilterChange(domainFilter, stateFilter, e.target.value)}
                placeholder="Search memory text..."
                className="w-full bg-transparent border-none py-1 focus:outline-none text-white/80 text-xs font-sans"
              />
            </div>
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded text-xs font-mono">
              Database error: {error}
            </div>
          )}

          {/* Data Table */}
          <DataTable
            data={memories}
            columns={columns}
            isLoading={isLoading}
            emptyMessage="No matching memory records detected."
          />

          {/* Pagination Controls */}
          <div className="flex justify-between items-center font-mono text-[11px] text-white/40 pt-2">
            <div>
              Showing {memories.length} entries of {total} total
            </div>
            <div className="flex items-center gap-2">
              <button
                disabled={page === 0}
                onClick={() => setPage(page - 1)}
                className="px-2.5 py-1 bg-white/5 border border-white/10 rounded disabled:opacity-30 disabled:cursor-not-allowed hover:bg-white/10 hover:text-white cursor-pointer"
              >
                &lt; PREV
              </button>
              <span className="text-white/60">Page {page + 1}</span>
              <button
                disabled={(page + 1) * 20 >= total}
                onClick={() => setPage(page + 1)}
                className="px-2.5 py-1 bg-white/5 border border-white/10 rounded disabled:opacity-30 disabled:cursor-not-allowed hover:bg-white/10 hover:text-white cursor-pointer"
              >
                NEXT &gt;
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Sentinel Resonance Audit Modal */}
      {auditItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-appear">
          <div className="bg-panel-bg border border-celestial-blue/40 rounded-lg max-w-xl w-full p-6 font-mono space-y-4 shadow-2xl">
            <div className="flex justify-between items-center border-b border-white/10 pb-3">
              <div>
                <h3 className="text-sm font-bold text-celestial-blue tracking-wider flex items-center gap-2">
                  <span>🛡️ SENTINEL RESONANCE AUDIT</span>
                </h3>
                <p className="text-[10px] text-white/50">Target Memory Chip #{auditItem.id}</p>
              </div>
              <button
                onClick={() => setAuditItem(null)}
                className="text-white/40 hover:text-white text-sm cursor-pointer px-2"
              >
                ✕
              </button>
            </div>

            <div className="bg-deep-space p-3 rounded border border-white/5 text-xs text-white/80 font-sans break-words">
              <span className="text-[10px] text-chrome font-mono block mb-1 uppercase tracking-wider">Content:</span>
              {auditItem.content}
            </div>

            {isAuditing ? (
              <div className="py-8 text-center space-y-2">
                <div className="inline-block animate-spin text-celestial-blue text-lg">⚙️</div>
                <p className="text-xs text-celestial-blue tracking-widest uppercase">Invoking Wisdom & Analyzing Cognitive Structure...</p>
              </div>
            ) : auditResult ? (
              auditResult.error ? (
                <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-3 rounded text-xs">
                  {auditResult.error}
                </div>
              ) : (
                <div className="space-y-4 text-xs">
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-white/5 border border-white/10 p-3 rounded text-center">
                      <span className="text-[10px] text-white/40 uppercase block">Resonance Score</span>
                      <span className={`text-xl font-bold ${auditResult.resonance_score >= 0.85 ? "text-green-400" : "text-amber-400"}`}>
                        {(auditResult.resonance_score * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="bg-white/5 border border-white/10 p-3 rounded text-center">
                      <span className="text-[10px] text-white/40 uppercase block">Status</span>
                      <span className={`text-xs font-semibold tracking-wider block mt-1 ${auditResult.status === "STABLE" ? "text-green-400" : "text-amber-400"}`}>
                        {auditResult.status}
                      </span>
                    </div>
                  </div>

                  {auditResult.quest_generated && (
                    <div className="bg-amber-500/15 border border-amber-500/40 text-amber-300 p-3 rounded flex items-center justify-between text-xs">
                      <span className="font-semibold flex items-center gap-1.5">
                        <span>⚡</span> Refinement Quest Auto-Generated in RPG Suite!
                      </span>
                    </div>
                  )}

                  <div>
                    <h4 className="text-[11px] font-semibold text-white/70 mb-2 uppercase tracking-wider">
                      Dissonance Markers ({auditResult.dissonance_markers?.length || 0})
                    </h4>
                    {auditResult.dissonance_markers?.length > 0 ? (
                      <div className="space-y-1.5 max-h-40 overflow-y-auto pr-1">
                        {auditResult.dissonance_markers.map((m: any, idx: number) => (
                          <div key={idx} className="bg-deep-space border border-white/5 p-2 rounded text-[11px] flex justify-between items-start">
                            <div>
                              <span className="text-white/90 font-semibold">{m.marker}</span>
                              <p className="text-white/50 text-[10px] mt-0.5">{m.message}</p>
                            </div>
                            <span className={`text-[9px] px-1.5 py-0.5 rounded uppercase font-mono ${
                              m.severity === "CRITICAL" ? "bg-red-500/20 text-red-400 border border-red-500/30" :
                              m.severity === "HIGH" ? "bg-amber-500/20 text-amber-400 border border-amber-500/30" :
                              "bg-blue-500/20 text-blue-400 border border-blue-500/30"
                            }`}>
                              {m.severity}
                            </span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-white/40 text-xs italic">Zero structural or semantic dissonance markers detected.</p>
                    )}
                  </div>
                </div>
              )
            ) : null}

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setAuditItem(null)}
                className="px-4 py-1.5 bg-white/10 hover:bg-white/20 text-white rounded text-xs tracking-wider transition-colors cursor-pointer"
              >
                CLOSE
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
