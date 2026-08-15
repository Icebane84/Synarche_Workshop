// @ts-ignore
import adjacencyMatrix from '../../../../prs_001_ashen_genesis/index/adjacency_matrix.json';

export interface CanonicalEnemy {

  id: string;
  name: string;
  maxHealth: number;
  attackDamage: number;
  category: string;
  description: string;
  abilities: string[];
  defeatedDrop?: string;
}

interface GraphNodeProperties {
  hp?: number;
  atk?: number;
  category?: string;
  description?: string;
  abilities?: string[];
  defeated_drop?: string;
}

interface GraphNode {
  id: string;
  label: string;
  name?: string;
  properties?: GraphNodeProperties;
}

export function loadCanonicalEnemies(): CanonicalEnemy[] {
  const nodes = (adjacencyMatrix.nodes || []) as GraphNode[];
  const enemyNodes = nodes.filter((n: GraphNode) => n.label === 'Enemy');

  if (!enemyNodes || enemyNodes.length === 0) {
    // Fallback default list if matrix is empty
    return [
      {
        id: 'enemy-creeping-doubt',
        name: 'Creeping Doubt',
        maxHealth: 80,
        attackDamage: 8,
        category: 'Spite Manifestation',
        description: 'A low-level shadow that feeds on fear.',
        abilities: ['Shadow Strike']
      },
      {
        id: 'enemy-ashen-abomination',
        name: 'Ashen Abomination',
        maxHealth: 300,
        attackDamage: 18,
        category: 'Manifestation of blight',
        description: 'Hulking, monstrous humanoids of fused ash, bone, and blackened flesh.',
        abilities: ['Corrupted Aura', "Nyx's Rage"],
        defeatedDrop: 'Heartstone Key'
      }
    ];
  }

  return enemyNodes.map((node: GraphNode) => {
    const props = node.properties || {};
    return {
      id: node.id,
      name: node.name || 'Unknown Corrupted',
      maxHealth: typeof props.hp === 'number' ? props.hp : 100,
      attackDamage: typeof props.atk === 'number' ? props.atk : 10,
      category: props.category || 'Manifestation of Nyx',
      description: typeof props.description === 'string' ? props.description.trim() : '',
      abilities: Array.isArray(props.abilities) ? props.abilities : [],
      defeatedDrop: props.defeated_drop || undefined
    };
  });
}

