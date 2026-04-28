/**
 * GUCA-AXN-002: PhoenixLogger Auto-Fixer
 * Automatically replaces console.log/error/warn with PhoenixLogger
 * and injects the required absolute path alias import.
 */

const fs = require('node:fs');
const path = require('node:path');

const TARGET_DIR = path.resolve(__dirname, '../../src'); // Adjust to your source directory
const IMPORT_STATEMENT = "import { PhoenixLogger } from '@system/logging';\n";

function processFile(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    let isModified = false;

    // Check if the file contains console statements
    if (/console\.(log|info|warn|error|debug)\s*\(/.test(content)) {
        
        // Map console methods to PhoenixLogger equivalents
        content = content.replaceAll(/console\.log\s*\(/g, 'PhoenixLogger.info(');
        content = content.replaceAll(/console\.info\s*\(/g, 'PhoenixLogger.info(');
        content = content.replaceAll(/console\.warn\s*\(/g, 'PhoenixLogger.info('); // Fallback to info, or create a warn method
        content = content.replaceAll(/console\.error\s*\(/g, 'PhoenixLogger.error(');
        content = content.replaceAll(/console\.debug\s*\(/g, 'PhoenixLogger.debug(');

        // Inject the import statement if it doesn't already exist
        if (!content.includes(IMPORT_STATEMENT.trim())) {
            // Add import after the last existing import, or at the top of the file
            const lastImportIndex = content.lastIndexOf('import ');
            if (lastImportIndex === -1) {
                content = IMPORT_STATEMENT + content;
            } else {
                const endOfLastImport = content.indexOf('\n', lastImportIndex) + 1;
                content = content.slice(0, endOfLastImport) + IMPORT_STATEMENT + content.slice(endOfLastImport);
            }
        }

        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`[FIXED] T201 Violation resolved in: ${filePath}`);
        isModified = true;
    }
    return isModified;
}

function walkDirectory(dir) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        if (fs.statSync(fullPath).isDirectory()) {
            walkDirectory(fullPath);
        } else if (fullPath.endsWith('.ts') || fullPath.endsWith('.tsx') || fullPath.endsWith('.js')) {
            processFile(fullPath);
        }
    }
}

console.log("Initiating PhoenixLogger Auto-Fix Sequence...");
walkDirectory(TARGET_DIR);
console.log("Sequence Complete.");
