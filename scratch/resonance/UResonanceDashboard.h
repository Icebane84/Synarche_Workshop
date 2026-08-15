// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "UResonanceDashboard.generated.h"

// Forward declare the CSE Subsystem
class UDissonanceQuestDetailWidget;
// Forward declarations for the sub-widgets
class UResonanceStateVectorWidget;
class UResonanceQuestBoardWidget;
class UResonanceProtocolMonitorWidget;
class UResonanceSynergyMapWidget;

/**
 * @brief Main container widget for the Resonance Dashboard.
 * Main container widget for the Resonance Dashboard.
 * Orchestrates and displays all sub-components of the AI's cognitive state.
 */
UCLASS()
class ASHENOATH_API UResonanceDashboard : public UUserWidget
{
	GENERATED_BODY()

public:
	// UPROPERTY bindings for the sub-widgets, to be linked in the UMG designer.
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UResonanceStateVectorWidget* StateVectorDisplay;
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UResonanceQuestBoardWidget* DissonanceQuestBoard;
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UResonanceProtocolMonitorWidget* ActiveProtocolMonitor;
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UResonanceSynergyMapWidget* SynergyMap;

protected:
	/**
	 * @brief Called when the widget is constructed.
	 * @details Subscribes to CSE Subsystem delegates for real-time updates.
	 */
	virtual void NativeConstruct() override;

	/**
	 * @brief Called when the widget is removed from the viewport.
	 * @details Unsubscribes from CSE Subsystem delegates to prevent memory leaks.
	 */
	virtual void NativeDestruct() override;

	/**
	 * @brief Callback for KPI updates from the CSE Subsystem.
	 */
	UFUNCTION()
	void OnCSEKPIValuesUpdated(float CoherenceIndex, float SynergyFlowRate, float CognitiveLoad);

	UFUNCTION()
	void OnCSEDissonanceQuestsUpdated(const TArray<FDissonanceQuest>& DissonanceQuests);

	// Handler for when a quest is selected in the board.
	UFUNCTION()
	void OnQuestSelected(const FDissonanceQuest& QuestData);
};
