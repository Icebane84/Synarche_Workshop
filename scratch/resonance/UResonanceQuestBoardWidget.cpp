// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#include "UI/UResonanceQuestBoardWidget.h"
#include "UI/UDissonanceQuestEntryWidget.h"
#include "UI/UDissonanceQuestItem.h" // Include our quest item wrapper

void UResonanceQuestBoardWidget::NativeConstruct()
{
	Super::NativeConstruct();

	if (QuestListView)
	{
		// This is a Blueprint event, so we bind to it dynamically.
		QuestListView->OnItemClicked().AddUObject(this, &UResonanceQuestBoardWidget::HandleQuestEntryClicked);
	}
}

void UResonanceQuestBoardWidget::PopulateQuestList(const TArray<FDissonanceQuest>& DissonanceQuests)
{
	if (!QuestListView)
	{
		UE_LOG(LogTemp, Warning, TEXT("QuestListView is not bound in UResonanceQuestBoardWidget!"));
		return;
	}

	QuestListView->ClearListItems();
	for (const FDissonanceQuest& Quest : DissonanceQuests)
	{
		UDissonanceQuestItem* QuestItem = NewObject<UDissonanceQuestItem>(this);
		QuestItem->QuestData = Quest;
		QuestListView->AddItem(QuestItem);
	}
}

void UResonanceQuestBoardWidget::HandleQuestEntryClicked(const FDissonanceQuest& QuestData)
{
	// Re-broadcast the event for the main dashboard to hear.
	OnQuestSelected.Broadcast(QuestData);
}
