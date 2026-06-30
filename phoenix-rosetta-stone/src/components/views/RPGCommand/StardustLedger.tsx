import React from "react";

interface StardustLedgerProps {
  ledger: any[];
}

export const StardustLedger: React.FC<StardustLedgerProps> = ({ ledger }) => {
  return (
    <div className="bg-panel-bg/40 border border-white/5 rounded-lg p-4 font-mono text-xs overflow-x-auto">
      <table className="w-full text-left">
        <thead>
          <tr className="border-b border-white/10 text-chrome">
            <th className="pb-2">Time</th>
            <th className="pb-2">Amount</th>
            <th className="pb-2">Type</th>
            <th className="pb-2">Reference</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-white/5 text-white/70">
          {ledger.length === 0 ? (
            <tr>
              <td colSpan={4} className="py-4 text-center text-white/30 italic">
                No stardust events recorded.
              </td>
            </tr>
          ) : (
            ledger.map((item) => (
              <tr key={item.id} className="hover:bg-white/[0.01]">
                <td className="py-2.5 text-[10px] text-white/40">
                  {item.created_at ? new Date(item.created_at).toLocaleTimeString() : "00:00"}
                </td>
                <td className={`py-2.5 font-bold ${item.amount >= 0 ? "text-green-400" : "text-red-400"}`}>
                  {item.amount >= 0 ? `+${item.amount}` : item.amount}
                </td>
                <td className="py-2.5">{item.transaction_type}</td>
                <td className="py-2.5 text-white/50">{item.reference_impact_id || "Direct Hack"}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};
