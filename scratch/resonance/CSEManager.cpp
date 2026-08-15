// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#include "Core/CSEManager.h"
#include "Core/CSESubsystem.h"
#include "Kismet/GameplayStatics.h"

ACSEManager::ACSEManager()
{
	PrimaryActorTick.bCanEverTick = false; // We will use a timer instead of the main tick
}

void ACSEManager::BeginPlay()
{
	Super::BeginPlay();

	// Get and cache the CSE Subsystem
	if (UGameInstance* GameInstance = UGameplayStatics::GetGameInstance(this))
	{
		CSESubsystem = GameInstance->GetSubsystem<UCSESubsystem>();
	}

	// Start a repeating timer to run our simulation every 2 seconds
	GetWorldTimerManager().SetTimer(SimulationTimerHandle, this, &ACSEManager::RunCSESimulationTick, 2.0f, true, 1.0f);
}

void ACSEManager::RunCSESimulationTick()
{
	if (!CSESubsystem)
	{
		return;
	}

	// --- 1. Simulate KPI Updates ---
	// In a real system, these values would be the result of complex calculations.
	// Here, we'll just generate some random-ish data.
	float NewCoherenceIndex = FMath::FRandRange(0.85f, 0.99f);
	float NewSynergyFlowRate = FMath::FRandRange(120.0f, 350.0f);
	float NewCognitiveLoad = FMath::FRandRange(0.1f, 0.4f);

	// Push the new KPI values to the subsystem, which will broadcast them to the UI.
	CSESubsystem->SetKPIValues(NewCoherenceIndex, NewSynergyFlowRate, NewCognitiveLoad);


	// --- 2. Simulate Dissonance Quest Updates ---
	// Create a new dummy Dissonance Quest
	TArray<FDissonanceQuest> Quests;
	FDissonanceQuest NewQuest;
	NewQuest.ID = FName(*FString::Printf(TEXT("DQ_%d"), FMath::RandRange(1000, 9999)));
	NewQuest.QuestName = FText::FromString("Resolve Inconsistent Documentation");
	NewQuest.Type = EDissonanceType::ConceptualInconsistency;
	NewQuest.Description = FText::FromString("The definition for 'Synergy Flow Rate' in UMB-CSE-001 contradicts the implementation in the Resonance Dashboard. The blueprint specifies a value range of 0-1, but the implementation uses a 0-500 scale.");
	NewQuest.Confidence = FMath::FRandRange(0.7f, 0.95f);
	NewQuest.ImpactPrediction = FText::FromString("High risk of misinterpretation during performance analysis, leading to incorrect optimization efforts.");
	NewQuest.RelevantPrinciples.Add(EEthicalPrinciple::EnsureTransparency);
	NewQuest.Status = EDissonanceQuestStatus::Detected;
	NewQuest.ProposedResolutionSummary = FText::FromString("Update UMB-CSE-001 to reflect the implemented 0-500 scale for Synergy Flow Rate and clarify the metric's units.");
	NewQuest.DetectedTimestamp = FDateTime::UtcNow();

	Quests.Add(NewQuest);

	// Push the new quest list to the subsystem.
	CSESubsystem->SetDissonanceQuests(Quests);

	UE_LOG(LogTemp, Log, TEXT("CSEManager: Pushed new telemetry data to UCSESubsystem."));
}
