// Setup type definitions for built-in Supabase Runtime APIs
import "jsr:@supabase/functions-js/edge-runtime.d.ts"
import { createClient } from 'jsr:@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

// --- SENTINEL: Type Definitions ---

interface DissonanceRequest {
  entity_id?: string;
  content?: string;
  context_depth?: number;
  generate_quest?: boolean;
}

interface DissonanceMarker {
  type: 'STRUCTURAL' | 'SEMANTIC' | 'OPERATIONAL';
  marker: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  message: string;
}

interface AnalysisResult {
  score: number;
  markers: DissonanceMarker[];
}

// --- SOPHIA: Logic & Constants ---

const WEIGHTS = {
  HEADER: 0.3,
  AGP: 0.4,
  PROMPT: 0.1
};

const THRESHOLDS = {
  STABLE: 0.85,
  QUEST_TRIGGER: 0.75
};

/**
 * Pure function to analyze content resonance.
 * "Wisdom requires seeing the structure within."
 */
function analyzeContent(content: string): AnalysisResult {
  let score = 1;
  const markers: DissonanceMarker[] = [];

  // 1. Structure Check (The Skeleton)
  if (!content.includes("###### [ARTIFACT START]")) {
    score -= WEIGHTS.HEADER;
    markers.push({
      type: "STRUCTURAL",
      marker: "Missing Artifact Header",
      severity: "HIGH",
      message: "Artifact lacks the crucial '###### [ARTIFACT START]' anchor."
    });
  }

  // 2. Semantic Check (The Soul - AGP)
  if (!content.includes("## II. Axiomatic Governance & Purpose")) {
    score -= WEIGHTS.AGP;
    markers.push({
      type: "SEMANTIC",
      marker: "Soulless (Missing AGP)",
      severity: "CRITICAL",
      message: "Artifact lacks the 'Axiomatic Governance & Purpose' block, rendering it unmoored."
    });
  }

  // 3. Operational Check (The Hand - Commands)
  if (!content.includes("CMD:") && !content.includes("Actionable Prompt Packet")) {
    score -= WEIGHTS.PROMPT;
    markers.push({
      type: "OPERATIONAL",
      marker: "Inert (No Commands)",
      severity: "LOW",
      message: "Artifact has no defined executable commands (CMD:)."
    });
  }

  return { score: Math.max(0, Number.parseFloat(score.toFixed(2))), markers };
}

// --- MAIN EXECUTION ---

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const supabaseUrl = Deno.env.get('SUPABASE_URL') ?? 'https://rtjkhpotguwngfpvhfej.supabase.co';
    const serviceRoleKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? 'sb_secret_fOIDz3lJfLlxWAe0Thwp8w_D5-ZQphj';
    const supabaseClient = createClient(supabaseUrl, serviceRoleKey);

    const payload = await req.json() as DissonanceRequest;
    const { entity_id, content = "", generate_quest = false } = payload;
    const subject = entity_id || "Unbound Content";

    // Invoke Wisdom
    const { score, markers } = analyzeContent(content);

    // Automation Phase: Quest Generation
    const questGenerated = generate_quest && score < THRESHOLDS.QUEST_TRIGGER;
    
    if (questGenerated) {
      const { error: questError } = await supabaseClient
        .from('quests')
        .insert({
          name: `Refine: ${subject}`,
          governing_axiom: "UMB-LIL-001",
          target_artifact: subject,
          dissonance_profile: JSON.stringify(markers.map(m => m.message)), 
          status: 'Active',
          success_metrics: { required_resonance: 0.9, detected_resonance: score }
        })
      
      if (questError) console.error("Quest Generation Error:", questError)
    }

    const responseData = {
      subject,
      resonance_score: score,
      dissonance_markers: markers,
      status: score > THRESHOLDS.STABLE ? "STABLE" : "REFINEMENT_REQUIRED",
      quest_generated: questGenerated,
      timestamp: new Date().toISOString(),
      governed_by: "UMB-LIL-001 v1.0"
    }

    return new Response(
      JSON.stringify(responseData),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } },
    )
  } catch (error) {
    return new Response(JSON.stringify({ error: (error as Error).message }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 400,
    })
  }
})
