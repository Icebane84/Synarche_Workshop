var __createBinding =
  (this && this.__createBinding) ||
  (Object.create
    ? (o, m, k, k2) => {
        if (k2 === undefined) k2 = k;
        var desc = Object.getOwnPropertyDescriptor(m, k);
        if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
          desc = {
            enumerable: true,
            get: () => m[k],
          };
        }
        Object.defineProperty(o, k2, desc);
      }
    : (o, m, k, k2) => {
        if (k2 === undefined) k2 = k;
        o[k2] = m[k];
      });
var __setModuleDefault =
  (this && this.__setModuleDefault) ||
  (Object.create
    ? (o, v) => {
        Object.defineProperty(o, "default", { enumerable: true, value: v });
      }
    : (o, v) => {
        o["default"] = v;
      });
var __importStar =
  (this && this.__importStar) ||
  (() => {
    var ownKeys = (o) => {
      ownKeys =
        Object.getOwnPropertyNames ||
        ((o) => {
          var ar = [];
          for (var k in o) if (Object.hasOwn(o, k)) ar[ar.length] = k;
          return ar;
        });
      return ownKeys(o);
    };
    return (mod) => {
      if (mod && mod.__esModule) return mod;
      var result = {};
      if (mod != null)
        for (var k = ownKeys(mod), i = 0; i < k.length; i++)
          if (k[i] !== "default") __createBinding(result, mod, k[i]);
      __setModuleDefault(result, mod);
      return result;
    };
  })();
Object.defineProperty(exports, "__esModule", { value: true });
exports.PRS_001_SCHEMA = exports.SOVEREIGN_ID_REGEX = void 0;
const standards = __importStar(
  require("../../../_governance/13_Standardization/GVRN.Standards.json"),
);
/**
 * Sovereign ID Regex: Supports legacy IDs (PRS-001) and OMEGA v15.0 standards (DOMAIN.TYPE.CLASS.SUBSYSTEM.DESCRIPTOR)
 * Pulled from GVRN.Standards.json
 */
exports.SOVEREIGN_ID_REGEX = new RegExp(standards.regex.SOVEREIGN_ID);
/**
 * PRS-001 Rosetta Stone Schema
 * Defines the structural requirements for the master knowledge graph.
 */
exports.PRS_001_SCHEMA = {
  required: ["artifact_id", "official_name", "version", "cognitive_loom"],
  types: {
    artifact_id: "string",
    official_name: "string",
    version: "string",
    cognitive_loom: {
      nodes: "object", // The current validator treats arrays as objects
    },
  },
  formats: {
    // artifact_id format check (if using the global regex)
    artifact_id: exports.SOVEREIGN_ID_REGEX,
  },
};
//# sourceMappingURL=schemas.js.map
