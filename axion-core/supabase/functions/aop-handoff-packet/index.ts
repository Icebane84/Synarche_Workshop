// Supabase Edge Function: aop-handoff-packet
// Purpose: create/update an Eidetic Buffer "handoff packet" in axion_state (Cold Storage)

import { createClient } from "npm:@supabase/supabase-js@2.45.4";

type HandoffPacket = {
  schema_version: string;
  crystalline_essence?: string;
  harvested_state_vector?: unknown;
  selts?: unknown;
  umbs?: unknown;
  aops?: unknown;
  created_at?: string;
};

type ReqBody = {
  session_id: string;
  packet: HandoffPacket;
  // Optional idempotency key so repeated calls don't spam updates
  idempotency_key?: string;
};

const jsonResponse = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Connection": "keep-alive",
    },
  });

Deno.serve(async (req: Request) => {
  if (req.method !== "POST") {
    return jsonResponse({ error: "Method not allowed" }, 405);
  }

  const authHeader = req.headers.get("Authorization") ?? "";
  const jwt = authHeader.startsWith("Bearer ") ? authHeader.slice("Bearer ".length) : null;

  const supabaseUrl = Deno.env.get("SUPABASE_URL") ?? "https://rtjkhpotguwngfpvhfej.supabase.co";
  const anonKey = Deno.env.get("SUPABASE_ANON_KEY") ?? "sb_publishable_APS-_w0TK4EeBkvmoRu5Zw_1nEsOLiD";

  const supabase = createClient(supabaseUrl, anonKey, {
    global: {
      headers: jwt ? { Authorization: `Bearer ${jwt}` } : {},
    },
  });

  let body: ReqBody;
  try {
    body = await req.json();
  } catch {
    return jsonResponse({ error: "Invalid JSON body" }, 400);
  }

  if (!body?.session_id) return jsonResponse({ error: "session_id is required" }, 400);
  if (!body?.packet) return jsonResponse({ error: "packet is required" }, 400);

  const nowIso = new Date().toISOString();
  const packet: HandoffPacket = {
    schema_version: body.packet.schema_version ?? "1",
    crystalline_essence: body.packet.crystalline_essence,
    harvested_state_vector: body.packet.harvested_state_vector,
    selts: body.packet.selts,
    umbs: body.packet.umbs,
    aops: body.packet.aops,
    created_at: body.packet.created_at ?? nowIso,
  };

  // Cold storage anchor
  // We use axion_state.key as the unique identifier.
  const key = `handoff_packet:${body.session_id}`;

  const value = {
    ...packet,
    _meta: {
      idempotency_key: body.idempotency_key ?? null,
      stored_at: nowIso,
      source: "aop-handoff-packet",
    },
  };

  const { error } = await supabase
    .from("axion_state")
    .upsert(
      {
        key,
        value,
      },
      {
        onConflict: "key",
      }
    );

  if (error) {
    return jsonResponse({ error: error.message }, 500);
  }

  return jsonResponse({ ok: true, key, stored_at: nowIso });
});
