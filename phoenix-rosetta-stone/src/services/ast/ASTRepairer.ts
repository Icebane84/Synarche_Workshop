import { ASTViolation } from './types';

/**
 * ASTRepairer [OMEGA v15.2]
 * Responsible for applying surgical patches to code strings based on AST coordinates.
 */
class ASTRepairer {
    applyFix(violation: ASTViolation, content: string): string {
        if (violation.start === undefined || violation.end === undefined) {
            console.warn('[ASTRepairer] Cannot apply fix: Missing coordinates.', violation);
            return content;
        }

        const before = content.slice(0, violation.start);
        const target = content.slice(violation.start, violation.end);
        const after = content.slice(violation.end);

        switch (violation.type) {
            case 'CONSOLE_LOG':
                return this.handleRangeRemoval(before, after);

            case 'LINT_ENTROPY':
                // Wrap in String() to fix "any template literal" lint
                if (target.startsWith('String(') && target.endsWith(')')) return content; // Already fixed
                return `${before}String(${target})${after}`;

            case 'UNUSED_IMPORT':
                // Base implementation: remove the range (specifier or entire line)
                return this.handleRangeRemoval(before, after);

            default:
                // For unknown types, we still attempt a range removal if expected
                return before + after;
        }
    }

    private handleRangeRemoval(before: string, after: string): string {
        // Check if the line is now effectively empty to avoid leaving blank lines
        const lastLineStart = before.lastIndexOf('\n') + 1;
        const nextLineEnd = after.indexOf('\n');
        const lineFragmentBefore = before.slice(lastLineStart);
        const lineFragmentAfter = after.slice(0, nextLineEnd === -1 ? undefined : nextLineEnd);
        const lineContent = lineFragmentBefore + lineFragmentAfter;

        if (lineContent.trim() === '' || lineContent.trim() === ';') {
            // Full line removal (including the newline itself)
            return (
                before.slice(0, lastLineStart) +
                after.slice(nextLineEnd === -1 ? after.length : nextLineEnd + 1)
            );
        }
        return before + after;
    }
}

export const astRepairer = new ASTRepairer();
