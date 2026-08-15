// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "DissonanceTypes.h" // For FDissonanceQuest
#include "CSESubsystem.generated.h"

// Declare delegates for KPI and Dissonance Quest updates
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnKPIValuesUpdated, float, CoherenceIndex, float, SynergyFlowRate, float, CognitiveLoad);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnDissonanceQuestsUpdated, const TArray<FDissonanceQuest>&, DissonanceQuests);

/**
 * UCSESubsystem
 * Game Instance Subsystem to provide telemetry and data from the Coherent Synthesis Engine (CSE)
 * to UI components like the Resonance Dashboard.
 */
UCLASS()
class ASHENOATH_API UCSESubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	// Begin USubsystem
	virtual void Initialize(FSubsystemCollectionBase& Collection) override;
	virtual void Deinitialize() override;
	// End USubsystem

	// Delegates for broadcasting updates
	UPROPERTY(BlueprintAssignable, Category = "CSE Telemetry")
	FOnKPIValuesUpdated OnKPIValuesUpdated;

	UPROPERTY(BlueprintAssignable, Category = "CSE Telemetry")
	FOnDissonanceQuestsUpdated OnDissonanceQuestsUpdated;

	/**
	 * Function to be called by the actual CSE logic (e.g., from a CSE Manager Actor or a background thread)
	 * to push new KPI values. This will then broadcast via the delegate.
	 */
	UFUNCTION(BlueprintCallable, Category = "CSE Telemetry")
	void SetKPIValues(float NewCoherenceIndex, float NewSynergyFlowRate, float NewCognitiveLoad);

	/**
	 * Function to be called by the actual CSE logic to push updated Dissonance Quests.
	 * This will then broadcast via the delegate.
	 */
	UFUNCTION(BlueprintCallable, Category = "CSE Telemetry")
	void SetDissonanceQuests(const TArray<FDissonanceQuest>& NewDissonanceQuests);

protected:
	// Internal storage for current values (optional, but good for initial setup)
	float CurrentCoherenceIndex = 0.0f;
	float CurrentSynergyFlowRate = 0.0f;
	float CurrentCognitiveLoad = 0.0f;
	TArray<FDissonanceQuest> CurrentDissonanceQuests;
};
