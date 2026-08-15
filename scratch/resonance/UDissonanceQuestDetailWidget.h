// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "Components/TextBlock.h"
#include "Components/Button.h"
#include "DissonanceTypes.h" // Include our FDissonanceQuest struct
#include "UDissonanceQuestDetailWidget.generated.h"

/**
 * UDissonanceQuestDetailWidget
 * Widget for displaying the detailed information of a single Dissonance Quest.
 */
UCLASS()
class ASHENOATH_API UDissonanceQuestDetailWidget : public UUserWidget
{
	GENERATED_BODY()

protected:
	virtual void NativeConstruct() override;

public:
	/**
	 * Sets the data for the Dissonance Quest to be displayed in this widget.
	 * @param InQuest The FDissonanceQuest struct containing the details.
	 */
	UFUNCTION(BlueprintCallable, Category = "Dissonance Quest Details")
	void SetQuestDetails(const FDissonanceQuest& InQuest);

	// UPROPERTY bindings for displaying quest details
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UTextBlock* Text_QuestID;
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UTextBlock* Text_QuestName;
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UTextBlock* Text_QuestType;
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UTextBlock* Text_Description;
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UTextBlock* Text_Confidence;
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UTextBlock* Text_ImpactPrediction;
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UTextBlock* Text_ProposedResolution;

	// Action buttons
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UButton* Button_Approve;
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UButton* Button_Prioritize;
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UButton* Button_Close;
};
