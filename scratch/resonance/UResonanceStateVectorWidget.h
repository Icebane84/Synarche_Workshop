// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "Components/TextBlock.h" // Required for UTextBlock
#include "Components/ProgressBar.h" // Required for UProgressBar
#include "UResonanceStateVectorWidget.generated.h"

/**
 * Widget for "The State Vector Display (The 'Vitals')".
 * Visualizes the core real-time KPIs of the Coherent Synthesis Engine.
 */
UCLASS()
class ASHENOATH_API UResonanceStateVectorWidget : public UUserWidget
{
	GENERATED_BODY()

protected:
	// Called when the widget is constructed.
	virtual void NativeConstruct() override;

public:
	// UPROPERTY bindings for displaying KPIs. These are linked in the UMG designer.

	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UTextBlock* Text_CoherenceIndex;

	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UTextBlock* Text_SynergyFlowRate;

	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UProgressBar* ProgressBar_CognitiveLoad;

    /**
     * Updates the displayed KPI values on the widget.
     * @param CoherenceIndex The current Coherence Index value.
     * @param SynergyFlowRate The current Synergy Flow Rate value.
     * @param CognitiveLoad The current Cognitive Load value.
     */
    UFUNCTION(BlueprintCallable, Category = "Resonance Dashboard|State Vector")
    void UpdateKPIValues(float CoherenceIndex, float SynergyFlowRate, float CognitiveLoad);
};
