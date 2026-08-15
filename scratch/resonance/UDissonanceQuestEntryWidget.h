// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "Components/TextBlock.h"
#include "Components/Button.h"
#include "Components/Image.h"
#include "Blueprint/IUserObjectListEntry.h" // Required for list entry interface
#include "UDissonanceQuestItem.h" // Include our data item
#include "UDissonanceQuestEntryWidget.generated.h"

// Declare the Event Dispatcher signature
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnQuestEntryClicked, const FDissonanceQuest&, QuestData);

/**
 * UDissonanceQuestEntryWidget
 * Widget for a single entry in the Dissonance Quest Board's UListView.
 * Implements IUserObjectListEntry to receive the UDissonanceQuestItem.
 */
UCLASS()
class ASHENOATH_API UDissonanceQuestEntryWidget : public UUserWidget, public IUserObjectListEntry
{
	GENERATED_BODY()

public:
	// Event dispatcher that will be broadcasted when this entry is clicked.
	UPROPERTY(BlueprintAssignable, Category = "Dissonance Quest")
	FOnQuestEntryClicked OnClicked;
protected:
	virtual void NativeConstruct() override;

	// IUserObjectListEntry interface implementation
	virtual void NativeOnListItemObjectSet(UObject* ListItemObject) override;

public:
	// UPROPERTY bindings for displaying quest details
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UTextBlock* Text_QuestName;
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UTextBlock* Text_QuestType;
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UTextBlock* Text_QuestStatus;
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UTextBlock* Text_Confidence;

	// We'll make the root button of our widget clickable.
	UPROPERTY(BlueprintReadOnly, meta = (BindWidget))
	UButton* ClickableButton;

	UFUNCTION()
	void HandleClick();
	// Add more UPROPERTY for other details as needed (e.g., Description, Priority)
};
