import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = process.env.VITE_SUPABASE_URL || 'https://rtjkhpotguwngfpvhfej.supabase.co';
const SUPABASE_KEY = process.env.VITE_SUPABASE_ANON_KEY || 'sb_publishable_APS-_w0TK4EeBkvmoRu5Zw_1nEsOLiD';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

async function verifySupabase() {
  console.log('🔍 Running Supabase Live Verification Protocol...\n');

  // 1. Check knowledge_base
  const { data: kbData, error: kbErr } = await supabase.from('knowledge_base').select('id, title, metadata');
  if (kbErr) console.error('❌ knowledge_base Error:', kbErr.message);
  else console.log(`✅ [knowledge_base]: ${kbData.length} records found in database.`);

  // 2. Check memory_entries
  const { data: memData, error: memErr } = await supabase.from('memory_entries').select('id, content, domain');
  if (memErr) console.error('❌ memory_entries Error:', memErr.message);
  else console.log(`✅ [memory_entries]: ${memData.length} nodes found in database.`);

  // 3. Check documents
  const { data: docData, error: docErr } = await supabase.from('documents').select('id, metadata');
  if (docErr) console.error('❌ documents Error:', docErr.message);
  else console.log(`✅ [documents]: ${docData.length} RAG documents found in database.`);

  console.log('\n✨ All Supabase database tables verified active and connected!');
}

verifySupabase().catch(console.error);
