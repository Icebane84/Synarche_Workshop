// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#include "Core/CSESubsystem.h"

void UCSESubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
	Super::Initialize(Collection);
	// Any initial setup for the CSE Subsystem can go here.
	// For example, if it needs to connect to a backend service.
}

void UCSESubsystem::Deinitialize()
{
	// Clean up any resources here.
	Super::Deinitialize();
}

void UCSESubsystem::SetKPIValues(float NewCoherenceIndex, float NewSynergyFlowRate, float NewCognitiveLoad)
{
	CurrentCoherenceIndex = NewCoherenceIndex;
	CurrentSynergyFlowRate = NewSynergyFlowRate;
	CurrentCognitiveLoad = NewCognitiveLoad;
	OnKPIValuesUpdated.Broadcast(CurrentCoherenceIndex, CurrentSynergyFlowRate, CurrentCognitiveLoad);
}

void UCSESubsystem::SetDissonanceQuests(const TArray<FDissonanceQuest>& NewDissonanceQuests)
{
	CurrentDissonanceQuests = NewDissonanceQuests;
	OnDissonanceQuestsUpdated.Broadcast(CurrentDissonanceQuests);
}
