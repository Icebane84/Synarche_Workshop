import React from "react";
import { DataTable } from "@components/ui/DataTable";
import { LivePill } from "@components/ui/LivePill";

interface MemoryTableProps {
    memories: any[];
    isLoading: boolean;
    updateState: (id: number, state: any) => Promise<void>;
    archive: (id: number) => Promise<void>;
    remove: (id: number) => Promise<void>;
    onTestResonance: (row: any) => Promise<void>;
}

export const MemoryTable: React.FC<MemoryTableProps> = ({
    memories,
    isLoading,
    updateState,
    archive,
    remove,
    onTestResonance,
}) => {
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
                        onClick={() => onTestResonance(row)}
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
        <DataTable
            data={memories}
            columns={columns}
            isLoading={isLoading}
            emptyMessage="No matching memory records detected."
        />
    );
};
