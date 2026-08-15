import { createClient } from '@supabase/supabase-js';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const SUPABASE_URL = process.env.VITE_SUPABASE_URL || 'https://rtjkhpotguwngfpvhfej.supabase.co';
const SUPABASE_KEY = process.env.VITE_SUPABASE_ANON_KEY || 'sb_publishable_APS-_w0TK4EeBkvmoRu5Zw_1nEsOLiD';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

async function seedSupabase() {
  console.log('🚀 Starting Sovereign Supabase Database Seed Protocol...');
  console.log(`Target Supabase URL: ${SUPABASE_URL}`);

  // 1. Load Adjacency Matrix Nodes for memory_entries
  const matrixPath = path.join(__dirname, '../src/data/adjacency_matrix.json');
  let adjacencyData = { nodes: [] };
  if (fs.existsSync(matrixPath)) {
    adjacencyData = JSON.parse(fs.readFileSync(matrixPath, 'utf8'));
  }

  const rawNodes = Array.isArray(adjacencyData.nodes)
    ? adjacencyData.nodes
    : Object.values(adjacencyData.nodes || {});

  console.log(`\n📦 Found ${rawNodes.length} nodes from Ashen Oath Adjacency Matrix.`);

  // Prepare memory_entries payloads with unique content_hash
  const memoryEntries = rawNodes.map((n, idx) => {
    const textContent = `${n.name || n.id} (${n.label || 'Entity'}): ${n.properties?.description || n.properties?.role || 'Ashen Oath Substrate Node'}`;
    const hash = crypto.createHash('md5').update(`${textContent}-${idx}`).digest('hex');

    return {
      content: textContent,
      content_hash: hash,
      domain: n.label || 'General',
      memory_layer: 2,
      tags: [n.label?.toLowerCase() || 'general', ...(n.aliases || [])],
      activation_score: 0.85,
      state: 'Active',
    };
  });

  if (memoryEntries.length > 0) {
    console.log(`Seeding ${memoryEntries.length} items into 'memory_entries' table...`);
    for (let i = 0; i < memoryEntries.length; i += 25) {
      const batch = memoryEntries.slice(i, i + 25);
      const { error } = await supabase.from('memory_entries').insert(batch);
      if (error) {
        console.warn(`[memory_entries] Batch ${Math.floor(i / 25) + 1} Note:`, error.message);
      }
    }
    console.log('✅ memory_entries seeding completed.');
  }

  // 2. Seed knowledge_base table (schema: id, title, content, metadata)
  const knowledgeSeedRecords = [
    {
      id: 'PHOENIX_PROTOCOL_BLUEPRINT',
      title: 'The Phoenix Protocol (Architecture)',
      content: 'The Phoenix Protocol defines the component-driven cognitive architecture of the Rosetta Stone system.',
      metadata: { category: 'Protocol', tags: ['protocol', 'architecture'] },
    },
    {
      title: 'The Phoenix Codex (43-Law Codex v15.1)',
      id: 'PHOENIX_CODEX_V15_1',
      content: 'Law 01: Struggle. Law 02: Naming. Law 03: Failure as Fuel. Law 04: Cognitive Loom. Law 11: NIM Detection.',
      metadata: { category: 'Codex', tags: ['codex', 'governance'] },
    },
    {
      title: 'UMB-LEX-001: The Master Lexicon & Rosetta Stone Concordance',
      id: 'UMB_LEX_001',
      content: 'Master concordance mapping Phoenix Rosetta Stone (PRS-001), Dissonance Quests, Actionable Prompt Packets, and NIM.',
      metadata: { category: 'Protocol', tags: ['lexicon', 'concordance'] },
    },
    {
      title: 'Where Light Fades: Ashen Oath Master Lore Substrate',
      id: 'WHERE_LIGHT_FADES_ASHEN_OATH',
      content: 'Master lore substrate detailing Kaelen, Serafina, Eldrin, Brother Malakor, Silent Spire, and the Architecture of Flesh.',
      metadata: { category: 'Codex', tags: ['ashen-oath', 'where-light-fades', 'lore'] },
    },
    {
      title: 'Blueprint for Dynamic Rosetta Stone App',
      id: 'DYNAMIC_ROSETTA_BLUEPRINT',
      content: 'Master technical blueprint for Component-Driven Cognition, Supabase Sovereign Backend, React 19, and D3.js physics.',
      metadata: { category: 'Blueprint', tags: ['blueprint', 'rosetta-stone'] },
    },
  ];

  console.log(`\nSeeding ${knowledgeSeedRecords.length} records into 'knowledge_base' table...`);
  const { error: kbErr } = await supabase.from('knowledge_base').upsert(knowledgeSeedRecords);
  if (kbErr) {
    console.warn("[knowledge_base] Insert note:", kbErr.message);
  } else {
    console.log("✅ 'knowledge_base' table successfully seeded.");
  }

  // 3. Seed documents table (RAG Vector Store)
  const documentsSeed = knowledgeSeedRecords.map((rec, idx) => ({
    content: `# ${rec.title}\nCategory: ${rec.metadata.category}\n\n${rec.content}`,
    metadata: {
      docId: rec.id,
      title: rec.title,
      type: rec.metadata.category,
      chunkIndex: 0,
    },
  }));

  console.log(`\nSeeding ${documentsSeed.length} documents into 'documents' table...`);
  const { error: docErr } = await supabase.from('documents').insert(documentsSeed);
  if (docErr) {
    console.warn("[documents] Insert note:", docErr.message);
  } else {
    console.log("✅ 'documents' table successfully seeded.");
  }

  console.log('\n✨ Database Seed Protocol Completed.');
}

seedSupabase().catch((err) => {
  console.error('❌ Seed Script Error:', err);
});
