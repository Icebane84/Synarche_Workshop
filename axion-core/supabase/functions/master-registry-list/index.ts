// Setup type definitions for built-in Supabase Runtime APIs
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from 'jsr:@supabase/supabase-js@2';

Deno.serve(async (req) => {
  try {
    const supabaseUrl = Deno.env.get('SUPABASE_URL') ?? 'https://rtjkhpotguwngfpvhfej.supabase.co';
    const anonKey = Deno.env.get('SUPABASE_ANON_KEY') ?? 'sb_publishable_APS-_w0TK4EeBkvmoRu5Zw_1nEsOLiD';
    const supabase = createClient(supabaseUrl, anonKey, {
      global: {
        headers: {
          Authorization: req.headers.get('Authorization') ?? ''
        }
      }
    });

    const { data, error } = await supabase.from('Master_Registry').select('*');
    if (error) {
      throw error;
    }

    return new Response(JSON.stringify({
      data
    }), {
      headers: {
        'Content-Type': 'application/json'
      },
      status: 200
    });
  } catch (err) {
    return new Response(JSON.stringify({
      message: err?.message ?? err
    }), {
      headers: {
        'Content-Type': 'application/json'
      },
      status: 500
    });
  }
});
