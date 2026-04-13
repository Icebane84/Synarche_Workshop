import { CornerDownLeft, Zap } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import { graphData } from '../../data/graphData';
import type { CommandDefinitionGUCAv5 } from '../../types/synapseTypes';
import ArtifactSelector from '../common/ArtifactSelector';
import Tooltip from '../common/Tooltip';

interface ParameterWeaverProps {
    command: CommandDefinitionGUCAv5;
    onSubmit: (params: Record<string, any>) => void;
    onCancel: () => void;
}

const ParameterWeaver: React.FC<ParameterWeaverProps> = ({ command, onSubmit, onCancel }) => {
    const [values, setValues] = useState<Record<string, any>>({});

    useEffect(() => {
        const defaultValues: Record<string, any> = {};
        command.parameters.forEach((param) => {
            if (param.type === 'boolean') {
                defaultValues[param.name] = false;
            }
        });
        setValues(defaultValues);
    }, [command]);

    const handleValueChange = (paramName: string, value: any) => {
        setValues((prev) => ({ ...prev, [paramName]: value }));
    };

    const isFormValid = command.parameters.every(
        (param) =>
            !param.required ||
            (values[param.name] !== undefined &&
                values[param.name] !== null &&
                values[param.name] !== '')
    );

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (isFormValid) {
            // Transform data if necessary, specifically for array types
            const finalValues = { ...values };
            command.parameters.forEach((p) => {
                if (p.type === 'string[]' && typeof finalValues[p.name] === 'string') {
                    finalValues[p.name] = finalValues[p.name]
                        .split(',')
                        .map((s: string) => s.trim())
                        .filter((s: string) => s !== '');
                }
            });
            onSubmit(finalValues);
        }
    };

    const renderInput = (param: CommandDefinitionGUCAv5['parameters'][0]) => {
        // 1. Prioritize specific UI hints from the command definition
        if (param.uiHint === 'artifact') {
            let disabledId: string | null = null;
            if (command.commandId === 'CMD_SIMULATE_SYNERGY') {
                // Special logic to prevent selecting the same artifact twice
                const otherParam = command.parameters.find(
                    (p) => p.uiHint === 'artifact' && p.name !== param.name
                );
                if (otherParam) {
                    disabledId = values[otherParam.name];
                }
            }
            return (
                <ArtifactSelector
                    artifacts={graphData.nodes}
                    selectedId={values[param.name] || null}
                    onSelect={(id) => handleValueChange(param.name, id)}
                    placeholder={`Select ${param.name}`}
                    disabledId={disabledId}
                />
            );
        }

        if (param.uiHint === 'textarea') {
            return (
                <textarea
                    value={values[param.name] || ''}
                    onChange={(e) => handleValueChange(param.name, e.target.value)}
                    rows={4}
                    className="w-full bg-cyan-900/10 border border-cyan-400/30 rounded-md p-3 text-cyan-200 placeholder-cyan-400/50 focus:outline-none focus:ring-2 focus:ring-cyan-300/80 resize-none"
                />
            );
        }

        // 2. Fallback to rendering based on the parameter's data type
        switch (param.type) {
            case 'boolean':
                return (
                    <div className="flex items-center">
                        <input
                            type="checkbox"
                            id={param.name}
                            checked={!!values[param.name]}
                            onChange={(e) => handleValueChange(param.name, e.target.checked)}
                            className="w-4 h-4 bg-cyan-900/20 border-cyan-500/50 text-cyan-400 focus:ring-cyan-500/50 rounded"
                        />
                        <label htmlFor={param.name} className="ml-2 text-sm text-cyan-300">
                            Enabled
                        </label>
                    </div>
                );
            case 'number':
                return (
                    <input
                        type="number"
                        value={values[param.name] || ''}
                        onChange={(e) => handleValueChange(param.name, e.target.valueAsNumber)}
                        className="w-full bg-cyan-900/10 border border-cyan-400/30 rounded-md p-3 text-cyan-200 placeholder-cyan-400/50 focus:outline-none focus:ring-2 focus:ring-cyan-300/80"
                    />
                );
            case 'string':
            case 'string[]': // Handles string[] as a comma-separated text input which is transformed in handleSubmit
            default:
                return (
                    <input
                        type="text"
                        value={values[param.name] || ''}
                        onChange={(e) => handleValueChange(param.name, e.target.value)}
                        className="w-full bg-cyan-900/10 border border-cyan-400/30 rounded-md p-3 text-cyan-200 placeholder-cyan-400/50 focus:outline-none focus:ring-2 focus:ring-cyan-300/80"
                    />
                );
        }
    };

    return (
        <div className="p-4 md:p-8 h-full flex flex-col w-full max-w-7xl mx-auto animate-fade-in-sm">
            <div className="flex items-center gap-4 mb-2 shrink-0">
                <div className="p-3 bg-cyan-900/20 rounded-full border border-cyan-500/30">
                    <Zap className="w-8 h-8 text-cyan-400" />
                </div>
                <div>
                    <h3 className="text-3xl font-light text-cyan-100 tracking-wide">
                        parameter_weaving
                    </h3>
                    <p className="text-base text-cyan-400/60">
                        Configure arguments for{' '}
                        <strong className="font-mono text-cyan-200">{command.commandId}</strong>
                    </p>
                </div>
            </div>

            <form onSubmit={handleSubmit} className="mt-6 flex-1 flex flex-col min-h-0 relative">
                <div className="overflow-y-auto pr-2 pb-6 flex-1 custom-scrollbar">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {command.parameters.map((param) => (
                            <div
                                key={param.name}
                                className="flex flex-col gap-2 p-4 bg-black/20 rounded-lg border border-white/5 hover:border-cyan-500/20 transition-colors"
                            >
                                <label className="block text-lg font-medium text-cyan-200 tracking-wide flex items-center justify-between">
                                    {param.name}
                                    {param.required && (
                                        <span className="text-[10px] uppercase text-red-400/80 tracking-widest border border-red-500/20 px-1.5 py-0.5 rounded">
                                            Required
                                        </span>
                                    )}
                                </label>
                                <p className="text-sm text-cyan-400/50 mb-3 min-h-[40px]">
                                    {param.description}
                                </p>
                                <div className="flex-1 flex flex-col justify-end">
                                    {renderInput(param)}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="flex items-center justify-end gap-4 pt-6 mt-4 border-t border-cyan-500/10 bg-gray-900/95 backdrop-blur z-10">
                    <button
                        type="button"
                        onClick={onCancel}
                        className="px-6 py-3 bg-gray-800 hover:bg-gray-700/80 border border-gray-600/50 rounded-lg text-cyan-300 transition-colors text-sm uppercase tracking-widest"
                    >
                        Abort Sequence
                    </button>
                    <Tooltip
                        label={
                            isFormValid
                                ? `Execute ${command.commandId}`
                                : 'All required parameters must be filled'
                        }
                    >
                        <div>
                            <button
                                type="submit"
                                disabled={!isFormValid}
                                className="flex items-center gap-3 px-8 py-3 bg-cyan-600/20 hover:bg-cyan-500/30 border border-cyan-400/60 rounded-lg text-cyan-100 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-[0_0_20px_rgba(34,211,238,0.15)] hover:shadow-[0_0_30px_rgba(34,211,238,0.3)]"
                            >
                                <span className="font-semibold tracking-wider">INITIATE</span>
                                <CornerDownLeft className="w-5 h-5" />
                            </button>
                        </div>
                    </Tooltip>
                </div>
            </form>
        </div>
    );
};
export default ParameterWeaver;
