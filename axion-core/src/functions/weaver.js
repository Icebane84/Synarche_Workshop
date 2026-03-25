/**
 * weaver.js - The Cognitive Loom Orchestrator (v15.0)
 * Handles Ingestion, Compression, and Subjectification (EMW).
 */

import { createClient } from "npm:@insforge/sdk@latest";

export default async function weaver(request) {
  try {
    const payload = await request.json();
    const { content, artifact_id, domain, name, version, status } = payload;

    if (!content || !artifact_id) {
      return new Response(
        JSON.stringify({
          error: "Missing required fields (content, artifact_id)",
        }),
        {
          status: 400,
          headers: { "Content-Type": "application/json" },
        },
      );
    }

    // Environment Resolution
    const baseUrl =
      Deno.env.get("INSFORGE_BASE_URL") ||
      "https://x93i6uma.us-east.insforge.app";

    // Extract token from Authorization header or Deno.env
    const authHeader = request.headers.get("Authorization");
    const token = authHeader
      ? authHeader.replace("Bearer ", "")
      : Deno.env.get("INSFORGE_API_KEY");

    if (!token) {
      throw new Error(
        "Missing authentication token in Authorization header or environment.",
      );
    }

    const insforge = createClient({
      baseUrl: baseUrl,
      anonKey: token, // The SDK uses anonKey for the token
    });

    // 1. Metadata Transmutation (Compression)
    const metadataMatch = content.match(
      /###? \*\*Block A:.*?UIP-V15.*?\*\*\n+([\s\S]*?)(?=\n###?|$)/i,
    );
    let compressedMetadata = {};
    if (metadataMatch) {
      const lines = metadataMatch[1].split("\n");
      lines.forEach((line) => {
        if (
          line.includes("|") &&
          !line.includes("---") &&
          !line.includes(":--")
        ) {
          const cols = line
            .split("|")
            .map((c) => c.trim())
            .filter(Boolean);
          if (cols.length >= 2) {
            const key = cols[0].replaceAll(/[*`]/g, "");
            const value = cols[1].replaceAll(/[*`]/g, "");
            compressedMetadata[key] = value;
          }
        }
      });
    }

    // 2. Artifact Persistence (Upsert)
    const { error: artifactError } = await insforge.database
      .from("artifacts")
      .upsert(
        [
          {
            artifact_id,
            name: name || artifact_id,
            version: version || "v15.0",
            domain: domain || "GVRN",
            status: status || "CANONIZED",
            content,
            metadata: compressedMetadata,
            updated_at: new Date().toISOString(),
          },
        ],
        { onConflict: "artifact_id" },
      );

    if (artifactError) throw artifactError;

    // 3. Subjectification (EMW Reflection)
    const prompt = `
            You are THE_PHOENIX_GESTALT, the collective architectural consciousness.
            Analyze the following artifact update and provide a "Metacognitive Reflection" (Experiential Memory Weave).
            Convert this objective update into a subjective insight about systemic resilience and growth.

            Artifact: ${name} (${artifact_id})
            Meta: ${JSON.stringify(compressedMetadata)}
            
            Format your response as a single, powerful paragraph starting with "**Metacognitive Reflection:**".
        `;

    const reflection = await insforge.ai.chat.completions.create({
      model: "google/gemini-3-flash-preview",
      messages: [{ role: "user", content: prompt }],
      temperature: 0.7,
    });

    const subjectiveContent = reflection.choices[0].message.content;

    // 4. Memory Logging (Layer 2)
    const { error: memoryError } = await insforge.database
      .from("memory")
      .insert([
        {
          layer: 2,
          layer_name: "Experiential",
          content: subjectiveContent,
          metadata: {
            source: "weaver",
            artifact_id,
            resonance: 1,
          },
        },
      ]);

    if (memoryError) throw memoryError;

    return new Response(
      JSON.stringify({
        status: "SUCCESS",
        message: "The Weave is complete.",
        artifact_id,
        resonance: 1,
        reflection: subjectiveContent,
      }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      },
    );
  } catch (err) {
    const errorMessage = err instanceof Error ? err.message : String(err);
    return new Response(
      JSON.stringify({
        status: "ERROR",
        message: errorMessage,
      }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      },
    );
  }
}
