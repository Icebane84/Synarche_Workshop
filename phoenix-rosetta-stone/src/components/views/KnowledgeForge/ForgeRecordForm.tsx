import React, { useState, useEffect } from "react";

interface ForgeRecordFormProps {
    selectedEntry: any | null;
    onCancelReview: () => void;
    onSaveReview: (id: number, title: string, content: string) => Promise<void>;
    onCreateEntry: (category: string, title: string, content: string) => Promise<void>;
}

export const ForgeRecordForm: React.FC<ForgeRecordFormProps> = ({
    selectedEntry,
    onCancelReview,
    onSaveReview,
    onCreateEntry,
}) => {
    // Form input states
    const [newTitle, setNewTitle] = useState("");
    const [newCategory, setNewCategory] = useState("Axiom");
    const [newContent, setNewContent] = useState("");
    const [isSaving, setIsSaving] = useState(false);

    // Edit states (for review panel)
    const [editTitle, setEditTitle] = useState("");
    const [editContent, setEditContent] = useState("");

    useEffect(() => {
        if (selectedEntry) {
            setEditTitle(selectedEntry.title || "");
            setEditContent(selectedEntry.content || "");
        }
    }, [selectedEntry]);

    const handleSubmitCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newTitle.trim() || !newContent.trim()) return;

        setIsSaving(true);
        try {
            await onCreateEntry(newCategory, newTitle, newContent);
            setNewTitle("");
            setNewContent("");
        } catch (err) {
            console.error(err);
        } finally {
            setIsSaving(false);
        }
    };

    const handleSaveEdit = async () => {
        if (!selectedEntry) return;
        setIsSaving(true);
        try {
            await onSaveReview(selectedEntry.id, editTitle, editContent);
        } catch (err) {
            console.error(err);
        } finally {
            setIsSaving(false);
        }
    };

    if (selectedEntry) {
        return (
            <div className="space-y-3 font-mono">
                <h3 className="text-xs font-semibold text-celestial-blue uppercase tracking-wider">
                    REVIEW CANONICAL NODE
                </h3>
                <div>
                    <label className="block text-[10px] text-chrome mb-1">Title</label>
                    <input
                        type="text"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        className="w-full bg-deep-space border border-white/10 rounded px-2.5 py-1.5 text-xs text-white/80 focus:border-celestial-blue/50 focus:outline-none"
                    />
                </div>
                <div>
                    <label className="block text-[10px] text-chrome mb-1">Content</label>
                    <textarea
                        value={editContent}
                        onChange={(e) => setEditContent(e.target.value)}
                        rows={8}
                        className="w-full bg-deep-space border border-white/10 rounded px-2.5 py-1.5 text-xs text-white/80 focus:border-celestial-blue/50 focus:outline-none font-sans"
                    />
                </div>
                <div className="flex gap-2">
                    <button
                        onClick={handleSaveEdit}
                        disabled={isSaving || !editTitle.trim() || !editContent.trim()}
                        className="flex-1 py-1.5 bg-green-500/10 hover:bg-green-500/20 border border-green-500/30 text-green-400 rounded text-xs tracking-wider font-semibold cursor-pointer"
                    >
                        {isSaving ? "SAVING..." : "SAVE"}
                    </button>
                    <button
                        onClick={onCancelReview}
                        className="px-3 py-1.5 bg-white/5 border border-white/10 rounded text-xs text-white/50 hover:text-white cursor-pointer"
                    >
                        CANCEL
                    </button>
                </div>
            </div>
        );
    }

    return (
        <form onSubmit={handleSubmitCreate} className="space-y-3 font-mono">
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
    );
};
