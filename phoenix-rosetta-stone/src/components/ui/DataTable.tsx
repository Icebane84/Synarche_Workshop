import React from "react";

interface Column<T> {
  header: string;
  accessor: (row: T) => React.ReactNode;
  sortKey?: string;
  className?: string;
}

interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  isLoading?: boolean;
  emptyMessage?: string;
  onRowClick?: (row: T) => void;
}

export function DataTable<T>({
  data,
  columns,
  isLoading = false,
  emptyMessage = "No records found.",
  onRowClick,
}: DataTableProps<T>) {
  return (
    <div className="w-full overflow-x-auto border border-white/5 bg-panel-bg/30 rounded-lg">
      <table className="w-full text-left border-collapse font-mono text-xs select-none">
        <thead>
          <tr className="border-b border-white/10 bg-white/[0.01]">
            {columns.map((col, idx) => (
              <th
                key={idx}
                className={`py-3 px-4 text-chrome uppercase tracking-wider ${col.className || ""}`}
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-white/5">
          {isLoading ? (
            <tr>
              <td colSpan={columns.length} className="py-8 text-center text-white/30 animate-pulse">
                Synchronizing data matrix...
              </td>
            </tr>
          ) : data.length === 0 ? (
            <tr>
              <td colSpan={columns.length} className="py-8 text-center text-white/30 italic">
                {emptyMessage}
              </td>
            </tr>
          ) : (
            data.map((row, rowIdx) => (
              <tr
                key={rowIdx}
                onClick={() => onRowClick?.(row)}
                className={`transition-colors group ${
                  onRowClick ? "cursor-pointer hover:bg-white/[0.02]" : "hover:bg-white/[0.01]"
                }`}
              >
                {columns.map((col, colIdx) => (
                  <td key={colIdx} className={`py-3 px-4 text-white/80 ${col.className || ""}`}>
                    {col.accessor(row)}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
