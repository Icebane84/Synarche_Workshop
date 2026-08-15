// [OMEGA AST Cleaned]: Tokenized design standards applied.
import { KnowledgeDocument } from './knowledgeBase';
import adjacencyMatrixData from './adjacency_matrix.json';

/**
 * @fileoverview Where Light Fades: Ashen Oath Lore Substrate.
 * Parses the 220-node & 858-edge Ashen Genesis adjacency graph
 * directly into canonical RAG documents.
 */

export interface AshenNode {
  id: string;
  label?: string;
  name?: string;
  properties?: Record<string, any>;
}

export interface AshenEdge {
  source: string;
  target: string;
  relation: string;
  properties?: Record<string, any>;
}

function buildLoreDocuments(): KnowledgeDocument[] {
  const docs: KnowledgeDocument[] = [];

  const rawNodes = (adjacencyMatrixData as any).nodes;
  const rawEdges = (adjacencyMatrixData as any).edges;

  let nodesList: AshenNode[] = [];
  let edgesList: AshenEdge[] = [];

  if (Array.isArray(rawNodes)) {
    nodesList = rawNodes;
  } else if (rawNodes && typeof rawNodes === 'object') {
    nodesList = Object.values(rawNodes);
  }

  if (Array.isArray(rawEdges)) {
    edgesList = rawEdges;
  }

  // 1. Ingest Main Character & Faction Nodes
  const characterDocs: KnowledgeDocument[] = nodesList
    .filter((n) => n.label === 'Character' || n.label === 'Faction' || n.label === 'Location' || n.label === 'Item')
    .map((n) => {
      const propLines = n.properties
        ? Object.entries(n.properties)
            .map(([k, v]) => `- **${k}**: ${typeof v === 'object' ? JSON.stringify(v) : v}`)
            .join('\n')
        : '';

      const connectedEdges = edgesList
        .filter((e) => e.source === n.id || e.target === n.id)
        .slice(0, 10)
        .map((e) => `- ${e.source} --[${e.relation}]--> ${e.target} ${e.properties?.notes ? `(${e.properties.notes})` : ''}`)
        .join('\n');

      return {
        id: `WLF-NODE-${n.id}`,
        title: `Where Light Fades: ${n.name || n.id} (${n.label || 'Entity'})`,
        type: (n.label === 'Character' ? 'Codex' : 'Blueprint') as KnowledgeDocument['type'],
        content: `
# Where Light Fades Substrate: ${n.name || n.id}
- **Entity ID**: ${n.id}
- **Type**: ${n.label || 'Unknown'}

## Properties & Lore Attributes
${propLines || 'Canonical active entity in Ashen Oath graph.'}

## Knowledge Graph Relations
${connectedEdges || 'No explicit edge connections recorded.'}
`,
      };
    });

  // 2. Master Ashen Oath World Overview
  const worldDoc: KnowledgeDocument = {
    id: 'WHERE_LIGHT_FADES_ASHEN_OATH_OVERVIEW',
    title: 'Where Light Fades: Ashen Oath Master World Canon & Adjacency Graph',
    type: 'Codex',
    content: `
# WHERE LIGHT FADES: ASHEN OATH MASTER CANON

## 1. World Summary & Narrative Core
In the realm of Where Light Fades, the world is consumed by The Stain, spectral corruption, and shadow entities.
Key protagonists and factions fight to maintain internal poise and honor the Ashen Oath:
- **Kaelen (Volatile Vanguard)**: Wielder of Oathbringer, struggling against his dark inner Shadow Self.
- **Serafina (Warden of White Flame)**: Projects Consecrated Circles to burn spectral corruption and stabilize party poise.
- **Eldrin (Prisoner to Ally)**: Transmutes arcana and achieves Grace in Act 2.
- **Brother Malakor & Valerius (Architect of Chains)**: Antagonistic forces orchestrating the Architecture of Flesh and Silent Spire trials.
- **Garrett (Tactical Pragmatist)**: Coats twin blades in Burning Steel Alchemical Oil.

## 2. Adjacency Graph Metrics
- Total Nodes: ${nodesList.length}
- Total Edges: ${edgesList.length}
- Primary Factions: Silent Spire, Ashen Order, Shadow Vanguard.
`,
  };

  docs.push(worldDoc);
  docs.push(...characterDocs.slice(0, 50)); // Include top 50 detailed character & item nodes

  return docs;
}

export const whereLightFadesLore: KnowledgeDocument[] = buildLoreDocuments();
