/**
 * PRS-001 Modular Validation Utility
 * Supports nested objects and Regex format enforcement.
 */

/**
 * Defines the recursive structure for type validation.
 * Can be a string representing a primitive type or a nested object of schemas.
 */
export type NestedSchema = {
  [key: string]: string | NestedSchema;
};

/**
 * Defines the schema for metadata validation.
 */
export interface MetadataSchema {
  required: string[];
  types: NestedSchema;
  formats?: {
    [key: string]: RegExp;
  };
}

/**
 * Validates a metadata object against a provided schema.
 * Performs recursive type checking, required field verification, and regex format enforcement.
 *
 * @param metadata - The object to validate.
 * @param schema - The MetadataSchema to validate against.
 * @throws Error - If validation fails.
 */
export const validateMetadata = (
  metadata: any,
  schema: MetadataSchema,
): void => {
  // 1. Check Required Fields (Supports nested paths via dot notation)
  for (const field of schema.required) {
    const parts = field.split(".");
    let current = metadata;
    let isMissing = false;

    for (const part of parts) {
      if (
        current === null ||
        typeof current !== "object" ||
        !(part in current)
      ) {
        isMissing = true;
        break;
      }
      current = current[part];
    }

    if (isMissing) {
      throw new Error(`[Validation Error]: Missing required field: "${field}"`);
    }
  }

  // 2. Recursive Type and Format Verification
  const verify = (data: any, typeSchema: NestedSchema, path: string = "") => {
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
          throw new TypeError(
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
