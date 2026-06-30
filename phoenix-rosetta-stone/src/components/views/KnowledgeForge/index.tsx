import React, { useState, useEffect } from "react";
import { supabase } from "@/core/supabase";
import { KnowledgeTable } from "./KnowledgeTable";
import { ForgeRecordForm } from "./ForgeRecordForm";

export const KnowledgeForgeView: React.FC = () => {
  const [knowledgeList, setKnowledgeList] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
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

  const handleCreate = async (category: string, title: string, content: string) => {
    const { error: err } = await supabase.from("knowledge_base").insert({
      title,
      category,
      content,
      meta_tags: [category.toLowerCase()],
    });

    if (err) {
      setError(err.message);
    } else {
      fetchKnowledge();
    }
  };

  const handleUpdate = async (id: number, updatedTitle: string, updatedContent: string) => {
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
          <ForgeRecordForm
            selectedEntry={selectedEntry}
            onCancelReview={() => setSelectedEntry(null)}
            onSaveReview={handleUpdate}
            onCreateEntry={handleCreate}
          />
        </div>

        {/* Database List */}
        <div className="lg:col-span-3 space-y-4">
          {error && (
            <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded text-xs font-mono">
              Database error: {error}
            </div>
          )}

          <KnowledgeTable
            data={knowledgeList}
            isLoading={isLoading}
            onSelectEntry={setSelectedEntry}
            onDeleteEntry={handleDelete}
          />
        </div>
      </div>
    </div>
  );
};
