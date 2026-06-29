import React, { useState, useEffect } from "react";
import { supabase } from "@/core/supabase";
import { DataTable } from "@/components/ui/DataTable";
import { LivePill } from "@/components/ui/LivePill";

export const KnowledgeForgeView: React.FC = () => {
  const [knowledgeList, setKnowledgeList] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form input states
  const [newTitle, setNewTitle] = useState("");
  const [newCategory, setNewCategory] = useState("Axiom");
  const [newContent, setNewContent] = useState("");
  const [isSaving, setIsSaving] = useState(false);

  // Selected entry for detailed view or editing
  const [selectedEntry, setSelectedEntry] = useState<any | null>(null);

  const fetchKnowledge = async () => {
    setIsLoading(true);
    const { data, error: err } = await supabase
      .from("knowledge_base")
      .select("*")
      .order("updated_at", { ascending: false });

    if (err) setError(err.message);
    else setKnowledgeList(data ?? []);
    setIsLoading(false);
  };

  useEffect(() => {
    fetchKnowledge();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newContent.trim()) return;

    setIsSaving(true);
    const { error: err } = await supabase.from("knowledge_base").insert({
      title: newTitle,
      category: newCategory,
      content: newContent,
      meta_tags: [newCategory.toLowerCase()],
    });

    if (err) {
      setError(err.message);
    } else {
      setNewTitle("");
      setNewContent("");
      fetchKnowledge();
    }
    setIsSaving(false);
  };

  const handleUpdate = async (id: number, updatedTitle: string, updatedContent: string) => {
    setIsSaving(true);
    const { error: err } = await supabase
      .from("knowledge_base")
      .update({
        title: updatedTitle,
        content: updatedContent,
      })
      .eq("id", id);

    if (err) {
      setError(err.message);
    } else {
      setSelectedEntry(null);
      fetchKnowledge();
    }
    setIsSaving(false);
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this knowledge block?")) return;
    const { error: err } = await supabase.from("knowledge_base").delete().eq("id", id);
    if (err) setError(err.message);
    else {
      setSelectedEntry(null);
      fetchKnowledge();
    }
  };

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
            onClick={() => setSelectedEntry(row)}
            className="px-2 py-0.5 border border-white/10 hover:border-celestial-blue/40 rounded bg-white/5 hover:bg-celestial-blue/10 text-[10px] text-white/50 hover:text-celestial-blue transition-colors cursor-pointer"
          >
            Review
          </button>
          <button
            onClick={() => handleDelete(row.id)}
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
    <div className="space-y-6 animate-appear">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-white/5 pb-4">
        <div>
          <h2 className="text-sm font-bold tracking-[0.25em] text-white uppercase">
            KNOWLEDGE FORGE
          </h2>
          <p className="text-[11px] text-white/40 font-mono mt-0.5">
            Synchronize, review, and author canonical substrate records
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Authoring & Review Form panel */}
        <div className="bg-panel-bg/40 border border-white/5 p-4 rounded-lg space-y-4 font-mono">
          {selectedEntry ? (
            <div className="space-y-3">
              <h3 className="text-xs font-semibold text-celestial-blue uppercase tracking-wider">
                REVIEW CANONICAL NODE
              </h3>
              <div>
                <label className="block text-[10px] text-chrome mb-1">Title</label>
                <input
                  type="text"
                  value={selectedEntry.title}
                  onChange={(e) => setSelectedEntry({ ...selectedEntry, title: e.target.value })}
                  className="w-full bg-deep-space border border-white/10 rounded px-2.5 py-1.5 text-xs text-white/80 focus:border-celestial-blue/50 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-[10px] text-chrome mb-1">Content</label>
                <textarea
                  value={selectedEntry.content}
                  onChange={(e) => setSelectedEntry({ ...selectedEntry, content: e.target.value })}
                  rows={8}
                  className="w-full bg-deep-space border border-white/10 rounded px-2.5 py-1.5 text-xs text-white/80 focus:border-celestial-blue/50 focus:outline-none font-sans"
                />
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => handleUpdate(selectedEntry.id, selectedEntry.title, selectedEntry.content)}
                  disabled={isSaving}
                  className="flex-1 py-1.5 bg-green-500/10 hover:bg-green-500/20 border border-green-500/30 text-green-400 rounded text-xs tracking-wider font-semibold cursor-pointer"
                >
                  SAVE
                </button>
                <button
                  onClick={() => setSelectedEntry(null)}
                  className="px-3 py-1.5 bg-white/5 border border-white/10 rounded text-xs text-white/50 hover:text-white cursor-pointer"
                >
                  CANCEL
                </button>
              </div>
            </div>
          ) : (
            <form onSubmit={handleCreate} className="space-y-3">
              <h3 className="text-xs font-semibold text-white/70 uppercase tracking-wider">
                FORGE CANONICAL RECORD
              </h3>
              <div>
                <label className="block text-[10px] text-chrome mb-1">Category</label>
                <select
                  value={newCategory}
                  onChange={(e) => setNewCategory(e.target.value)}
                  className="w-full bg-deep-space border border-white/10 rounded px-2.5 py-1.5 text-xs text-white/80 focus:border-celestial-blue/50 focus:outline-none"
                >
                  <option value="Axiom">Axiom</option>
                  <option value="Epistemic">Epistemic</option>
                  <option value="Protocol">Protocol</option>
                  <option value="System">System</option>
                </select>
              </div>
              <div>
                <label className="block text-[10px] text-chrome mb-1">Title</label>
                <input
                  type="text"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  placeholder="Record label/title"
                  className="w-full bg-deep-space border border-white/10 rounded px-2.5 py-1.5 text-xs text-white/80 focus:border-celestial-blue/50 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-[10px] text-chrome mb-1">Body Text</label>
                <textarea
                  value={newContent}
                  onChange={(e) => setNewContent(e.target.value)}
                  placeholder="Detailed cognitive knowledge context..."
                  rows={6}
                  className="w-full bg-deep-space border border-white/10 rounded px-2.5 py-1.5 text-xs text-white/80 focus:border-celestial-blue/50 focus:outline-none font-sans"
                />
              </div>
              <button
                type="submit"
                disabled={isSaving || !newTitle.trim() || !newContent.trim()}
                className="w-full py-2 bg-celestial-blue/15 hover:bg-celestial-blue/25 border border-celestial-blue/40 hover:border-celestial-blue/60 text-celestial-blue rounded text-xs tracking-widest font-semibold cursor-pointer"
              >
                {isSaving ? "FORGING..." : "FORGE CANON"}
              </button>
            </form>
          )}
        </div>

        {/* Database List */}
        <div className="lg:col-span-3 space-y-4">
          {error && (
            <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded text-xs font-mono">
              Database error: {error}
            </div>
          )}

          <DataTable
            data={knowledgeList}
            columns={columns}
            isLoading={isLoading}
            emptyMessage="No canonical records detected in registry."
          />
        </div>
      </div>
    </div>
  );
};
