import React from "react";
import { DataTable } from "@/components/ui/DataTable";
import { LivePill } from "@/components/ui/LivePill";

interface KnowledgeTableProps {
    data: any[];
    isLoading: boolean;
    onSelectEntry: (entry: any) => void;
    onDeleteEntry: (id: number) => Promise<void>;
}

export const KnowledgeTable: React.FC<KnowledgeTableProps> = ({
    data,
    isLoading,
    onSelectEntry,
    onDeleteEntry,
}) => {
    const columns = [
        {
            header: "ID",
            accessor: (row: any) => <span className="text-white/40">#{row.id}</span>,
            className: "w-12",
        },
        {
            header: "Category",
            accessor: (row: any) => <LivePill label={row.category || "General"} type="info" />,
            className: "w-28",
        },
        {
            header: "Title",
            accessor: (row: any) => <span className="font-bold text-white/90">{row.title}</span>,
        },
        {
            header: "Modified",
            accessor: (row: any) => (
                <span className="text-[10px] text-white/40">
                    {row.updated_at ? new Date(row.updated_at).toLocaleDateString() : "Never"}
                </span>
            ),
            className: "w-24",
        },
        {
            header: "Actions",
            accessor: (row: any) => (
                <div className="flex items-center gap-2">
                    <button
                        onClick={() => onSelectEntry(row)}
                        className="px-2 py-0.5 border border-white/10 hover:border-celestial-blue/40 rounded bg-white/5 hover:bg-celestial-blue/10 text-[10px] text-white/50 hover:text-celestial-blue transition-colors cursor-pointer"
                    >
                        Review
                    </button>
                    <button
                        onClick={() => onDeleteEntry(row.id)}
                        className="px-2 py-0.5 border border-white/10 hover:border-red-500/40 rounded bg-white/5 hover:bg-red-500/10 text-[10px] text-white/50 hover:text-red-500 transition-colors cursor-pointer"
                    >
                        Purge
                    </button>
                </div>
            ),
            className: "w-32",
        },
    ];

    return (
        <DataTable
            data={data}
            columns={columns}
            isLoading={isLoading}
            emptyMessage="No canonical records detected in registry."
        />
    );
};
