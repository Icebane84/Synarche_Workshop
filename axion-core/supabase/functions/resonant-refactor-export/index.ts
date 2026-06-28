import { createClient } from "npm:@supabase/supabase-js@2";

const encoder = new TextEncoder();

Deno.serve(async (req) => {
  try {
    const url = new URL(req.url);
    const params = url.searchParams;

    const reportId = params.get("report_id");
    const status = params.get("status");
    const from = params.get("from"); // ISO
    const to = params.get("to"); // ISO

    const limit = clampInt(params.get("limit"), 500);
    const offset = clampInt(params.get("offset"), 0);

    const format = (params.get("format") ?? "csv").toLowerCase();
    const includeEmpty = (params.get("include_empty") ?? "true").toLowerCase() === "true";

    const supabaseUrl = Deno.env.get("SUPABASE_URL") ?? "https://rtjkhpotguwngfpvhfej.supabase.co";
    const supabaseAnonKey = Deno.env.get("SUPABASE_ANON_KEY") ?? "sb_publishable_APS-_w0TK4EeBkvmoRu5Zw_1nEsOLiD";

    const authHeader = req.headers.get("Authorization");
    const supabase = createClient(supabaseUrl, supabaseAnonKey, {
      global: {
        headers: authHeader ? { Authorization: authHeader } : {},
      },
    });

    // Decide report set
    let reportFilter = supabase.from("resonant_refactor_reports");
    if (reportId) reportFilter = reportFilter.eq("id", reportId);
    if (status) reportFilter = reportFilter.eq("status", status);
    if (from) reportFilter = reportFilter.gte("created_at", from);
    if (to) reportFilter = reportFilter.lte("created_at", to);

    const { data: reports, error: reportErr } = await reportFilter
      .select("id,event,status,created_at,created_with_version")
      .order("created_at", { ascending: false })
      .limit(limit)
      .offset(offset);

    if (reportErr) return json({ error: reportErr.message }, 500);
    if (!reports || reports.length === 0) {
      const empty = format === "json" ? { rows: [] } : csvWithHeader();
      return new Response(typeof empty === "string" ? empty : JSON.stringify(empty), {
        status: 200,
        headers: {
          ...(format === "json" ? { "content-type": "application/json; charset=utf-8" } : { "content-type": "text/csv; charset=utf-8" }),
        },
      });
    }

    const reportIds = reports.map((r) => r.id);

    // Export from normalized operations table.
    // Deterministic ordering: operation_order, created_at, id
    let opsQuery = supabase
      .from("resonant_refactor_operations")
      .select(
        "operation_type,intent,constraint,operation_order,created_at,id,report_id",
      )
      .in("report_id", reportIds)
      .order("operation_order", { ascending: true })
      .order("created_at", { ascending: true })
      .order("id", { ascending: true });

    const { data: ops, error: opsErr } = await opsQuery;
    if (opsErr) return json({ error: opsErr.message }, 500);

    const reportById = new Map(reports.map((r) => [r.id, r]));
    const rows: Array<Record<string, unknown>> = [];

    // Include empty operations rows if requested.
    if (includeEmpty) {
      for (const r of reports) {
        rows.push({
          id: r.id,
          event: r.event ?? "",
          status: r.status ?? "",
          created_at: r.created_at,
          created_with_version: r.created_with_version ?? "",
          operation_order: null,
          operation_type: "",
          intent: "",
          constraint: "",
        });
      }
    }

    for (const op of ops ?? []) {
      const r = reportById.get(op.report_id);
      if (!r) continue;
      rows.push({
        id: r.id,
        event: r.event ?? "",
        status: r.status ?? "",
        created_at: r.created_at,
        created_with_version: r.created_with_version ?? "",
        operation_order: op.operation_order,
        operation_type: op.operation_type ?? "",
        intent: op.intent ?? "",
        constraint: op.constraint ?? "",
      });
    }

    if (format === "json") {
      return new Response(JSON.stringify({ rows }), {
        status: 200,
        headers: { "content-type": "application/json; charset=utf-8" },
      });
    }

    // CSV
    const csv = csvRows(rows);
    return new Response(csv, {
      status: 200,
      headers: {
        "content-type": "text/csv; charset=utf-8",
        "content-disposition": reportId
          ? `attachment; filename="resonant_refactor_${reportId}.csv"`
          : `attachment; filename="resonant_refactor_export.csv"`,
      },
    });
  } catch (e) {
    return json({ error: e?.message ?? String(e) }, 500);
  }
});

function clampInt(v: string | null, fallback: number) {
  const n = v === null ? fallback : Number(v);
  if (!Number.isFinite(n)) return fallback;
  return Math.max(0, Math.floor(n));
}

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8" },
  });
}

const CSV_HEADER = [
  "report_id",
  "created_at",
  "created_with_version",
  "event",
  "status",
  "operation_order",
  "operation_type",
  "intent",
  "constraint",
];

function csvWithHeader() {
  return CSV_HEADER.join(",") + "\n";
}

function csvEscape(value: unknown) {
  const s = value === null || value === undefined ? "" : String(value);
  const escaped = s.replaceAll('"', '""');
  const needsQuotes = /[\n\r,\"]/.test(escaped);
  return needsQuotes ? `"${escaped}"` : escaped;
}

function csvRows(rows: Array<Record<string, unknown>>) {
  const out: string[] = [];
  out.push(CSV_HEADER.join(","));
  for (const r of rows) {
    out.push(
      [
        r.id,
        r.created_at,
        r.created_with_version,
        r.event,
        r.status,
        r.operation_order,
        r.operation_type,
        r.intent,
        r.constraint,
      ].map(csvEscape).join(","),
    );
  }
  return out.join("\n");
}
