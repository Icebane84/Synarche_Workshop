/*
artifact_anchor:
  id: CORE.REGISTERPATHS.001
  version: v15.0 [OMEGA]
  provenance: '2026-06-18'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: RUNTIME_MODULE_RESOLUTION
  relations: []
*/

import * as fs from "node:fs";
import { Module } from "node:module";
import * as path from "node:path";

const ModuleWithResolve = Module as unknown as {
  _resolveFilename: (
    request: string,
    parent: unknown,
    isMain: boolean,
    options: unknown,
  ) => string;
};

const originalResolveFilename = ModuleWithResolve._resolveFilename;

const prefixMappings: [string, string, string][] = [
  ["@governance/", "..", "_governance"],
  ["@domain/", ".", "02_domain"],
  ["@nexus/", ".", "nexus"],
  ["@fabric/", ".", "03_fabric"],
  ["@atlas/", ".", "01_atlas"],
  ["@essence/", ".", "types"],
  ["@shield/", "..", "sentinel"],
  ["@pulse/", "..", "_logs"],
  ["@loom/", "..", "templates"],
  ["@archive/", "..", "archives"],
  ["@universe/", "..", "_universe"],
  ["@logging/", ".", "system/logging"],
  ["@utils/", ".", "utils"],
];

function getMappedPath(request: string): string | null {
  if (request === "@logging") {
    return path.join(__dirname, "system", "logging", "index");
  }

  if (request.startsWith("@system/")) {
    const sub = request.slice(8);
    const systemPath = path.join(__dirname, "system", sub);
    const fileExists =
      fs.existsSync(systemPath) ||
      fs.existsSync(`${systemPath}.js`) ||
      fs.existsSync(`${systemPath}.json`) ||
      fs.existsSync(path.join(systemPath, "index.js"));
    return fileExists ? systemPath : path.join(__dirname, "cse", sub);
  }

  for (const [prefix, relativeDir, targetDir] of prefixMappings) {
    if (request.startsWith(prefix)) {
      return path.join(__dirname, relativeDir, targetDir, request.slice(prefix.length));
    }
  }

  return null;
}

ModuleWithResolve._resolveFilename = function (
  request: string,
  parent: unknown,
  isMain: boolean,
  options: unknown,
) {
  const mapped = getMappedPath(request);
  if (mapped !== null) {
    return originalResolveFilename.call(
      this,
      mapped,
      parent,
      isMain,
      options,
    );
  }

  return originalResolveFilename.call(
    this,
    request,
    parent,
    isMain,
    options,
  );
};
