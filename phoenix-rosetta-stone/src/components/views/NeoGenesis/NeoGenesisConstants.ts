export interface OrganismStats {
  hp: number;
  maxHp: number;
  dna: number;
  starlight: number;
  population: number;
  ecology: number; // 0-100%
  industry: number; // 0-100%
  stage: "Cellular" | "Aquatic" | "Tribal" | "Galactic";
  speed: number;
  armor: number;
  ingestion: number;
  intelligence: number;
  readiness: number;
}

export interface Nutrient {
  x: number;
  y: number;
  size: number;
  color: string;
  type: "amino" | "lipid" | "mutagen";
}

export interface PredatorICE {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  name: string;
}

export interface ToxicZone {
  x: number;
  y: number;
  radius: number;
}

export interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  color: string;
  life: number;
  maxLife: number;
  size: number;
}

export interface TribalStructure {
  id: string;
  name: string;
  type: string;
  cost: number;
  count: number;
  effect: string;
  icon: string;
}

export interface PlanetNode {
  id: string;
  name: string;
  type: string;
  color: string;
  cost: number;
  status: "Unexplored" | "Colonized" | "Terraformed";
  population: number;
  output: string;
}

export const INITIAL_PLANETS: PlanetNode[] = [
  { id: "P1", name: "Solaria Prime", type: "Terran Origin World", color: "text-cyan-400 border-cyan-500/40 bg-cyan-500/10", cost: 0, status: "Colonized", population: 2500000, output: "+50 DNA/sec" },
  { id: "P2", name: "Kryon-9", type: "Glacial Cryo-World", color: "text-blue-400 border-blue-500/40 bg-blue-500/10", cost: 150, status: "Unexplored", population: 0, output: "+100 Mutagens/sec" },
  { id: "P3", name: "Aetheria IV", type: "Gas Giant Dyson Station", color: "text-purple-400 border-purple-500/40 bg-purple-500/10", cost: 300, status: "Unexplored", population: 0, output: "+200 Starlight/sec" },
  { id: "P4", name: "Vulcanus Prime", type: "Magma Core Mining Sphere", color: "text-amber-400 border-amber-500/40 bg-amber-500/10", cost: 500, status: "Unexplored", population: 0, output: "+400 Industry/sec" },
  { id: "P5", name: "Zephyr Alpha", type: "Hyper-Biosphere Reserve", color: "text-green-400 border-green-500/40 bg-green-500/10", cost: 800, status: "Unexplored", population: 0, output: "+1000 DNA/sec" },
];

export const INITIAL_TRIBAL_STRUCTURES: TribalStructure[] = [
  { id: "S1", name: "Bio-Habitat Pod", type: "HOUSING", cost: 40, count: 2, effect: "+25 Pop Growth/sec", icon: "🛖" },
  { id: "S2", name: "Spore Sanctum", type: "CULTURE", cost: 60, count: 1, effect: "+5 DNA & Readiness/sec", icon: "🔮" },
  { id: "S3", name: "Chitin Smelter", type: "INDUSTRY", cost: 80, count: 0, effect: "+15 Industry, -5% Ecology", icon: "🏭" },
  { id: "S4", name: "Ecology Shrine", type: "ECO", cost: 75, count: 1, effect: "+10% Ecology Harmony", icon: "🌿" },
];
