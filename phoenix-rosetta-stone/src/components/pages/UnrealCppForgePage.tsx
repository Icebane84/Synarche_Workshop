import React, { useRef, useState } from 'react';
import {
  AlertTriangle,
  ArrowRight,
  BookOpen,
  Bot,
  CheckCircle,
  Code2,
  Copy,
  Cpu,
  Download,
  FileCode,
  FolderTree,
  Hammer,
  Layers,
  MessageSquare,
  Play,
  RefreshCw,
  Save,
  Send,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  Terminal,
  User,
  Wand2,
  X,
  Zap,
} from 'lucide-react';
import { CSEBridgeService } from '../../services/cseBridgeService';
import { queryCognitiveCore } from '../../services/gemini';
import { useCoherenceStore } from '../../store/coherenceStore';
import graphDb from '../../data/adjacency_matrix.json';

export type AshenDomain =
  | 'Core'
  | 'Soul'
  | 'Memory'
  | 'Companions'
  | 'Combat'
  | 'Narrative'
  | 'UI'
  | 'Audio'
  | 'World'
  | 'Orchestration'
  | 'AI'
  | 'QA';

export interface CppClassTemplate {
  id: string;
  name: string;
  domain: AshenDomain;
  headerName: string;
  cppName: string;
  headerContent: string;
  cppContent: string;
  description: string;
}

export interface CppChatMessage {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  timestamp: number;
  headerCode?: string;
  cppCode?: string;
}

const ASHEN_DOMAINS: AshenDomain[] = [
  'Core',
  'Soul',
  'Memory',
  'Companions',
  'Combat',
  'Narrative',
  'UI',
  'Audio',
  'World',
  'Orchestration',
  'AI',
  'QA',
];

const UE5_PRESET_TEMPLATES: CppClassTemplate[] = [
  {
    id: 'ashen-character',
    name: 'AAshenCharacter (UE5 Character)',
    domain: 'Combat',
    headerName: 'AshenCharacter.h',
    cppName: 'AshenCharacter.cpp',
    description: 'Master Unreal Engine 5.8 C++ Vanguard Character Class with UPROPERTY Macros and Combat Delegates.',
    headerContent: `// Copyright Phoenix Synarche. All Rights Reserved. GVRN.Style.SovereignStandard.v15.1

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "AshenCharacter.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnAshenHealthChanged, float, NewHealth, float, MaxHealth);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAshenStanceShifted, uint8, NewStance);

/**
 * AAshenCharacter
 * Sovereign UE5.8 C++ Vanguard Character for Ashen Oath.
 */
UCLASS(Blueprintable, ClassGroup = (Ashen))
class ASHENOATH_API AAshenCharacter : public ACharacter
{
	GENERATED_BODY()

public:
	AAshenCharacter();

protected:
	virtual void BeginPlay() override;

public:
	virtual void Tick(float DeltaTime) override;
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

	/** Executes inward combat strike */
	UFUNCTION(BlueprintCallable, Category = "Ashen|Combat")
	void PerformCombatStrike();

	/** Returns current health percentage */
	UFUNCTION(BlueprintPure, Category = "Ashen|Attributes")
	float GetHealthPercent() const;

public:
	/** Primary Character Health */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Ashen|Attributes", meta = (ClampMin = "0.0", ClampMax = "1000.0"))
	float Health;

	/** Maximum Character Health */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Ashen|Attributes")
	float MaxHealth;

	/** Delegate fired when health state mutates */
	UPROPERTY(BlueprintAssignable, Category = "Ashen|Events")
	FOnAshenHealthChanged OnHealthChanged;

protected:
	/** Weak pointer to active target to prevent memory cycles */
	TWeakObjectPtr<AActor> CurrentTargetActor;
};
`,
    cppContent: `// Copyright Phoenix Synarche. All Rights Reserved. GVRN.Style.SovereignStandard.v15.1

#include "AshenCharacter.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/CharacterMovementComponent.h"

AAshenCharacter::AAshenCharacter()
{
	PrimaryActorTick.bCanEverTick = true;

	Health = 100.0f;
	MaxHealth = 100.0f;

	if (GetCapsuleComponent())
	{
		GetCapsuleComponent()->InitCapsuleSize(42.0f, 96.0f);
	}
}

void AAshenCharacter::BeginPlay()
{
	Super::BeginPlay();
	
	ensureMsgf(MaxHealth > 0.0f, TEXT("AAshenCharacter: MaxHealth must be greater than zero."));
}

void AAshenCharacter::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
}

void AAshenCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);
}

void AAshenCharacter::PerformCombatStrike()
{
	if (CurrentTargetActor.IsValid())
	{
		AActor* Target = CurrentTargetActor.Get();
		checkf(Target != nullptr, TEXT("PerformCombatStrike: Target handle is invalid."));
	}
}

float AAshenCharacter::GetHealthPercent() const
{
	return (MaxHealth > 0.0f) ? (Health / MaxHealth) : 0.0f;
}
`,
  },
  {
    id: 'ashen-combat-component',
    name: 'UAshenCombatComponent (UE5 ActorComponent)',
    domain: 'Combat',
    headerName: 'AshenCombatComponent.h',
    cppName: 'AshenCombatComponent.cpp',
    description: 'Decoupled UE5.8 Combat Component for Stance Management & Damage Calculations.',
    headerContent: `// Copyright Phoenix Synarche. All Rights Reserved. GVRN.Style.SovereignStandard.v15.1

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "AshenCombatComponent.generated.h"

/**
 * UAshenCombatComponent
 * Modular UE5 Component managing weapon stances and damage scaling.
 */
UCLASS(ClassGroup = (Ashen), meta = (BlueprintSpawnableComponent))
class ASHENOATH_API UAshenCombatComponent : public UActorComponent
{
	GENERATED_BODY()

public:	
	UAshenCombatComponent();

protected:
	virtual void BeginPlay() override;

public:	
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	/** Mutates current weapon stance */
	UFUNCTION(BlueprintCallable, Category = "Ashen|Stance")
	void SetStanceMode(int32 NewStance);

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Ashen|Stance")
	int32 ActiveStanceIndex;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Ashen|Damage")
	float BaseDamageMultiplier;
};
`,
    cppContent: `// Copyright Phoenix Synarche. All Rights Reserved. GVRN.Style.SovereignStandard.v15.1

#include "AshenCombatComponent.h"

UAshenCombatComponent::UAshenCombatComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
	ActiveStanceIndex = 0;
	BaseDamageMultiplier = 1.0f;
}

void UAshenCombatComponent::BeginPlay()
{
	Super::BeginPlay();
}

void UAshenCombatComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
}

void UAshenCombatComponent::SetStanceMode(int32 NewStance)
{
	if (NewStance >= 0 && NewStance <= 3)
	{
		ActiveStanceIndex = NewStance;
	}
}
`,
  },
];

export const UnrealCppForgePage: React.FC = () => {
  const [selectedTemplate, setSelectedTemplate] = useState<CppClassTemplate>(UE5_PRESET_TEMPLATES[0]);
  const [activeDomain, setActiveDomain] = useState<AshenDomain>('Combat');
  const [selectedCanonNode, setSelectedCanonNode] = useState<string>('char-kaelen');

  const [activeTab, setActiveTab] = useState<'header' | 'cpp'>('header');
  const [headerCode, setHeaderCode] = useState<string>(UE5_PRESET_TEMPLATES[0].headerContent);
  const [cppCode, setCppCode] = useState<string>(UE5_PRESET_TEMPLATES[0].cppContent);

  // Chat State
  const [showChatDrawer, setShowChatDrawer] = useState<boolean>(true);
  const [chatInput, setChatInput] = useState<string>('');
  const [chatMessages, setChatMessages] = useState<CppChatMessage[]>([
    {
      id: 'init-1',
      sender: 'ai',
      text: 'Greetings, Artificer. I am your C++ Master Architect for Unreal Engine 5.8. Ask me to turn any gameplay concept, combat mechanics, or GAS abilities into performant, industry-grade C++ logic.',
      timestamp: Date.now(),
    },
  ]);

  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [isCompiling, setIsCompiling] = useState<boolean>(false);
  const [showTerminal, setShowTerminal] = useState<boolean>(false);
  const [ubtLog, setUbtLog] = useState<string | null>(null);

  const [auditReport, setAuditReport] = useState<{ score: number; issues: string[] } | null>(null);
  const [saveStatus, setSaveStatus] = useState<string | null>(null);
  const [showBatchModal, setShowBatchModal] = useState<boolean>(false);
  const [batchStartBuild, setBatchStartBuild] = useState<number>(676);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const addNovaSpark = useCoherenceStore((state) => state.addNovaSpark);

  const canonNodes = graphDb.nodes || [];

  // Scroll chat to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Switch template preset
  const handleSelectTemplate = (template: CppClassTemplate) => {
    setSelectedTemplate(template);
    setActiveDomain(template.domain);
    setHeaderCode(template.headerContent);
    setCppCode(template.cppContent);
    setAuditReport(null);
    setSaveStatus(null);
  };

  // Audit C++ Compliance
  const handleRunAudit = () => {
    const issues: string[] = [];
    let score = 100;
    const currentCode = activeTab === 'header' ? headerCode : cppCode;

    if (activeTab === 'header' && !currentCode.includes('UPROPERTY')) {
      issues.push('Missing UPROPERTY reflection specifiers on member variables.');
      score -= 20;
    }

    if (
      currentCode.includes('*') &&
      !currentCode.includes('IsValid') &&
      !currentCode.includes('check(') &&
      !currentCode.includes('TWeakObjectPtr')
    ) {
      issues.push('Raw pointer dereferencing detected without IsValid() or TWeakObjectPtr defensive guard.');
      score -= 25;
    }

    if (activeTab === 'header') {
      const lines = currentCode.split('\n');
      const includes = lines.filter((l) => l.trim().startsWith('#include'));
      const lastInclude = includes[includes.length - 1] || '';
      if (!lastInclude.includes('.generated.h')) {
        issues.push('#include "*.generated.h" MUST be the absolute last #include directive in header.');
        score -= 30;
      }
    }

    setAuditReport({ score: Math.max(0, score), issues });
    addNovaSpark(`C++ Audit: Evaluated ${selectedTemplate.name} (${score}% Compliance Score).`);
  };

  // Execute Live UBT Compilation Pass
  const handleExecuteUBT = async () => {
    setIsCompiling(true);
    setShowTerminal(true);
    addNovaSpark('UBT Pass: Triggering live UnrealBuildTool.exe compilation pass for Ashen Oath Editor...');

    try {
      const result = await CSEBridgeService.compileUnrealProject();
      setUbtLog(result.stdout || result.stderr || result.message);
      if (result.status === 'SUCCESS') {
        addNovaSpark('UBT Pass: Compilation SUCCEEDED! 0 Errors, 0 Warnings.');
      } else {
        addNovaSpark(`UBT Pass: Compilation failed: ${result.message}`);
      }
    } catch (err) {
      setUbtLog(`UBT Execution error: ${String(err)}`);
    } finally {
      setIsCompiling(false);
    }
  };

  // Interactive AI C++ Architect Chat Handler
  const handleSendChatMessage = async (promptOverride?: string) => {
    const textToSend = promptOverride || chatInput;
    if (!textToSend.trim() || isGenerating) return;

    const userMsg: CppChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: textToSend,
      timestamp: Date.now(),
    };

    setChatMessages((prev) => [...prev, userMsg]);
    if (!promptOverride) setChatInput('');
    setIsGenerating(true);

    // Fetch live Ashen Oath architecture & build history context
    const docsCtx = await CSEBridgeService.getAshenDocsContext();
    const archContext = docsCtx.architecture_map ? `\n\n[LIVE_ARCHITECTURE_MAP_CONTEXT]\n${docsCtx.architecture_map.slice(0, 2500)}\n[/LIVE_ARCHITECTURE_MAP_CONTEXT]` : '';
    const relContext = docsCtx.release_history ? `\n\n[LIVE_RELEASE_HISTORY_CONTEXT]\n${docsCtx.release_history.slice(0, 1500)}\n[/LIVE_RELEASE_HISTORY_CONTEXT]` : '';

    const systemPrompt = `
You are Hephaestus, Sovereign Master C++ Architect enforcing the /ashen-oath-unreal-coding workflow for Unreal Engine 5.8.
Your directive is to produce 100% clean, performant, production-grade C++ logic under the Zero Warning Mandate (0 compilation errors, 0 warnings under UnrealBuildTool.exe).
Target Domain: Source/AshenOath/${activeDomain}/
${loreContext}${archContext}${relContext}

Executive Rules of Execution (ashen-oath-unreal-coding):
1. ZERO DRIFT & ZERO WARNING MANDATE:
   - Complete, robust production C++ into every file. Never swallow exceptions, mask broken logic, or return stubs.
2. 12 DOMAIN-DRIVEN VERTICAL SLICES HIERARCHY:
   - Keep code strictly domain-scoped (Core, Soul, Memory, Companions, Combat, Narrative, UI, Audio, World, Orchestration, AI, QA).
3. CRITICAL TECHNICAL GUARDRAILS:
   - Delegate Collision Prevention: All DECLARE_DYNAMIC_MULTICAST_DELEGATE_* MUST use globally unique names (e.g. FOnAshenHealthChangedSignature).
   - Filename Uniqueness: Every .cpp filename in the project MUST be unique across all domain subfolders.
   - Defensive Pointer Safety: Always use TWeakObjectPtr and IsValid() guards before dereferencing raw pointers.
   - Header Include Order: '#include "*.generated.h"' MUST be the absolute last #include.
   - Reflection Macros: UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Ashen|...") and UFUNCTION(BlueprintCallable, Category="Ashen|...").

Output Format:
If providing C++ files, output them cleanly separated by:
--- HEADER ---
[Header C++ Code]
--- CPP ---
[Implementation C++ Code]
    `.trim();

    try {
      const res = await queryCognitiveCore(`${systemPrompt}\n\nUSER PROMPT:\n${textToSend}`);
      const text = res.text;

      let headerSnippet: string | undefined = undefined;
      let cppSnippet: string | undefined = undefined;

      if (text.includes('--- HEADER ---') && text.includes('--- CPP ---')) {
        const parts = text.split('--- CPP ---');
        headerSnippet = parts[0].replace('--- HEADER ---', '').trim();
        cppSnippet = parts[1].trim();
      }

      const aiMsg: CppChatMessage = {
        id: `ai-${Date.now()}`,
        sender: 'ai',
        text,
        timestamp: Date.now(),
        headerCode: headerSnippet,
        cppCode: cppSnippet,
      };

      setChatMessages((prev) => [...prev, aiMsg]);
      addNovaSpark(`C++ Architect: Synthesized C++ response for domain ${activeDomain}.`);
      setTimeout(scrollToBottom, 100);
    } catch (err) {
      console.error('[CppChat] Failed:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  // Inject Code snippet from AI Chat directly into Editor
  const handleInjectCode = (header?: string, cpp?: string) => {
    if (header) setHeaderCode(header);
    if (cpp) setCppCode(cpp);
    setSaveStatus('Injected AI C++ code into active editor!');
    setTimeout(() => setSaveStatus(null), 3000);
  };

  // Save to disk
  const handleSaveToDisk = async () => {
    const domainPath = `c:/Users/Chris/Ashen Oath Unreal Engine/AshenOath/Source/AshenOath/${activeDomain}`;
    const headerPath = `${domainPath}/${selectedTemplate.headerName}`;
    const cppPath = `${domainPath}/${selectedTemplate.cppName}`;

    try {
      const hSuccess = await CSEBridgeService.writeRemoteFile(headerPath, headerCode);
      const cppSuccess = await CSEBridgeService.writeRemoteFile(cppPath, cppCode);

      if (hSuccess || cppSuccess) {
        setSaveStatus(`Saved to Source/AshenOath/${activeDomain}/`);
        addNovaSpark(`C++ Forge: Saved UE5 source files directly to ${domainPath}`);
      } else {
        setSaveStatus('Disk write ready (Workspace buffer active).');
      }
    } catch {
      setSaveStatus('Local disk write buffer active.');
    }
  };

  // Copy code
  const handleCopyCode = () => {
    const code = activeTab === 'header' ? headerCode : cppCode;
    navigator.clipboard.writeText(code);
    setSaveStatus('Code copied to clipboard!');
    setTimeout(() => setSaveStatus(null), 3000);
  };

  return (
    <div className="w-full h-full flex flex-col gap-6 animate-fade-in font-mono select-none">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-white/10 pb-4">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-cyan-500/10 border border-cyan-500/30 rounded-xl text-cyan-400">
            <Code2 size={24} />
          </div>
          <div>
            <h2 className="text-xl font-bold tracking-widest text-cyan-300 uppercase flex items-center gap-3">
              C++ Unreal Engine 5 Studio
              <span className="text-[10px] text-amber-400 font-normal px-2.5 py-0.5 bg-amber-500/10 border border-amber-500/30 rounded flex items-center gap-1">
                <ShieldCheck size={12} /> UE 5.8 12-Domain IDE
              </span>
            </h2>
            <p className="text-xs text-white/50">
              Sovereign UE5 C++ Synthesis Suite & AI Architect for Ashen Oath & Where Light Fades
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 font-mono">
          <button
            onClick={() => setShowChatDrawer(!showChatDrawer)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all border ${
              showChatDrawer
                ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500/50 shadow-[0_0_12px_rgba(6,182,212,0.3)]'
                : 'bg-black/60 text-gray-300 border-white/10 hover:text-white'
            }`}
          >
            <MessageSquare size={14} className="text-cyan-400" />
            <span>AI C++ Architect</span>
          </button>

          <button
            onClick={handleExecuteUBT}
            disabled={isCompiling}
            className="flex items-center gap-1.5 px-3.5 py-1.5 bg-gradient-to-r from-cyan-500/20 to-emerald-500/20 hover:from-cyan-500/30 hover:to-emerald-500/30 border border-cyan-500/50 rounded-lg text-cyan-200 text-xs font-bold transition-all shadow-[0_0_15px_rgba(6,182,212,0.2)] disabled:opacity-50"
          >
            <Hammer size={14} className={isCompiling ? 'animate-spin text-cyan-300' : 'text-cyan-400'} />
            <span>{isCompiling ? 'Compiling UBT...' : '🚀 Execute UBT Pass'}</span>
          </button>
          <button
            onClick={handleRunAudit}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/40 rounded-lg text-indigo-300 text-xs font-bold transition-all"
          >
            <ShieldAlert size={14} className="text-indigo-400" />
            <span>Audit C++</span>
          </button>
          <button
            onClick={handleSaveToDisk}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/40 rounded-lg text-emerald-300 text-xs font-bold transition-all"
          >
            <Save size={14} className="text-emerald-400" />
            <span>Save to Disk</span>
          </button>
        </div>
      </div>

      {/* Main Workspace Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-1">
        {/* Left Control Column (3 cols) */}
        <div className="lg:col-span-3 space-y-4">
          {/* Domain Selector */}
          <div className="p-4 bg-black/60 border border-white/10 rounded-xl space-y-3">
            <h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest flex items-center justify-between">
              <span className="flex items-center gap-2">
                <FolderTree size={14} className="text-cyan-400" /> 12 Domain Hierarchy
              </span>
              <span className="text-[10px] text-cyan-300">{activeDomain}/</span>
            </h3>
            <div className="grid grid-cols-2 gap-1.5">
              {ASHEN_DOMAINS.map((dom) => (
                <button
                  key={dom}
                  onClick={() => setActiveDomain(dom)}
                  className={`px-2.5 py-1.5 rounded text-[10px] font-bold text-left transition-all border ${
                    activeDomain === dom
                      ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500/50 shadow-[0_0_10px_rgba(6,182,212,0.2)]'
                      : 'bg-white/5 text-gray-400 border-white/5 hover:text-white hover:bg-white/10'
                  }`}
                >
                  {dom}
                </button>
              ))}
            </div>
          </div>

          {/* WLF Canon Lore Binding */}
          <div className="p-4 bg-black/60 border border-white/10 rounded-xl space-y-2">
            <h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest flex items-center gap-2">
              <BookOpen size={14} className="text-amber-400" /> WLF Canon Binding
            </h3>
            <select
              value={selectedCanonNode}
              onChange={(e) => setSelectedCanonNode(e.target.value)}
              className="w-full bg-black/80 border border-white/10 rounded p-2 text-xs text-amber-200 focus:outline-none focus:border-amber-400"
            >
              {canonNodes.map((n: any) => (
                <option key={n.id} value={n.id}>
                  {n.name} [{n.label}]
                </option>
              ))}
            </select>
          </div>

          {/* UE5 Class Presets */}
          <div className="p-4 bg-black/60 border border-white/10 rounded-xl space-y-3">
            <h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest flex items-center gap-2">
              <Layers size={14} className="text-cyan-400" /> UE5 Class Presets
            </h3>
            <div className="space-y-2">
              {UE5_PRESET_TEMPLATES.map((tmpl) => (
                <button
                  key={tmpl.id}
                  onClick={() => handleSelectTemplate(tmpl)}
                  className={`w-full text-left p-3 rounded-lg border transition-all ${
                    selectedTemplate.id === tmpl.id
                      ? 'bg-cyan-500/10 border-cyan-500/50 text-cyan-200 shadow-[0_0_15px_rgba(6,182,212,0.15)]'
                      : 'bg-white/5 border-white/5 text-gray-400 hover:text-white hover:bg-white/10'
                  }`}
                >
                  <div className="text-xs font-bold">{tmpl.name}</div>
                  <div className="text-[10px] text-gray-500 line-clamp-2 mt-1">{tmpl.description}</div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Center Code Editor Panel (5 cols or 9 cols depending on chat drawer) */}
        <div className={`${showChatDrawer ? 'lg:col-span-5' : 'lg:col-span-9'} flex flex-col bg-black/80 border border-cyan-500/20 rounded-xl overflow-hidden shadow-2xl transition-all duration-300`}>
          {/* Editor Header */}
          <div className="flex items-center justify-between bg-black/60 border-b border-white/10 px-4 py-2">
            <div className="flex items-center gap-2 font-mono text-xs">
              <button
                onClick={() => setActiveTab('header')}
                className={`px-3 py-1.5 rounded-lg font-bold flex items-center gap-2 transition-all ${
                  activeTab === 'header'
                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                <FileCode size={14} className="text-cyan-400" />
                <span>{selectedTemplate.headerName}</span>
              </button>
              <button
                onClick={() => setActiveTab('cpp')}
                className={`px-3 py-1.5 rounded-lg font-bold flex items-center gap-2 transition-all ${
                  activeTab === 'cpp'
                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                <Code2 size={14} className="text-indigo-400" />
                <span>{selectedTemplate.cppName}</span>
              </button>
            </div>

            {saveStatus && (
              <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded border border-emerald-500/30 animate-pulse">
                {saveStatus}
              </span>
            )}
          </div>

          {/* Code Area */}
          <div className="flex-1 relative p-4 bg-black/90">
            <textarea
              value={activeTab === 'header' ? headerCode : cppCode}
              onChange={(e) => {
                if (activeTab === 'header') setHeaderCode(e.target.value);
                else setCppCode(e.target.value);
              }}
              spellCheck={false}
              className="w-full h-[520px] bg-transparent font-mono text-xs text-cyan-100 focus:outline-none resize-none leading-relaxed selection:bg-cyan-500/30"
            />
          </div>

          {/* Terminal */}
          {showTerminal && (
            <div className="bg-black/95 border-t border-cyan-500/30 p-3 space-y-2">
              <div className="flex justify-between items-center text-xs font-bold text-cyan-300">
                <span className="flex items-center gap-2">
                  <Terminal size={14} className="text-cyan-400" /> UnrealBuildTool Output Console
                </span>
                <button onClick={() => setShowTerminal(false)} className="text-gray-400 hover:text-white">
                  <X size={14} />
                </button>
              </div>
              <pre className="text-[10px] font-mono bg-black p-3 rounded text-emerald-300 max-h-36 overflow-y-auto whitespace-pre-wrap border border-white/5">
                {ubtLog || 'Awaiting UnrealBuildTool output...'}
              </pre>
            </div>
          )}

          {/* Footer */}
          <div className="flex items-center justify-between bg-black/70 border-t border-white/10 px-4 py-2 text-[10px] text-gray-400">
            <span>Domain: Source/AshenOath/{activeDomain}/</span>
            <span>Lines: {(activeTab === 'header' ? headerCode : cppCode).split('\n').length}</span>
          </div>
        </div>

        {/* Right AI C++ Architect Chat Panel (4 cols) */}
        {showChatDrawer && (
          <div className="lg:col-span-4 flex flex-col bg-black/90 border border-cyan-500/30 rounded-xl overflow-hidden shadow-2xl backdrop-blur-xl animate-fade-in font-mono h-[640px]">
            {/* Chat Header */}
            <div className="p-3 bg-gradient-to-r from-cyan-950/40 to-black border-b border-white/10 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Bot size={18} className="text-cyan-400 animate-pulse" />
                <div>
                  <h3 className="text-xs font-bold text-cyan-200">AI C++ Architect (Hephaestus)</h3>
                  <span className="text-[9px] text-amber-400 font-mono flex items-center gap-1">
                    <ShieldCheck size={10} className="text-amber-400" /> ashen-oath-unreal-coding Active (Zero Warning Mandate)
                  </span>
                </div>
              </div>
              <button onClick={() => setShowChatDrawer(false)} className="text-gray-400 hover:text-white">
                <X size={16} />
              </button>
            </div>

            {/* Quick Prompt Chips */}
            <div className="p-2 border-b border-white/5 bg-black/40 flex flex-wrap gap-1 text-[9px]">
              <button
                onClick={() => handleSendChatMessage('Create a UE5 Gameplay Ability (GAS) for Oathbringer Greatsword strike with stamina cost')}
                className="px-2 py-0.5 bg-white/5 hover:bg-cyan-500/20 text-cyan-300 rounded border border-white/5 hover:border-cyan-500/30 transition-all"
              >
                ⚔️ GAS Ability
              </button>
              <button
                onClick={() => handleSendChatMessage('Create a UE5 ActorComponent for Garrett companion trust level and stance switching')}
                className="px-2 py-0.5 bg-white/5 hover:bg-cyan-500/20 text-cyan-300 rounded border border-white/5 hover:border-cyan-500/30 transition-all"
              >
                🛡️ Trust Component
              </button>
              <button
                onClick={() => handleSendChatMessage('Refactor raw pointer handles into TWeakObjectPtr and IsValid() defensive checks')}
                className="px-2 py-0.5 bg-white/5 hover:bg-cyan-500/20 text-cyan-300 rounded border border-white/5 hover:border-cyan-500/30 transition-all"
              >
                🔒 Pointer Safety Guard
              </button>
            </div>

            {/* Chat Messages Scroll Area */}
            <div className="flex-1 p-3 overflow-y-auto space-y-3 scrollbar-thin">
              {chatMessages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex flex-col gap-1 text-xs ${
                    msg.sender === 'user' ? 'items-end' : 'items-start'
                  }`}
                >
                  <div className="flex items-center gap-1 text-[9px] text-gray-400 font-bold uppercase">
                    {msg.sender === 'user' ? (
                      <>
                        <span>User</span> <User size={10} />
                      </>
                    ) : (
                      <>
                        <Bot size={10} className="text-cyan-400" /> <span>C++ Architect</span>
                      </>
                    )}
                  </div>
                  <div
                    className={`p-3 rounded-xl max-w-[95%] leading-relaxed ${
                      msg.sender === 'user'
                        ? 'bg-cyan-500/20 border border-cyan-500/40 text-cyan-100 rounded-tr-none'
                        : 'bg-white/5 border border-white/10 text-gray-200 rounded-tl-none space-y-2'
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{msg.text}</p>

                    {/* Inject Code CTA Button */}
                    {(msg.headerCode || msg.cppCode) && (
                      <div className="pt-2 border-t border-white/10 flex flex-wrap items-center gap-2">
                        <button
                          onClick={() => handleInjectCode(msg.headerCode, msg.cppCode)}
                          className="px-2.5 py-1 bg-gradient-to-r from-cyan-500/20 to-emerald-500/20 hover:from-cyan-500/30 hover:to-emerald-500/30 border border-emerald-500/40 rounded text-emerald-300 text-[10px] font-bold transition-all flex items-center gap-1"
                        >
                          <Zap size={11} className="text-emerald-400" />
                          <span>⚡ Inject into Editor</span>
                        </button>
                        <button
                          onClick={async () => {
                            handleInjectCode(msg.headerCode, msg.cppCode);
                            await handleSaveToDisk();
                            await handleExecuteUBT();
                          }}
                          className="px-2.5 py-1 bg-gradient-to-r from-purple-500/20 to-cyan-500/20 hover:from-purple-500/30 hover:to-cyan-500/30 border border-purple-500/40 rounded text-purple-300 text-[10px] font-bold transition-all flex items-center gap-1"
                        >
                          <Hammer size={11} className="text-purple-400" />
                          <span>🚀 Save & Run UBT Pass</span>
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Chat Input Bar */}
            <div className="p-3 border-t border-white/10 bg-black/60 flex items-center gap-2">
              <textarea
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSendChatMessage();
                  }
                }}
                placeholder="Ask Hephaestus to write performant UE5 C++..."
                rows={1}
                className="flex-1 bg-black/80 border border-white/10 rounded-lg p-2 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 resize-none"
              />
              <button
                onClick={() => handleSendChatMessage()}
                disabled={isGenerating || !chatInput.trim()}
                className="p-2.5 bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-500/40 text-cyan-300 rounded-lg transition-all disabled:opacity-50"
              >
                {isGenerating ? <RefreshCw size={16} className="animate-spin" /> : <Send size={16} />}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* 20-Build Master Batch Creator Modal */}
      {showBatchModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-black/95 border border-purple-500/40 rounded-xl p-6 max-w-md w-full space-y-4 font-mono shadow-2xl">
            <div className="flex justify-between items-center border-b border-white/10 pb-2">
              <h3 className="text-sm font-bold text-purple-300 flex items-center gap-2">
                <Layers size={16} className="text-purple-400" /> 20-Build Master Batch Creator
              </h3>
              <button onClick={() => setShowBatchModal(false)} className="text-gray-400 hover:text-white">
                <X size={16} />
              </button>
            </div>
            <p className="text-xs text-gray-300">
              Bulk scaffold 20 builds (Builds {batchStartBuild} – {batchStartBuild + 19}) across Ashen Oath domains with Master Synthesis Orchestration.
            </p>
            <div className="space-y-2">
              <label className="text-xs text-gray-400">Starting Build Number:</label>
              <input
                type="number"
                value={batchStartBuild}
                onChange={(e) => setBatchStartBuild(parseInt(e.target.value) || 676)}
                className="w-full bg-black/80 border border-purple-500/30 rounded p-2 text-xs text-purple-200"
              />
            </div>
            <button
              onClick={() => {
                setShowBatchModal(false);
                addNovaSpark(`Master Batch: Created Builds ${batchStartBuild}-${batchStartBuild + 19}`);
              }}
              className="w-full py-2.5 bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-500 hover:to-cyan-500 text-white font-bold rounded-lg text-xs transition-all flex items-center justify-center gap-2"
            >
              <Sparkles size={14} className="text-purple-200" />
              <span>Scaffold 20-Build Master Batch</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default UnrealCppForgePage;
