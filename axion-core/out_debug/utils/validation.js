"use strict";
/**
 * PRS-001 Modular Validation Utility
 * Supports nested objects and Regex format enforcement.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.validateMetadata = void 0;
/**
 * Validates a metadata object against a provided schema.
 * Performs recursive type checking, required field verification, and regex format enforcement.
 *
 * @param metadata - The object to validate.
 * @param schema - The MetadataSchema to validate against.
 * @throws Error - If validation fails.
 */
const validateMetadata = (metadata, schema) => {
  // 1. Check Required Top-Level Fields
  for (const field of schema.required) {
    if (!(field in metadata)) {
      throw new Error(`[Validation Error]: Missing required field: "${field}"`);
    }
  }
  // 2. Recursive Type and Format Verification
  const verify = (data, typeSchema, path = "") => {
    for (const key in typeSchema) {
      const currentPath = path ? `${path}.${key}` : key;
      const expectedType = typeSchema[key];
      const actualValue = data[key];
      if (actualValue === undefined) continue;
      if (typeof expectedType === "object") {
        // Recursive Call for Nested Objects
        if (typeof actualValue !== "object" || actualValue === null) {
          throw new Error(
            `[Validation Error]: "${currentPath}" must be an object.`,
          );
        }
        verify(actualValue, expectedType, currentPath);
      } else {
        // Primitive Type Check
        if (typeof actualValue !== expectedType) {
          throw new Error(
            `[Validation Error]: "${currentPath}" must be a ${expectedType}.`,
          );
        }
        // Regex Format Check (if applicable)
        if (schema.formats?.[key] && typeof actualValue === "string") {
          if (!schema.formats[key].test(actualValue)) {
            throw new Error(
              `[Validation Error]: "${currentPath}" does not match required format.`,
            );
          }
        }
      }
    }
  };
  verify(metadata, schema.types);
};
exports.validateMetadata = validateMetadata;
//# sourceMappingURL=validation.js.map
