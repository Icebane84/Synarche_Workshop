// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#include "UI/UResonanceDashboard.h"
#include "UI/UResonanceStateVectorWidget.h"
#include "UI/UResonanceQuestBoardWidget.h"
#include "UI/UResonanceProtocolMonitorWidget.h"
#include "UI/UDissonanceQuestDetailWidget.h"
#include "UI/UResonanceSynergyMapWidget.h"
#include "Core/CSESubsystem.h" // Include the CSE Subsystem
#include "Kismet/GameplayStatics.h" // For GetGameInstance

void UResonanceDashboard::NativeConstruct()
{
	Super::NativeConstruct();

	// Get the CSE Subsystem and subscribe to its delegates
	if (UGameInstance* GameInstance = UGameplayStatics::GetGameInstance(this))
	{
		UCSESubsystem* CSESubsystem = GameInstance->GetSubsystem<UCSESubsystem>();
		if (CSESubsystem)
		{
			CSESubsystem->OnKPIValuesUpdated.AddDynamic(this, &UResonanceDashboard::OnCSEKPIValuesUpdated);
			CSESubsystem->OnDissonanceQuestsUpdated.AddDynamic(this, &UResonanceDashboard::OnCSEDissonanceQuestsUpdated);

			// Request initial data immediately after subscribing
			CSESubsystem->OnKPIValuesUpdated.Broadcast(CSESubsystem->CurrentCoherenceIndex, CSESubsystem->CurrentSynergyFlowRate, CSESubsystem->CurrentCognitiveLoad);
			CSESubsystem->OnDissonanceQuestsUpdated.Broadcast(CSESubsystem->CurrentDissonanceQuests);
		}
	}

	if (DissonanceQuestBoard)
	{
		DissonanceQuestBoard->OnQuestSelected.AddDynamic(this, &UResonanceDashboard::OnQuestSelected);
		}
	}
}

void UResonanceDashboard::NativeDestruct()
{
	// Unsubscribe from delegates to prevent memory leaks
	if (UGameInstance* GameInstance = UGameplayStatics::GetGameInstance(this))
	{
		if (UCSESubsystem* CSESubsystem = GameInstance->GetSubsystem<UCSESubsystem>())
		{
			CSESubsystem->OnKPIValuesUpdated.RemoveDynamic(this, &UResonanceDashboard::OnCSEKPIValuesUpdated);
			CSESubsystem->OnDissonanceQuestsUpdated.RemoveDynamic(this, &UResonanceDashboard::OnCSEDissonanceQuestsUpdated);
		}
	}
	Super::NativeDestruct();
}

void UResonanceDashboard::OnCSEKPIValuesUpdated(float CoherenceIndex, float SynergyFlowRate, float CognitiveLoad)
{
	if (StateVectorDisplay)
	{
		StateVectorDisplay->UpdateKPIValues(CoherenceIndex, SynergyFlowRate, CognitiveLoad);
	}
}

void UResonanceDashboard::OnCSEDissonanceQuestsUpdated(const TArray<FDissonanceQuest>& DissonanceQuests)
{
	if (DissonanceQuestBoard)
	{
		DissonanceQuestBoard->PopulateQuestList(DissonanceQuests);
	}
}

void UResonanceDashboard::OnQuestSelected(const FDissonanceQuest& QuestData)
{
	// Here you would create and show your Quest Detail Widget.
	// This logic depends on how you manage widgets (e.g., adding to viewport,
	// setting visibility on a pre-existing widget).

	// Example:
	// if (QuestDetailWidget) // Assuming you have a UPROPERTY for it
	// {
	//     QuestDetailWidget->SetQuestDetails(QuestData);
	//     QuestDetailWidget->SetVisibility(ESlateVisibility::Visible);
	// }
}
