import { knowledgeBase, KnowledgeDocument } from '../data/knowledgeBase';
import { ontologyKnowledge } from '../data/ontologyKnowledge';
import { scratchKnowledge } from '../data/scratchKnowledge';
import { whereLightFadesLore } from '../data/whereLightFadesLore';
import { create } from 'zustand';

const CUSTOM_KNOWLEDGE_STORAGE_KEY = 'phoenix_custom_knowledge_docs';

function loadCustomDocuments(): KnowledgeDocument[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = localStorage.getItem(CUSTOM_KNOWLEDGE_STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) return parsed;
    }
  } catch (err) {
    console.warn('[KnowledgeStore] Error loading custom documents from localStorage:', err);
  }
  return [];
}

function saveCustomDocuments(customDocs: KnowledgeDocument[]) {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(CUSTOM_KNOWLEDGE_STORAGE_KEY, JSON.stringify(customDocs));
  } catch (err) {
    console.warn('[KnowledgeStore] Error saving custom documents to localStorage:', err);
  }
}

const BASE_DOCUMENTS: KnowledgeDocument[] = [
  ...knowledgeBase,
  ...ontologyKnowledge,
  ...scratchKnowledge,
  ...whereLightFadesLore,
];

interface KnowledgeState {
  customDocuments: KnowledgeDocument[];
  documents: KnowledgeDocument[];

  addDocument: (doc: Omit<KnowledgeDocument, 'id'> & { id?: string }) => void;
  importFileDocument: (title: string, content: string, type?: KnowledgeDocument['type']) => void;
  removeDocument: (id: string) => void;
  updateDocument: (id: string, updated: Partial<KnowledgeDocument>) => void;
  searchDocuments: (query: string) => KnowledgeDocument[];
  resetKnowledgeStore: () => void;
}

export const useKnowledgeStore = create<KnowledgeState>((set, get) => {
  const initialCustom = loadCustomDocuments();
  const initialCombined = [...BASE_DOCUMENTS, ...initialCustom];

  return {
    customDocuments: initialCustom,
    documents: initialCombined,

    addDocument: (doc) => {
      const newDoc: KnowledgeDocument = {
        id: doc.id || `custom-doc-${Date.now()}`,
        title: doc.title,
        content: doc.content,
        type: doc.type || 'Blueprint',
      };
      set((state) => {
        const nextCustom = [newDoc, ...state.customDocuments];
        saveCustomDocuments(nextCustom);
        return {
          customDocuments: nextCustom,
          documents: [...BASE_DOCUMENTS, ...nextCustom],
        };
      });
    },

    importFileDocument: (title, content, type = 'Protocol') => {
      const uniqueSuffix = typeof crypto !== 'undefined' && crypto.randomUUID ? crypto.randomUUID().slice(0, 8) : String(Date.now());
      get().addDocument({
        id: `import-${Date.now()}-${uniqueSuffix}`,
        title,
        content,
        type,
      });
    },

    removeDocument: (id) => {
      set((state) => {
        const nextCustom = state.customDocuments.filter((d) => d.id !== id);
        saveCustomDocuments(nextCustom);
        return {
          customDocuments: nextCustom,
          documents: [...BASE_DOCUMENTS, ...nextCustom],
        };
      });
    },

    updateDocument: (id, updated) => {
      set((state) => {
        const nextCustom = state.customDocuments.map((d) => (d.id === id ? { ...d, ...updated } : d));
        saveCustomDocuments(nextCustom);
        return {
          customDocuments: nextCustom,
          documents: state.documents.map((d) => (d.id === id ? { ...d, ...updated } : d)),
        };
      });
    },

    searchDocuments: (query) => {
      const q = query.toLowerCase().trim();
      if (!q) return get().documents;

      const keywords = q.split(/\s+/).filter((k) => k.length > 2);
      return get().documents.filter((doc) => {
        const titleLower = doc.title.toLowerCase();
        const contentLower = doc.content.toLowerCase();
        return titleLower.includes(q) || keywords.some((k) => contentLower.includes(k));
      });
    },

    resetKnowledgeStore: () => {
      saveCustomDocuments([]);
      set({
        customDocuments: [],
        documents: [...BASE_DOCUMENTS],
      });
    },
  };
});
