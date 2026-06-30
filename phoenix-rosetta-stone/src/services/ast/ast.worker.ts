import { parse } from '@babel/parser';
import { detectPropDrilling } from './rules/detectPropDrilling';
import { detectConsoleLog } from './rules/detectConsoleLog';
import { detectLintEntropy } from './rules/detectLintEntropy';
import { RuleConfig, InspectionContext } from './types';

// Web Worker context
const ctx: Worker = self as any;

const rules = [detectPropDrilling, detectConsoleLog, detectLintEntropy];

ctx.onmessage = (event: MessageEvent) => {
    const { filePath, content, config } = event.data as {
        filePath: string;
        content: string;
        config: RuleConfig;
    };

    try {
        const ast = parse(content, {
            sourceType: 'module',
            plugins: ['typescript', 'jsx'],
            tokens: true,
        });

        const context: InspectionContext = {
            filePath,
            content,
            ast,
        };

        const violations = rules.flatMap((rule) => rule(context, config));
        ctx.postMessage({ filePath, violations, success: true });
    } catch (error: any) {
        ctx.postMessage({
            filePath,
            violations: [],
            success: false,
            error: error.message,
        });
    }
};
