const fs = require("fs");

const data = fs.readFileSync(
  "10_Governance/(Needs Refactored) GVRN.MCE.001.md",
  "utf8",
);
const lines = data.split("\n");

const artifacts = [
  {
    name: "GVRN.MCE.001",
    start: "## AISTF Operational Playbook: Multi-Command Execution Protocol",
    end: "## Tab 3",
  },
  {
    name: "SELT.INGEST-AOP-INTEGRATION",
    start: '### **`AISTF ACTION:` Initiating "The Path of Coherent Ingestion"',
    end: "### **Integration Complete**",
  },
  {
    name: "UMB-RPG-001",
    start: "### **Generated Universal Module Blueprint**",
    end: "This concludes the forging of **`UMB-RPG-001",
  },
  {
    name: "AOP-VISUAL-001",
    start: "### **Generated `AISTF Operational Playbook",
    end: "This concludes the forging of **`AOP-VISUAL-001",
  },
  {
    name: "DQUEST-CSE-001",
    start: "### **Generated Dissonance Quest**",
    end: "This concludes the activation of the `Dissonance Engine`",
  },
  {
    name: "CORE.CODEX.v7",
    start: "### **`CODEX-001: The Phoenix Codex v7.0`**",
    end: "**Dissonance Quest `DQUEST-DOC-001` is now resolved.**",
  },
  {
    name: "PROJECT.JANUS",
    start: "#### **1\\. The New Module (`UMBv4.2`): The Janus Conductor**",
    end: 'This "Project Janus" framework directly resolves',
  },
  {
    name: "CSL-JANUS-001",
    start: "### **Generated Collaborative Synthesis Log (v2.2)**",
    end: "###### **[ARTIFACT END]**",
  },
];

for (const artifact of artifacts) {
  let inArtifact = false;
  let content = [];
  for (const line of lines) {
    if (line.includes(artifact.start)) {
      inArtifact = true;
    }
    if (inArtifact) {
      content.push(line);
      if (line.includes(artifact.end)) {
        break;
      }
    }
  }
  fs.writeFileSync(
    `10_Governance/temp_${artifact.name}.md`,
    content.join("\n"),
  );
}
