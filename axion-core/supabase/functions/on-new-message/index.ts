import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const OPENAI_API_URL = "https://api.openai.com/v1/chat/completions";

console.log("Axion 'on-new-message' function initialized.");

Deno.serve(async (req) => {
  try {
    // 1. Webhook Payload Parsing
    const payload = await req.json();
    const { record } = payload;

    // Guard: Only respond to user messages to prevent infinite loops
    if (!record || record.sender === "Axion") {
      console.log("Ignoring message from Axion or empty record.");
      return new Response("Ignored", { status: 200 });
    }

    console.log(`Received message from ${record.sender}: ${record.content}`);

    // 2. Initialize Supabase Client
    // We use the Service Role Key to bypass RLS for reading state/writing response
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const supabaseKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, supabaseKey);

    // 3. Fetch Context
    // Get the last 20 messages for this session
    const { data: history, error: historyError } = await supabase
      .from("conversation_history")
      .select("sender, content")
      .eq("session_id", record.session_id)
      .order("created_at", { ascending: false })
      .limit(20);

    if (historyError) {
      throw new Error(`History fetch error: ${historyError.message}`);
    }

    // Reverse history to chronological order
    const contextMessages = (history || []).reverse().map((msg) => ({
      role: msg.sender === "Chris" ? "user" : "assistant",
      content: msg.content,
    }));

    // 4. Fetch System Prompt
    const { data: stateData } = await supabase
      .from("axion_state")
      .select("value")
      .eq("key", "system_prompt")
      .single();

    const systemPrompt =
      stateData?.value?.prompt || "You are Axion, an advanced AI system.";

    // 5. Construct LLM Payload
    const messages = [
      { role: "system", content: systemPrompt },
      ...contextMessages,
      // The new message is already in history? Need to check webhook timing.
      // Database Webhooks trigger AFTER insert. So 'record' is already in 'history'
      // if we fetched recently inserted rows. However, usually webhooks are async enough.
      // Let's assume the context fetch captured it if we ordered by created_at.
      // But to be safe and rigorous:
      // If the last message in 'contextMessages' is NOT the new record, append it.
      // But simpler: Just use the context fetched from DB.
    ];

    // 6. Call LLM API (OpenAI)
    const openAiKey = Deno.env.get("OPENAI_API_KEY");
    if (!openAiKey) {
      throw new Error("Missing OPENAI_API_KEY");
    }

    const llmResponse = await fetch(OPENAI_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${openAiKey}`,
      },
      body: JSON.stringify({
        model: "gpt-4-turbo", // or preferred model
        messages: messages,
        temperature: 0.7,
      }),
    });

    const llmData = await llmResponse.json();
    const aiContent = llmData.choices[0].message.content;

    // 7. Insert Response
    const { error: insertError } = await supabase
      .from("conversation_history")
      .insert({
        sender: "Axion",
        content: aiContent,
        session_id: record.session_id,
        metadata: {
          model: "gpt-4-turbo",
          usage: llmData.usage,
        },
      });

    if (insertError) {
      throw new Error(`Response insert error: ${insertError.message}`);
    }

    return new Response(
      JSON.stringify({ status: "Replied", reply: aiContent }),
      {
        headers: { "Content-Type": "application/json" },
        status: 200,
      }
    );
  } catch (err) {
    console.error("Error processing message:", err);
    return new Response(JSON.stringify({ error: err.message }), {
      headers: { "Content-Type": "application/json" },
      status: 500,
    });
  }
});
