// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "CSEManager.generated.h"

class UCSESubsystem;

/**
 * ACSEManager
 * A conceptual actor representing the core logic of the Coherent Synthesis Engine.
 * It runs a simulation/processing loop and pushes updates to the UCSESubsystem.
 */
UCLASS()
class ASHENOATH_API ACSEManager : public AActor
{
	GENERATED_BODY()

public:
	ACSEManager();

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

private:
	// A timer handle for our simulation tick
	FTimerHandle SimulationTimerHandle;

	// The function that simulates a single CSE processing step
	void RunCSESimulationTick();

	// A cached pointer to the CSE Subsystem for efficiency
	UPROPERTY()
	TObjectPtr<UCSESubsystem> CSESubsystem;
};
