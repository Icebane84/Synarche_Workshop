import _babelTraverse, { NodePath } from '@babel/traverse';
import * as t from '@babel/types';
import { ASTViolation, InspectionContext, RuleConfig } from '../types';

const getTraverseFn = (): any => {
    if (typeof _babelTraverse === 'function') return _babelTraverse;
    if (typeof (_babelTraverse as any)?.default === 'function') return (_babelTraverse as any).default;
    if (typeof (_babelTraverse as any)?.traverse === 'function') return (_babelTraverse as any).traverse;
    return null;
};

/**
 * Rule: Detect Prop Drilling
 */
export const detectPropDrilling = (context: InspectionContext, _config: RuleConfig): ASTViolation[] => {
    const violations: ASTViolation[] = [];
    const traverse = getTraverseFn();
    if (!traverse) return violations;

    try {
        traverse(context.ast, {
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
    } catch {
        // Safe fallback on AST traversal failures
    }

    return violations;
};
