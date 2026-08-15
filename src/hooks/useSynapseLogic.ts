// [OMEGA AST Cleaned]: Tokenized design standards applied.
/**
 * Core Logic: src/hooks/useSynapseLogic.ts
 * Visual Interface: src/components/TheSynapse.tsx (now exporting SynapseInterface)
 * Superposition Demo: src/components/pages/ArtifactCatalogPage.tsx (Neural Assistant)
 */
import { useEffect, useMemo, useRef, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useAuralInterface } from './useAuralInterface';
import { DispatchResult, WeaverValue } from '@essence/types';
import { CommandDefinitionGUCAv5 } from '@essence/codex';
import { 
    interpretNaturalLanguageCommand, 
    getEchoCommands, 
    getResonantCommands, 
    trackCommandExecution,
    signalBus,
    SignalType 
} from '../services';

export interface SynapseLogicOptions {
    registry: Record<string, CommandDefinitionGUCAv5>;
    dispatchCommand: (command: CommandDefinitionGUCAv5, params: Record<string, any>) => Promise<DispatchResult>;
    onNovaSpark?: (message: string) => void;
    cognitiveFocus?: string;
    isGlobal?: boolean;
    initialSearchQuery?: string;
}

export type CommandWithMetadata = CommandDefinitionGUCAv5 & {
    isEcho: boolean;
    isResonant: boolean;
};

export const useSynapseLogic = ({
    registry,
    dispatchCommand,
    onNovaSpark,
    cognitiveFocus = 'Neutral',
    isGlobal = false,
    initialSearchQuery = ''
}: SynapseLogicOptions) => {
    const [searchQuery, setSearchQuery] = useState(initialSearchQuery);
    const [selectedIndex, setSelectedIndex] = useState(0);
    const [confirmationCandidate, setConfirmationCandidate] = useState<CommandDefinitionGUCAv5 | null>(null);
    const [commandForParams, setCommandForParams] = useState<CommandDefinitionGUCAv5 | null>(null);
    const [isClcMode, setIsClcMode] = useState(false);
    const [currentConstruction, setCurrentConstruction] = useState<CommandDefinitionGUCAv5[]>([]);
    const [isFiring, setIsFiring] = useState(false);
    const [commandResult, setCommandResult] = useState<DispatchResult | null>(null);
    const [visualContext, setVisualContext] = useState<{ data: string; name: string } | null>(null);

    const interpretationTimeoutRef = useRef<number | null>(null);
    const location = useLocation();

    // Voice Interface - Only active if isGlobal is true
    const aural = useAuralInterface();
    
    useEffect(() => {
        if (isGlobal && aural.transcript && aural.transcript !== searchQuery) {
            setSearchQuery(aural.transcript);
        }
    }, [isGlobal, aural.transcript, searchQuery]);

    const commands = useMemo(() => Object.values(registry), [registry]);
    
    // Command Resonance - Only if global
    const resonantCommands = useMemo(() => {
        if (!isGlobal) return [];
        return getResonantCommands(commands, 3);
    }, [commands, isGlobal]);

    const resetState = () => {
        setSearchQuery('');
        setConfirmationCandidate(null);
        setCommandForParams(null);
        setIsClcMode(false);
        setCurrentConstruction([]);
        setIsFiring(false);
        setCommandResult(null);
        setVisualContext(null);
        if (isGlobal) aural.resetTranscript();
    };

    const filteredCommands = useMemo<CommandWithMetadata[]>(() => {
        if (confirmationCandidate) return [{ ...confirmationCandidate, isEcho: false, isResonant: false }];
        
        let matches = commands;
        if (searchQuery) {
            const lowerQuery = searchQuery.toLowerCase();
            matches = commands.filter(
                (cmd) =>
                    cmd.commandId.toLowerCase().includes(lowerQuery) ||
                    cmd.description.toLowerCase().includes(lowerQuery) ||
                    cmd.aliases?.some((alias) => alias.toLowerCase().includes(lowerQuery)),
            );
        }

        const echoIds = isGlobal ? getEchoCommands(location.pathname, cognitiveFocus as any) : [];
        const resonantIds = resonantCommands.map((c) => c.commandId);

        return matches
            .map((cmd) => ({
                ...cmd,
                isEcho: echoIds.includes(cmd.commandId),
                isResonant: resonantIds.includes(cmd.commandId),
            }))
            .sort((a, b) => {
                if (a.isEcho !== b.isEcho) return a.isEcho ? -1 : 1;
                if (a.isResonant !== b.isResonant) return a.isResonant ? -1 : 1;
                return 0;
            });
    }, [searchQuery, commands, confirmationCandidate, location.pathname, cognitiveFocus, resonantCommands, isGlobal]);

    // NLP Interpretation
    useEffect(() => {
        if (searchQuery && filteredCommands.length === 0 && !confirmationCandidate) {
            if (interpretationTimeoutRef.current) clearTimeout(interpretationTimeoutRef.current);
            interpretationTimeoutRef.current = window.setTimeout(() => {
                void (async () => {
                    const interpretedId = await interpretNaturalLanguageCommand(searchQuery);
                    if (interpretedId && interpretedId in registry) {
                        setConfirmationCandidate(registry[interpretedId]);
                        setSelectedIndex(0);
                    }
                })();
            }, 800);
        }
        return () => {
            if (interpretationTimeoutRef.current) clearTimeout(interpretationTimeoutRef.current);
        };
    }, [searchQuery, filteredCommands.length, confirmationCandidate, registry]);

    const executeCommand = async (command: CommandDefinitionGUCAv5, params: Record<string, WeaverValue>) => {
        setIsFiring(true);
        if (isGlobal) trackCommandExecution(command.commandId);
        
        // --- [SIGNAL BUS EMISSION] ---
        signalBus.emit(SignalType.SYNERGY_FIRE, { commandId: command.commandId, params }, { isGlobal });
        signalBus.emit(SignalType.COHERENCE_RIPPLE, { intensity: 0.8 }, { isGlobal });
        signalBus.emit(SignalType.AURAL_ECHO, { type: 'neutral' }, { isGlobal });
        // -----------------------------

        const result = await dispatchCommand(command, { ...params, visualContext });
        
        setIsFiring(false);
        setCommandResult(result);
        
        if (onNovaSpark && result.success) {
            onNovaSpark(`Directive Manifested: ${command.commandId}`);
        }
        
        signalBus.emit(SignalType.SYNERGY_RESULT, { success: result.success, message: result.message }, { isGlobal });
    };

    const handleSelectCommand = (command: CommandDefinitionGUCAv5) => {
        if (command.commandId === 'CMD_BEGIN_CLC') {
            setIsClcMode(true);
            setSearchQuery('');
            return;
        }

        if (isClcMode) {
            setCurrentConstruction((prev) => [...prev, command]);
            setSearchQuery('');
            if (onNovaSpark) onNovaSpark(`Chain Augmented: ${command.commandId}`);
        } else {
            if (command.parameters.length > 0) {
                setCommandForParams(command);
            } else {
                void executeCommand(command, {});
            }
        }
    };

    const executeChain = async () => {
        if (currentConstruction.length === 0) return;
        setIsFiring(true);

        // --- [SIGNAL BUS EMISSION] ---
        signalBus.emit(SignalType.SYNERGY_FIRE, { chain: currentConstruction.map(c => c.commandId) }, { isGlobal });
        signalBus.emit(SignalType.COHERENCE_RIPPLE, { intensity: 1.0 }, { isGlobal });
        // -----------------------------

        const messages: string[] = [];
        let allSuccess = true;

        for (const cmd of currentConstruction) {
            const res = await dispatchCommand(cmd, { visualContext });
            if (!res.success) allSuccess = false;
            messages.push(`[${cmd.commandId}]: ${res.message}`);
        }

        setIsFiring(false);
        setCommandResult({
            success: allSuccess,
            message: allSuccess ? 'Neural chain executed successfully.' : 'Dissonance detected in command chain.',
            data: { log: messages },
        });

        signalBus.emit(SignalType.SYNERGY_RESULT, { success: allSuccess, chain: true }, { isGlobal });
    };

    return {
        state: {
            searchQuery,
            selectedIndex,
            confirmationCandidate,
            commandForParams,
            isClcMode,
            currentConstruction,
            isFiring,
            commandResult,
            visualContext,
            filteredCommands,
            isListening: aural.isListening
        },
        actions: {
            setSearchQuery,
            setSelectedIndex,
            setConfirmationCandidate,
            setCommandForParams,
            setVisualContext,
            setCurrentConstruction,
            resetState,
            handleSelectCommand,
            executeCommand,
            executeChain,
            startListening: aural.startListening,
            stopListening: aural.stopListening
        }
    };
};

