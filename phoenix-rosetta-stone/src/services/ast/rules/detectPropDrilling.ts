import traverse, { NodePath } from '@babel/traverse';
import * as t from '@babel/types';
import { ASTViolation, InspectionContext, RuleConfig } from '../types';

/**
 * Rule: Detect Prop Drilling
 *
 * Logic:
 * 1. Identifies Functional Components.
 * 2. Checks if the component accepts props.
 * 3. Checks if `...props` (spread) is passed to a child element.
 * 4. (Basic Heuristic) In a single-file context, detecting true depth is hard.
 *    Instead, we detect "Blind Pass-Through" which is a strong indicator of drilling.
 *    Condition: Component takes `props` (or specific props) and spreads them onto a child
 *    WITHOUT using them in the component body (simplified check).
 */
export const detectPropDrilling = (context: InspectionContext, _config: RuleConfig): ASTViolation[] => {
    const violations: ASTViolation[] = [];

    // Check if we are using the real traverse from babel or if it's a default export issue
    // Vite handling of CJS modules sometimes requires .default
    // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-explicit-any
    const _traverse = typeof traverse === 'function' ? traverse : ((traverse as any).default as typeof traverse);

    _traverse(context.ast, {
        // Visit Function Declarations and Arrow Functions (Potential Components)
        Function(path: NodePath<t.Function>) {
            const node = path.node;

            // 1. Must have params (props)
            if (node.params.length === 0) return;

            const propsParam = node.params[0];
            let propsIdentifier = '';

            // Handle: (props) => ...
            if (propsParam.type === 'Identifier') {
                propsIdentifier = propsParam.name;
            }
            // Handle: ({ foo, bar, ...rest }) => ...
            else if (propsParam.type === 'ObjectPattern') {
                // If destructuring with rest, checking 'rest' usage is complex.
                // For now, let's focus on explicit `props` identifier pass-through.
                return;
            } else {
                return;
            }

            // 2. Check strict blind pass-through: <Child {...props} />
            let hasBlindSpread = false;
            let spreadLine = 0;

            path.traverse({
                JSXSpreadAttribute(jsxPath: NodePath<t.JSXSpreadAttribute>) {
                    if (jsxPath.node.argument.type === 'Identifier' && jsxPath.node.argument.name === propsIdentifier) {
                        hasBlindSpread = true;
                        spreadLine = jsxPath.node.loc?.start.line ?? 0;
                    }
                },
            });

            // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
            if (hasBlindSpread) {
                violations.push({
                    file: context.filePath,
                    line: spreadLine,
                    type: 'PROP_DRILLING',
                    message: `Component performs a blind prop spread ({...${propsIdentifier}}). This obscures data flow and often indicates prop drilling.`,
                    severity: 'medium',
                    codeSnippet: `<Element {...${propsIdentifier}} />`,
                });
            }
        },
    });

    return violations;
};
