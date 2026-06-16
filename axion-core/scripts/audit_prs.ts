import * as fs from "fs";
import * as path from "path";
import { validateMetadata } from "../src/utils/validation";
import { PRS_001_SCHEMA } from "../src/constants/schemas";

const REGISTRY_PATH = path.join(__dirname, "..", "assets", "PRS-001.json");

const audit = () => {
  console.log(`[VIGIL] Initiating Audit of Phoenix Rosetta Stone...`);
  console.log(`[VIGIL] Path: ${REGISTRY_PATH}`);

  try {
    if (!fs.existsSync(REGISTRY_PATH)) {
      throw new Error(`Registry not found at: ${REGISTRY_PATH}`);
    }

    const data = JSON.parse(fs.readFileSync(REGISTRY_PATH, "utf8"));

    console.log(`[VIGIL] Data loaded. Commencing recursive validation...`);
    validateMetadata(data, PRS_001_SCHEMA);

    console.log(`[SUCCESS] PRS-001.json structural integrity VERIFIED.`);
    console.log(`[SUCCESS] Current Status: ZERO ENTROPY.`);
  } catch (error: any) {
    console.error(`[Dissonance Detected]: ${error.message}`);
    process.exit(1);
  }
};

audit();
