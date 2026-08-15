// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "Components/ListView.h" // Required for UListView
#include "DissonanceTypes.h" // Include FDissonanceQuest
#include "UResonanceQuestBoardWidget.generated.h"

/**
 * Widget for "The Dissonance Quest Board (The 'Mission Log')".
 * Displays a list of active Dissonance Quests for the user to review and prioritize.
 */
UCLASS()
class ASHENOATH_API UResonanceQuestBoardWidget : public UUserWidget
{
	GENERATED_BODY()

public:
	// A new dispatcher for the board itself, to pass the click event up to the main dashboard.
	UPROPERTY(BlueprintAssignable, Category = "Dissonance Quest")
	FOnQuestEntryClicked OnQuestSelected;

protected:
	virtual void NativeConstruct() override;

public:
	// UPROPERTY binding for the ListView that will display the quests
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UListView* QuestListView;

	/**
	 * Populates the QuestListView with a given array of Dissonance Quests.
	 * @param DissonanceQuests The array of quests to display.
	 */
	UFUNCTION(BlueprintCallable, Category = "Resonance Dashboard|Dissonance Quests")
	void PopulateQuestList(const TArray<FDissonanceQuest>& DissonanceQuests);

	UFUNCTION()
	void HandleQuestEntryClicked(const FDissonanceQuest& QuestData);
};
