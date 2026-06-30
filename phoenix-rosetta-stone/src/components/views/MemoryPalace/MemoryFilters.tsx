import React from "react";

interface MemoryFiltersProps {
    domainFilter: string;
    stateFilter: string;
    searchFilter: string;
    onFilterChange: (domain: string, state: string, search: string) => void;
}

export const MemoryFilters: React.FC<MemoryFiltersProps> = ({
    domainFilter,
    stateFilter,
    searchFilter,
    onFilterChange,
}) => {
    return (
        <div className="flex flex-wrap gap-3 bg-panel-bg/20 border border-white/5 p-3 rounded-lg font-mono text-xs">
            <div className="flex items-center gap-2">
                <span className="text-white/40">Domain:</span>
                <select
                    value={domainFilter}
                    onChange={(e) => onFilterChange(e.target.value, stateFilter, searchFilter)}
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
                    onChange={(e) => onFilterChange(domainFilter, e.target.value, searchFilter)}
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
                    onChange={(e) => onFilterChange(domainFilter, stateFilter, e.target.value)}
                    placeholder="Search memory text..."
                    className="w-full bg-transparent border-none py-1 focus:outline-none text-white/80 text-xs font-sans"
                />
            </div>
        </div>
    );
};
