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
    archive,
    remove,
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

  const columns = [
    {
      header: "ID",
      accessor: (row: any) => <span className="text-[10px] text-white/40">#{row.id}</span>,
      className: "w-12",
    },
    {
      header: "Domain",
      accessor: (row: any) => <LivePill label={row.domain} type="info" />,
      className: "w-28",
    },
    {
      header: "Memory Content",
      accessor: (row: any) => <span className="font-sans text-xs text-white/90 break-words">{row.content}</span>,
    },
    {
      header: "Layer",
      accessor: (row: any) => <span className="text-white/60">L{row.memory_layer ?? 1}</span>,
      className: "w-16",
    },
    {
      header: "State",
      accessor: (row: any) => {
        let type: "active" | "fading" | "consolidated" | "archived" = "active";
        if (row.state === "Fading") type = "fading";
        if (row.state === "Consolidated") type = "consolidated";
        if (row.state === "Archived") type = "archived";
        return <LivePill label={row.state} type={type} />;
      },
      className: "w-24",
    },
    {
      header: "Actions",
      accessor: (row: any) => (
        <div className="flex items-center gap-2">
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
      className: "w-32",
    },
  ];

  return (
    <div className="space-y-6 animate-appear">
      {/* View Header */}
      <div className="flex items-center justify-between border-b border-white/5 pb-4">
        <div>
          <h2 className="text-sm font-bold tracking-[0.25em] text-white uppercase">
            MEMORY PALACE
          </h2>
          <p className="text-[11px] text-white/40 font-mono mt-0.5">
            Full-spectrum CRUD access to the memory_entries cognitive records
          </p>
        </div>
        <div className="text-right font-mono text-[10px] text-white/40">
          Total Nodes: <span className="text-celestial-blue font-bold">{total}</span>
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
    </div>
  );
};
