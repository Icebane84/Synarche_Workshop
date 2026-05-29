"use strict";

/**
 * Phoenix Protocol Governance Rules (PF-Series)
 *
 * These rules enforce the structural integrity of GVRN artifacts,
 * specifically handling spacing, block boundaries, and metadata placement.
 */

module.exports = [
  {
    names: ["PF001", "phoenix-heading-spacing"],
    description: "Enforce blank lines around headings for linter consistency",
    tags: ["phoenix", "governance"],
    function: (params, onError) => {
      const { lines } = params;
      params.tokens
        .filter((t) => t.type === "heading_open")
        .forEach((token) => {
          const [startLine, endLine] = token.map;

          // Validate line above (startLine is 0-indexed)
          if (startLine > 0) {
            const prevLine = lines[startLine - 1];
            // Allow the heading to be immediately preceded by the front matter separator
            if (prevLine.trim() !== "" && prevLine.trim() !== "---") {
              onError({
                lineNumber: token.lineNumber,
                detail: "Expected 1 blank line above heading",
                context: token.line.trim(),
              });
            }
          }

          // Validate line below (endLine is the index of the line following the heading)
          if (endLine < lines.length) {
            const nextLine = lines[endLine];
            if (nextLine.trim() !== "") {
              onError({
                lineNumber: token.lineNumber,
                detail: "Expected 1 blank line below heading",
                context: token.line.trim(),
              });
            }
          }
        });
    },
  },
  // Placeholder for PF002 - PF032
];
