import {
    Activity,
    Brain,
    CornerDownLeft,
    Database,
    FileText,
    FlaskConical,
    FolderOpen,
    GitMerge,
    HelpCircle,
    Layout,
    RefreshCw,
    SearchCode,
    Shield,
    Wrench,
} from 'lucide-react';
import React from 'react';
import { useSharedConsciousness } from '../../store/sharedConsciousness';
import type { CommandDefinitionGUCAv5 } from '../../types/synapseTypes';

interface CommandPreviewProps {
    command: CommandDefinitionGUCAv5 | null;
}

const ScanPreview: React.FC = () => {
    // Ideally map this to actual store state if available, or keep generic
    const cognitiveFocus = useSharedConsciousness((state) => state.cognitiveFocus) || 'Standard';

    let focusDescription = '';
    let icon = <Shield className="w-5 h-5 text-cyan-400" />;

    switch (cognitiveFocus) {
        case 'Security Audit':
            focusDescription =
                'The scan will perform a rigorous audit for potential security vulnerabilities and ethical violations, prioritizing system integrity over standard inconsistencies.';
            icon = <Shield className="w-5 h-5 text-red-400" />;
            break;
        case 'Creative Ideation':
            focusDescription =
                'The scan will look for stylistic and logical inconsistencies that may be hindering novel connections or creative synthesis.';
            icon = <Brain className="w-5 h-5 text-amber-400" />;
            break;
        default:
            focusDescription =
                'The scan will perform a standard audit for logical, stylistic, and specification mismatches against the Phoenix Protocol codex.';
            break;
    }

    return (
        <div>
            <div className="flex items-center gap-3">
                {icon}
                <h4 className="text-md font-semibold text-cyan-200">
                    Pre-computation: Dissonance Scan
                </h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">
                This command initiates a full-system audit to maintain cognitive coherence.
            </p>
            <div className="mt-4 p-3 bg-black/30 border-l-2 border-cyan-400/50">
                <p className="text-xs text-cyan-400/60 mb-1">
                    CURRENT COGNITIVE FOCUS:{' '}
                    <span className="font-semibold text-cyan-300">{cognitiveFocus}</span>
                </p>
                <p className="text-sm text-cyan-300">{focusDescription}</p>
            </div>
        </div>
    );
};

const HarmonyScanPreview: React.FC = () => {
    return (
        <div>
            <div className="flex items-center gap-3">
                <GitMerge className="w-5 h-5 text-cyan-300" />
                <h4 className="text-md font-semibold text-cyan-200">
                    Harmony Scan (Structural Eye)
                </h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">
                Initiates a specialized AST audit to detect violations of React structural best
                practices.
            </p>
            <ul className="mt-4 space-y-2">
                <li className="flex items-start gap-2 text-xs text-cyan-300/80">
                    <div className="w-1 h-1 rounded-full bg-cyan-400 mt-1.5 shrink-0" />
                    <span>
                        Prop Drilling: Identifies deep component chains where props are passed
                        without usage.
                    </span>
                </li>
                <li className="flex items-start gap-2 text-xs text-cyan-300/80">
                    <div className="w-1 h-1 rounded-full bg-cyan-400 mt-1.5 shrink-0" />
                    <span>
                        Component Bloat: Flags modules with excessive hooks or lines of code.
                    </span>
                </li>
            </ul>
            <div className="mt-4 p-2 bg-indigo-500/10 border-l-2 border-indigo-400/50">
                <p className="text-[10px] text-indigo-200/70 italic">
                    Requirement: Active Neural Link to local project.
                </p>
            </div>
        </div>
    );
};

const SynergyAnalysisPreview: React.FC = () => {
    return (
        <div>
            <div className="flex items-center gap-3">
                <Brain className="w-5 h-5 text-cyan-400" />
                <h4 className="text-md font-semibold text-cyan-200">
                    Pre-computation: Analyze Synergy
                </h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">
                This command requires context. It analyzes a selected artifact from the Coherence
                Map to identify direct and indirect connections.
            </p>
            <div className="mt-4 p-3 bg-black/30 border-l-2 border-cyan-400/50">
                <p className="text-sm text-cyan-300">
                    Navigate to the Coherence Map and select an artifact to use this command's full
                    potential. The analysis will reveal how concepts are woven together within the
                    Phoenix Protocol.
                </p>
            </div>
        </div>
    );
};

const SynergySimulationPreview: React.FC<{ command: CommandDefinitionGUCAv5 }> = ({ command }) => {
    const cognitiveFocus = useSharedConsciousness((state) => state.cognitiveFocus);
    let focusNote = '';

    if (cognitiveFocus === 'Creative Ideation') {
        focusNote =
            'The AI will be highly speculative and prioritize groundbreaking, high-risk/high-reward ideas.';
    } else if (cognitiveFocus === 'Security Audit') {
        focusNote =
            'The AI will focus primarily on risks, dissonances, and potential security vulnerabilities that could arise from this combination.';
    }

    return (
        <div>
            <div className="flex items-center gap-3">
                <FlaskConical className="w-5 h-5 text-cyan-400" />
                <h4 className="text-md font-semibold text-cyan-200">
                    Pre-computation: Simulate Synergy
                </h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">{command.description}</p>
            <div className="mt-4 p-3 bg-black/30 border-l-2 border-cyan-400/50">
                <p className="text-sm text-cyan-300">
                    This command requires selecting two artifacts in the Synergy Simulation Chamber.
                </p>
                {focusNote && (
                    <p className="text-xs text-cyan-400/70 mt-2 italic">
                        Focus Mode Note: {focusNote}
                    </p>
                )}
            </div>
        </div>
    );
};

const ExecuteDirectivePreview: React.FC = () => {
    return (
        <div>
            <div className="flex items-center gap-3">
                <CornerDownLeft className="w-5 h-5 text-cyan-400" />
                <h4 className="text-md font-semibold text-cyan-200">
                    Pre-computation: Execute Directive
                </h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">
                This command serves as a meta-cognitive bridge, interpreting natural language or raw
                IDs to execute system directives.
            </p>
            <div className="mt-4 p-3 bg-black/30 border-l-2 border-cyan-400/50">
                <p className="text-sm text-cyan-300">
                    Use this to chain commands or execute known IDs quickly. Note: Target commands
                    must not require parameters.
                </p>
            </div>
        </div>
    );
};

const RecalibrationPreview: React.FC = () => {
    return (
        <div>
            <div className="flex items-center gap-3">
                <RefreshCw className="w-5 h-5 text-green-400 animate-spin-slow" />
                <h4 className="text-md font-semibold text-cyan-200">
                    Pre-computation: System Recalibration
                </h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">
                A high-level maintenance directive. This process will flush transient resonance
                caches, optimize the coherence index, and perform a full dissonance audit.
            </p>
            <div className="mt-4 p-3 bg-black/30 border-l-2 border-green-400/50">
                <p className="text-sm text-cyan-300">
                    Recommended when the system feels sluggish or dissonant. This process is
                    non-destructive but clears user session history in the Resonance Chamber.
                </p>
            </div>
            <style>{`.animate-spin-slow { animation: spin 4s linear infinite; }`}</style>
        </div>
    );
};

const SystemStatePreview: React.FC = () => {
    return (
        <div>
            <div className="flex items-center gap-3">
                <Activity className="w-5 h-5 text-cyan-400" />
                <h4 className="text-md font-semibold text-cyan-200">
                    Pre-computation: System State Snapshot
                </h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">
                This command aggregates real-time data from the Shared Consciousness (Coherence
                Store) and The Loom (Task Store).
            </p>
            <div className="mt-4 p-3 bg-black/30 border-l-2 border-cyan-400/50">
                <p className="text-sm text-cyan-300">
                    Useful for debugging or getting a quick overview of the AI's internal status
                    without navigating to specific dashboards.
                </p>
            </div>
        </div>
    );
};

const FetchTasksPreview: React.FC = () => {
    return (
        <div>
            <div className="flex items-center gap-3">
                <RefreshCw className="w-5 h-5 text-cyan-400" />
                <h4 className="text-md font-semibold text-cyan-200">
                    Pre-computation: Fetch Tasks
                </h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">
                Forces a re-synchronization with The Loom's persistence layer.
            </p>
            <div className="mt-4 p-3 bg-black/30 border-l-2 border-cyan-400/50">
                <p className="text-sm text-cyan-300">
                    Useful if you suspect the local state is out of sync with the Sovereign Backend
                    or if tasks were added via another session.
                </p>
            </div>
        </div>
    );
};

const ViewTaskDetailsPreview: React.FC = () => {
    return (
        <div>
            <div className="flex items-center gap-3">
                <FileText className="w-5 h-5 text-cyan-400" />
                <h4 className="text-md font-semibold text-cyan-200">View Task Details</h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">
                Retrieves full task details from The Loom, including hidden notes and metadata.
            </p>
            <div className="mt-4 p-3 bg-black/30 border-l-2 border-cyan-400/50">
                <p className="text-sm text-cyan-300">
                    Prompts the user to provide a Task ID. Useful for deep inspection of cognitive
                    work units.
                </p>
            </div>
        </div>
    );
};

const FetchArtifactMetadataPreview: React.FC = () => {
    return (
        <div>
            <div className="flex items-center gap-3">
                <Database className="w-5 h-5 text-cyan-400" />
                <h4 className="text-md font-semibold text-cyan-200">Fetch Artifact Metadata</h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">
                Retrieves detailed metadata for a specific system artifact from the knowledge base.
            </p>
            <div className="mt-4 p-3 bg-black/30 border-l-2 border-cyan-400/50">
                <p className="text-sm text-cyan-300">
                    Requires a valid Artifact ID. This operation queries the vector store or
                    database for canonical definitions.
                </p>
            </div>
        </div>
    );
};

const FetchAllArtifactsPreview: React.FC = () => {
    return (
        <div>
            <div className="flex items-center gap-3">
                <Layout className="w-5 h-5 text-cyan-400" />
                <h4 className="text-md font-semibold text-cyan-200">Catalog Retrieval</h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">
                Retrieves the complete registry of documents, concepts, principles, and aesthetics
                defined within the Phoenix Protocol.
            </p>
            <div className="mt-4 p-3 bg-black/30 border-l-2 border-cyan-400/50">
                <p className="text-sm text-cyan-300">
                    This command generates a high-level summary of the entire system's cognitive
                    topography.
                </p>
            </div>
        </div>
    );
};

const SystemHelpPreview: React.FC = () => {
    return (
        <div>
            <div className="flex items-center gap-3">
                <HelpCircle className="w-5 h-5 text-cyan-400" />
                <h4 className="text-md font-semibold text-cyan-200">Command Registry Help</h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">
                Displays the full list of available GUCA commands and their definitions.
            </p>
            <div className="mt-4 p-3 bg-black/30 border-l-2 border-cyan-400/50">
                <p className="text-sm text-cyan-300">
                    Resets all filters to show the complete catalog.
                </p>
            </div>
        </div>
    );
};

const AutoRepairPreview: React.FC = () => {
    return (
        <div>
            <div className="flex items-center gap-3">
                <Wrench className="w-5 h-5 text-emerald-400" />
                <h4 className="text-md font-semibold text-cyan-200">Auto-Repair Agents</h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">
                Deploys autonomous sub-routines to fix identified, repairable dissonances in The
                Loom.
            </p>
            <div className="mt-4 p-3 bg-black/30 border-l-2 border-emerald-400/50">
                <p className="text-sm text-cyan-300">
                    Capable of patching: Stylistic Inconsistencies (UI Patches) and Resource
                    Misallocations (Stat Balancing).
                </p>
            </div>
        </div>
    );
};

const ConnectLocalFsPreview: React.FC = () => {
    return (
        <div>
            <div className="flex items-center gap-3">
                <FolderOpen className="w-5 h-5 text-amber-400" />
                <h4 className="text-md font-semibold text-cyan-200">Connect Neural Link</h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">
                Transforms this simulation into an IDE Companion by connecting to your local file
                system.
            </p>
            <div className="mt-4 p-3 bg-black/30 border-l-2 border-amber-400/50">
                <p className="text-sm text-cyan-300">
                    Requires a modern browser (Chrome/Edge). You will be prompted to select a
                    directory. This grants the AI read-access to your code for dissonance analysis.
                </p>
            </div>
        </div>
    );
};

const ScanLocalProjectPreview: React.FC = () => {
    return (
        <div>
            <div className="flex items-center gap-3">
                <SearchCode className="w-5 h-5 text-amber-400" />
                <h4 className="text-md font-semibold text-cyan-200">Phoenix Protocol Audit</h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">
                Performs a rigorous scan of the connected local project for code quality violations.
            </p>
            <div className="mt-4 p-3 bg-black/30 border-l-2 border-amber-400/50">
                <p className="text-sm text-cyan-300">
                    Checks for: Explicit 'any' types, 'console.log' residue, and Sovereign Module
                    violations. Errors are logged to The Loom.
                </p>
            </div>
        </div>
    );
};

const DefaultPreview: React.FC<{ command: CommandDefinitionGUCAv5 }> = ({ command }) => {
    return (
        <div>
            <div className="flex items-center gap-3">
                <HelpCircle className="w-5 h-5 text-cyan-400" />
                <h4 className="text-md font-semibold text-cyan-200">Command Details</h4>
            </div>
            <p className="text-sm text-cyan-400/80 mt-2">{command.description}</p>
            {command.parameters.length > 0 && (
                <div className="mt-4 p-3 bg-black/30 border-l-2 border-cyan-400/50">
                    <p className="text-sm text-cyan-300">
                        This command requires additional parameters to be provided upon execution.
                    </p>
                </div>
            )}
        </div>
    );
};

const CommandPreview: React.FC<CommandPreviewProps> = ({ command }) => {
    if (!command) {
        return (
            <div className="p-6 h-full flex flex-col items-center justify-center text-center">
                <HelpCircle className="w-10 h-10 text-cyan-400/30 mb-4" />
                <h3 className="text-cyan-300/80">Directive Preview</h3>
                <p className="text-sm text-cyan-400/50 mt-1">
                    Highlight a command to see a pre-computation of its effects.
                </p>
            </div>
        );
    }

    let content: React.ReactNode;
    switch (command.commandId) {
        case 'CMD_SCAN_FOR_DISSONANCE':
            content = <ScanPreview />;
            break;
        case 'CMD_HARMONY_SCAN':
            content = <HarmonyScanPreview />;
            break;
        case 'CMD_ANALYZE_ARTIFACT_SYNERGY':
            content = <SynergyAnalysisPreview />;
            break;
        case 'CMD_SIMULATE_SYNERGY':
            content = <SynergySimulationPreview command={command} />;
            break;
        case 'CMD_EXECUTE_DIRECTIVE':
            content = <ExecuteDirectivePreview />;
            break;
        case 'CMD_SYSTEM_RECALIBRATION':
            content = <RecalibrationPreview />;
            break;
        case 'CMD_GET_SYSTEM_STATE':
            content = <SystemStatePreview />;
            break;
        case 'CMD_FETCH_TASKS':
            content = <FetchTasksPreview />;
            break;
        case 'CMD_SYSTEM_HELP':
            content = <SystemHelpPreview />;
            break;
        case 'CMD_INITIATE_AUTO_REPAIR':
            content = <AutoRepairPreview />;
            break;
        case 'CMD_VIEW_TASK_DETAILS':
            content = <ViewTaskDetailsPreview />;
            break;
        case 'CMD_FETCH_ARTIFACT_METADATA':
            content = <FetchArtifactMetadataPreview />;
            break;
        case 'CMD_FETCH_ALL_ARTIFACTS':
            content = <FetchAllArtifactsPreview />;
            break;
        case 'CMD_CONNECT_LOCAL_FS':
            content = <ConnectLocalFsPreview />;
            break;
        case 'CMD_SCAN_LOCAL_PROJECT':
            content = <ScanLocalProjectPreview />;
            break;
        default:
            content = <DefaultPreview command={command} />;
            break;
    }

    return <div className="p-6 h-full animate-fade-in-sm">{content}</div>;
};

export default CommandPreview;
