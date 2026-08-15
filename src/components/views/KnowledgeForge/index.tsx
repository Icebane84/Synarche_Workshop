// [OMEGA AST Cleaned]: Tokenized design standards applied.
import React, { useState } from 'react';
import { useKnowledgeStore } from '../../../store/knowledgeStore';
import { KnowledgeDocument } from '../../../data/knowledgeBase';
import { BookOpen, FileUp, Search, Trash2, Plus, Edit2, RotateCcw, Check, Database } from 'lucide-react';

export const KnowledgeForgeView: React.FC = () => {
  const documents = useKnowledgeStore((state) => state.documents);
  const addDocument = useKnowledgeStore((state) => state.addDocument);
  const importFileDocument = useKnowledgeStore((state) => state.importFileDocument);
  const removeDocument = useKnowledgeStore((state) => state.removeDocument);
  const updateDocument = useKnowledgeStore((state) => state.updateDocument);
  const resetKnowledgeStore = useKnowledgeStore((state) => state.resetKnowledgeStore);

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [selectedDoc, setSelectedDoc] = useState<KnowledgeDocument | null>(null);

  // Authoring Form state
  const [newTitle, setNewTitle] = useState('');
  const [newType, setNewType] = useState<KnowledgeDocument['type']>('Protocol');
  const [newContent, setNewContent] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [notification, setNotification] = useState<string | null>(null);

  const categories = ['All', 'Codex', 'Protocol', 'Blueprint', 'Code', 'Log'];

  const filteredDocs = documents.filter((doc) => {
    const matchesCategory = selectedCategory === 'All' || doc.type === selectedCategory;
    const matchesSearch =
      !searchQuery.trim() ||
      doc.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      doc.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
      doc.id.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const handleSelectDoc = (doc: KnowledgeDocument) => {
    setSelectedDoc(doc);
    setNewTitle(doc.title);
    setNewType(doc.type);
    setNewContent(doc.content);
    setIsEditing(true);
  };

  const handleCancelEdit = () => {
    setSelectedDoc(null);
    setNewTitle('');
    setNewType('Protocol');
    setNewContent('');
    setIsEditing(false);
  };

  const handleSaveDoc = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newContent.trim()) return;

    if (isEditing && selectedDoc) {
      updateDocument(selectedDoc.id, {
        title: newTitle.trim(),
        type: newType,
        content: newContent.trim(),
      });
      setNotification(`Updated Knowledge Record: "${newTitle.trim()}"`);
    } else {
      addDocument({
        title: newTitle.trim(),
        type: newType,
        content: newContent.trim(),
      });
      setNotification(`Canonized New Substrate Record: "${newTitle.trim()}"`);
    }

    setTimeout(() => setNotification(null), 3000);
    handleCancelEdit();
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target?.result as string;
      if (text) {
        const titleName = file.name.replace(/\.[^/.]+$/, '');
        const type: KnowledgeDocument['type'] = file.name.endsWith('.md')
          ? 'Protocol'
          : file.name.endsWith('.json')
          ? 'Blueprint'
          : 'Code';
        importFileDocument(`Imported: ${titleName}`, text, type);
        setNotification(`Successfully imported local knowledge file "${file.name}" into RAG memory.`);
        setTimeout(() => setNotification(null), 4000);
      }
    };
    reader.readAsText(file);
    e.target.value = '';
  };

  return (
    <div className="space-y-6 animate-appear font-mono select-text">
      {/* Top Header */}
      <div className="flex flex-wrap items-center justify-between border-b border-white/10 pb-4 gap-4">
        <div>
          <div className="flex items-center gap-2">
            <Database size={20} className="text-cyan-400 animate-pulse" />
            <h2 className="text-sm font-bold tracking-[0.25em] text-cyan-300 uppercase">
              SOVEREIGN KNOWLEDGE FORGE & RAG SUBSTRATE
            </h2>
          </div>
          <p className="text-[11px] text-white/50 font-mono mt-1">
            Active Neural Knowledge Base: {documents.length} canonized records indexed for local & vector AI retrieval
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* File Import Button */}
          <label className="flex items-center gap-2 px-3 py-1.5 bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-400/40 rounded text-cyan-200 text-xs font-mono cursor-pointer transition-all hover:shadow-[0_0_10px_rgba(100,220,255,0.4)]">
            <FileUp size={14} />
            <span>Import Local File (.md / .json)</span>
            <input type="file" accept=".md,.json,.txt,.ts" onChange={handleFileUpload} className="hidden" />
          </label>

          {/* Seed Supabase Button */}
          <button
            onClick={async () => {
              try {
                const { supabase } = await import('../../../services/supabaseClient');
                setNotification('Seeding Supabase tables (knowledge_base, documents, memory_entries)...');

                const seedPayload = documents.map((doc) => ({
                  id: doc.id,
                  title: doc.title,
                  content: doc.content,
                  metadata: { category: doc.type, tags: [doc.type.toLowerCase()] },
                }));

                const { error: kbErr } = await supabase.from('knowledge_base').upsert(seedPayload);
                if (kbErr) {
                  setNotification(`Supabase Note: ${kbErr.message}. Ensure SQL migration 001 is run to unlock RLS.`);
                } else {
                  setNotification(`Successfully seeded ${seedPayload.length} records directly into Supabase!`);
                }
              } catch (err) {
                setNotification(`Seed Error: ${err instanceof Error ? err.message : String(err)}`);
              }
              setTimeout(() => setNotification(null), 6000);
            }}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-500/20 hover:bg-indigo-500/30 border border-indigo-400/40 rounded text-indigo-200 text-xs font-mono transition-all hover:shadow-[0_0_10px_rgba(129,140,248,0.4)]"
            title="Seed local knowledge substrate directly into Supabase backend"
          >
            <Database size={13} />
            <span>Seed Supabase</span>
          </button>

          <button
            onClick={resetKnowledgeStore}
            className="flex items-center gap-1 px-2.5 py-1.5 bg-white/5 hover:bg-red-500/20 border border-white/10 hover:border-red-500/30 rounded text-white/60 hover:text-red-300 text-xs font-mono transition-all"
            title="Reset Knowledge Store to factory canonical defaults"
          >
            <RotateCcw size={13} />
            <span>Reset Defaults</span>
          </button>
        </div>
      </div>

      {notification && (
        <div className="p-3 bg-cyan-950/80 border border-cyan-500/40 rounded-lg text-cyan-200 text-xs flex items-center gap-2 animate-fade-in-sm">
          <Check size={14} className="text-cyan-400" />
          <span>{notification}</span>
        </div>
      )}

      {/* Main Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Authoring & Review Form */}
        <div className="bg-panel-bg/40 border border-white/10 p-5 rounded-xl space-y-4 shadow-xl">
          <div className="flex items-center justify-between border-b border-white/10 pb-2">
            <h3 className="text-xs font-semibold tracking-wider text-cyan-300 uppercase flex items-center gap-1.5">
              {isEditing ? <Edit2 size={13} /> : <Plus size={13} />}
              {isEditing ? 'Review / Edit Record' : 'Author Canonical Record'}
            </h3>
            {isEditing && (
              <button
                onClick={handleCancelEdit}
                className="text-[10px] text-white/40 hover:text-white transition-colors"
              >
                Cancel
              </button>
            )}
          </div>

          <form onSubmit={handleSaveDoc} className="space-y-3">
            <div>
              <label className="text-[10px] text-white/50 block mb-1">Document Title</label>
              <input
                type="text"
                value={newTitle}
                onChange={(e) => setNewTitle(e.target.value)}
                placeholder="e.g. Systemic Ontology: Law 44"
                className="w-full bg-black/40 border border-white/15 rounded p-2 text-xs text-cyan-100 placeholder-white/20 focus:outline-none focus:border-cyan-400"
                required
              />
            </div>

            <div>
              <label className="text-[10px] text-white/50 block mb-1">Category Type</label>
              <select
                value={newType}
                onChange={(e) => setNewType(e.target.value as KnowledgeDocument['type'])}
                className="w-full bg-black/40 border border-white/15 rounded p-2 text-xs text-cyan-100 focus:outline-none focus:border-cyan-400"
              >
                <option value="Codex">Codex (Laws & Ethos)</option>
                <option value="Protocol">Protocol (Standards)</option>
                <option value="Blueprint">Blueprint (Architecture)</option>
                <option value="Code">Code (Types & Engine)</option>
                <option value="Log">Log (Evolution History)</option>
              </select>
            </div>

            <div>
              <label className="text-[10px] text-white/50 block mb-1">Record Content (Markdown / Text)</label>
              <textarea
                value={newContent}
                onChange={(e) => setNewContent(e.target.value)}
                placeholder="Paste canonical rules, blueprints, or ontology definitions..."
                rows={8}
                className="w-full bg-black/40 border border-white/15 rounded p-2 text-xs text-cyan-100 placeholder-white/20 focus:outline-none focus:border-cyan-400 font-sans resize-none"
                required
              />
            </div>

            <div className="flex items-center gap-2 pt-2">
              <button
                type="submit"
                className="flex-1 py-2 bg-cyan-500/20 hover:bg-cyan-500/40 border border-cyan-400/50 rounded text-cyan-200 text-xs font-mono transition-all hover:shadow-[0_0_10px_rgba(100,220,255,0.4)]"
              >
                {isEditing ? 'Save Re-alignment' : 'Canonize to Memory'}
              </button>
              {isEditing && selectedDoc && (
                <button
                  type="button"
                  onClick={() => {
                    if (confirm(`Purge record "${selectedDoc.title}" from Knowledge Store?`)) {
                      removeDocument(selectedDoc.id);
                      handleCancelEdit();
                    }
                  }}
                  className="p-2 bg-red-500/10 hover:bg-red-500/30 border border-red-500/30 rounded text-red-300 text-xs"
                  title="Purge Document"
                >
                  <Trash2 size={14} />
                </button>
              )}
            </div>
          </form>
        </div>

        {/* Right 2 Columns: Knowledge Records Explorer */}
        <div className="lg:col-span-2 space-y-4">
          {/* Search & Category Filter Bar */}
          <div className="flex flex-wrap items-center justify-between gap-3 bg-panel-bg/40 border border-white/10 p-3 rounded-xl">
            <div className="flex items-center gap-2 bg-black/40 border border-white/10 px-3 py-1.5 rounded-lg flex-1 min-w-[200px]">
              <Search size={14} className="text-white/40" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search canonical substrate..."
                className="bg-transparent text-xs text-cyan-100 placeholder-white/30 focus:outline-none w-full"
              />
            </div>

            <div className="flex items-center gap-1 overflow-x-auto">
              {categories.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setSelectedCategory(cat)}
                  className={`text-[11px] px-2.5 py-1 rounded transition-colors ${
                    selectedCategory === cat
                      ? 'bg-cyan-500/30 border border-cyan-400 text-cyan-200 font-bold'
                      : 'bg-white/5 border border-white/10 text-white/50 hover:text-white'
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>

          {/* Document Cards List */}
          <div className="space-y-3 max-h-[600px] overflow-y-auto pr-1 scrollbar-thin scrollbar-thumb-white/10">
            {filteredDocs.length === 0 ? (
              <div className="p-8 bg-black/20 border border-white/5 rounded-xl text-center text-xs text-white/30 italic">
                No substrate documents matched search criteria.
              </div>
            ) : (
              filteredDocs.map((doc) => (
                <div
                  key={doc.id}
                  className={`p-4 rounded-xl border transition-all ${
                    selectedDoc?.id === doc.id
                      ? 'bg-cyan-950/40 border-cyan-400/60 shadow-[0_0_15px_rgba(100,220,255,0.15)]'
                      : 'bg-panel-bg/30 border-white/10 hover:border-white/20'
                  }`}
                >
                  <div className="flex items-start justify-between gap-4 mb-2">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] px-2 py-0.5 rounded bg-cyan-500/20 border border-cyan-400/30 text-cyan-300 font-mono">
                          {doc.type}
                        </span>
                        <h4 className="text-xs font-bold text-white/90">{doc.title}</h4>
                      </div>
                      <span className="text-[9px] text-white/30 font-mono block mt-1">ID: {doc.id}</span>
                    </div>

                    <button
                      onClick={() => handleSelectDoc(doc)}
                      className="px-2.5 py-1 bg-white/5 hover:bg-cyan-500/20 border border-white/10 hover:border-cyan-400/40 rounded text-[10px] text-white/60 hover:text-cyan-200 transition-colors"
                    >
                      Review / Edit
                    </button>
                  </div>

                  <p className="text-[11px] text-white/70 line-clamp-3 font-sans leading-relaxed whitespace-pre-wrap">
                    {doc.content}
                  </p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
