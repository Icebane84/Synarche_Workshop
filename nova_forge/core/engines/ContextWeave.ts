/*
artifact_anchor:
  id: COG.CONTEXTWEAVE.001
  version: v15.0 [OMEGA]
  provenance: '2026-07-22'
  domain: COG
  celestial_class: PLANET
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
*/

import { PhoenixLogger } from "@system/logging";

export interface ArtifactData {
  id: string;
  content?: string;
  tags?: string[];
}

export interface WeaveResult {
  synergyScore: number;
  pivots: string[];
  isAligned: boolean;
}

export class ContextWeave {
  private synergyThreshold: number;

  constructor(synergyThreshold = 0.5) {
    this.synergyThreshold = synergyThreshold;
    PhoenixLogger.info("ContextWeave: Online and aligned with OMEGA v15.0");
  }

  /**
   * Classic signature: Weaves connection between nodes in the association memory.
   */
  weave(sourceId: string, targetId: string, weight: number): void {
    PhoenixLogger.info(`ContextWeave: Weaving connection between ${sourceId} and ${targetId} with weight ${weight}`);
    // Association graph updates can be simulated or persisted here
  }

  /**
   * Ported from weaver.py: Calculates the synergy score between two artifacts.
   */
  calculateSynergyScore(artifactA: ArtifactData, artifactB: ArtifactData): number {
    let score = 0.0;
    try {
      const contentA = artifactA.content || "";
      const contentB = artifactB.content || "";

      // 1. Keyword Overlap
      const keywordsA = new Set(this.extractKeywords(contentA));
      const keywordsB = new Set(this.extractKeywords(contentB));
      
      const overlap = new Set([...keywordsA].filter(x => keywordsB.has(x)));
      if (overlap.size > 0) {
        score += Math.min(overlap.size * 0.1, 0.4);
      }

      // 2. Metadata Alignment
      const tagsA = new Set(artifactA.tags || []);
      const tagsB = new Set(artifactB.tags || []);
      const tagOverlap = new Set([...tagsA].filter(x => tagsB.has(x)));
      if (tagOverlap.size > 0) {
        score += 0.2;
      }

      // 3. Explicit References
      const idB = artifactB.id;
      if (idB && (contentA.includes(`[[${idB}]]`) || contentA.includes(idB))) {
        score += 0.4;
      }
    } catch (err) {
      PhoenixLogger.error(`Error calculating synergy score between ${artifactA.id} and ${artifactB.id}: ${err}`);
      return 0.0;
    }
    return Math.min(score, 1.0);
  }

  /**
   * Ported from weaver.py: Weaves two artifacts together, determining synergy and pivots.
   */
  weaveArtifacts(artifactA: ArtifactData, artifactB: ArtifactData): WeaveResult {
    const score = this.calculateSynergyScore(artifactA, artifactB);
    const keywordsA = new Set(this.extractKeywords(artifactA.content || ""));
    const keywordsB = new Set(this.extractKeywords(artifactB.content || ""));
    const pivots = [...keywordsA].filter(x => keywordsB.has(x));

    return {
      synergyScore: score,
      pivots,
      isAligned: score >= this.synergyThreshold
    };
  }

  /**
   * Extracts uppercase-starting words of length > 3 (proper nouns).
   */
  extractKeywords(text: string): string[] {
    if (!text) {
      return [];
    }
    const words = text.match(/\b[A-Z]\w*\b/g);
    if (!words) {
      return [];
    }
    return words.filter(w => w.length > 3);
  }
}
