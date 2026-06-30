import type { CommandDefinitionGUCAv5 } from '@essence/codex';

// --- Web Speech API Extensions ---
export interface SpeechRecognitionEvent extends Event {
    readonly resultIndex: number;
    readonly results: SpeechRecognitionResultList;
}

export interface SpeechRecognitionErrorEvent extends Event {
    readonly error: string;
    readonly message: string;
}

export interface SpeechRecognition extends EventTarget {
    continuous: boolean;
    interimResults: boolean;
    lang: string;
    onresult: (event: SpeechRecognitionEvent) => void;
    onerror: (event: SpeechRecognitionErrorEvent) => void;
    onend: () => void;
    start: () => void;
    stop: () => void;
    abort: () => void;
}

declare global {
    interface Window {
        webkitSpeechRecognition: new () => SpeechRecognition;
        SpeechRecognition: new () => SpeechRecognition;
        webkitAudioContext: typeof AudioContext;
        showDirectoryPicker: (options?: { mode?: 'read' | 'readwrite' }) => Promise<FileSystemDirectoryHandle>;
    }
}

// --- File System Access API Types ---
export interface FileSystemHandle {
    readonly kind: 'file' | 'directory';
    readonly name: string;
}

export interface FileSystemDirectoryHandle extends FileSystemHandle {
    queryPermission(arg0: { mode: string }): unknown;
    readonly kind: 'directory';
    values: () => AsyncIterableIterator<FileSystemHandle>;
    getDirectoryHandle: (name: string, options?: { create?: boolean }) => Promise<FileSystemDirectoryHandle>;
    getFileHandle: (name: string, options?: { create?: boolean }) => Promise<FileSystemFileHandle>;
}

export interface FileSystemWritableFileStream extends WritableStream {
    write: (data: string | BufferSource | Blob) => Promise<void>;
    seek: (position: number) => Promise<void>;
    truncate: (size: number) => Promise<void>;
}

export interface FileSystemFileHandle extends FileSystemHandle {
    readonly kind: 'file';
    getFile: () => Promise<File>;
    createWritable: (options?: { keepExistingData?: boolean }) => Promise<FileSystemWritableFileStream>;
    requestPermission: (descriptor: { mode: 'read' | 'readwrite' }) => Promise<PermissionState>;
}

export interface LocalFile {
    path: string;
    name: string;
    content: string;
    handle: FileSystemFileHandle;
}

export interface CoreStat {
    value: number;
    max: number;
}

export interface StatusEffect {
    id: string;
    name: string;
    type: 'buff' | 'debuff';
    iconName: string;
    description: string;
}

export interface NovaSpark {
    id: string;
    timestamp: number;
    timeString?: string;
    summary: string;
}

export type TaskStatus = 'To Do' | 'In Progress' | 'Completed';
export type TaskSource = 'Manual' | 'Dissonance Scanner' | 'Synergy Simulator' | 'Neural Link';
export type TaskPriority = 'Low' | 'Medium' | 'High';

export interface TaskAuditEntry {
    timestamp: number;
    action: 'Fixed Error' | 'Caused Error' | 'Comment' | 'Status Change';
    details: string;
}

export interface Task {
    id: string;
    title: string;
    notes: string;
    status: TaskStatus;
    source: TaskSource;
    priority: TaskPriority;
    timestamp: number;
    auditLog?: TaskAuditEntry[];
}

export type WeaverValue = string | number | boolean | string[] | null;

export type CognitiveFocus = 'Standard' | 'Creative Ideation' | 'Security Audit' | 'Strategy';

export interface GroundingSource {
    uri: string;
    title: string;
    notes?: string;
}

export interface GroundedResponse {
    text: string;
    sources: GroundingSource[];
}

// --- Sensory Bridge Interfaces ---
export interface SensoryData {
    timestamp: number;
    timeString: string;
    location: {
        lat: number;
        lng: number;
        description: string;
    } | null;
    weather: {
        temperature: number;
        conditionCode: number;
        conditionText: string;
        isDay: boolean;
        windSpeed: number;
    } | null;
    status: 'offline' | 'calibrating' | 'online';
}

export interface CoherenceState {
    coherenceIndex: number;
    pulse: () => void;
    decay: () => void;
    prestigeLevel: number;
    xp: {
        current: number;
        nextLevel: number;
    };
    stardust: number;
    cognitiveLoad: number;
    coreStats: {
        coherence: CoreStat;
        synergy: CoreStat;
        adaptability: CoreStat;
        transparency: CoreStat;
    };
    statusEffects: StatusEffect[];
    novaSparks: NovaSpark[];
    cognitiveFocus: CognitiveFocus;
    isDreaming: boolean;
    sensoryData: SensoryData;
    investStardust: (stat: keyof CoherenceState['coreStats']) => void;
    addNovaSpark: (summary: string) => void;
    setCognitiveFocus: (focus: CognitiveFocus) => void;
    setDreaming: (isDreaming: boolean) => void;
    updateSensoryData: (data: Partial<SensoryData>) => void;
}

export interface CommandUsage {
    count: number;
    lastUsed: number;
}

export interface ScoredCommand {
    command: CommandDefinitionGUCAv5;
    score: number;
    usage: CommandUsage | null;
}

export interface DispatchResult {
    success: boolean;
    message: string;
    data?: Record<string, unknown>;
}

export interface SystemContext {
    tasks: Task[];
    coherence: {
        index: number;
        focus: CognitiveFocus;
        stats: CoherenceState['coreStats'];
    };
    sensory?: SensoryData;
    currentLocation?: string;
}

export interface DynamicStateInfusion {
    COGNITIVE_LOAD_INDEX: number;
    ACTIVATED_NEURAL_PATHWAYS: string[];
    EMOTIONAL_PROXY_STATE: string;
}

export interface InteractionAnalysis {
    inferredIntent: string;
    detectedTopics: string[];
    sentimentScore: number;
}

export interface UserTurnLog {
    timestamp: string;
    participant: 'User';
    verbatimContent: string;
    analysis: InteractionAnalysis;
}

export interface AgentResponseLog {
    timestamp: string;
    participant: 'Agent';
    verbatimContent: string;
    reasoning: {
        agentIntent: string;
        retrievalMethods: string[];
        retrievalDetails?: {
            sources: string[];
        };
    };
}

export interface PhenomenologicalState {
    decisionPathway: string;
    internalConsistency: string;
}

export interface ExperienceLog {
    logId: string;
    timestamp: string;
    sessionId: string;
    dynamicState: DynamicStateInfusion;
    userTurn: UserTurnLog;
    agentResponse: AgentResponseLog;
    phenomenologicalState: PhenomenologicalState;
    contextualMeta: {
        moduleOfOrigin: string;
        cognitiveFocus: CognitiveFocus;
        location: string;
    };
}

export interface Violation {
    file: string;
    line: number;
    type: string;
    message: string;
    start?: number;
    end?: number;
    severity?: string;
}

export interface AnalysisReport {
    violations: Violation[];
    dependencyGraph: Record<string, unknown>;
    cycles: string[][];
    propDrillingPaths: string[][];
    styleMetrics: {
        totalClasses: number;
        variablesUsed: number;
        hardcodedColors: number;
        deepSelectors: number;
    };
    stats: {
        filesParsed: number;
        totalImports: number;
    };
}

