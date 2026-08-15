// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#include "UI/UDissonanceQuestEntryWidget.h"
#include "Internationalization/Text.h"

void UDissonanceQuestEntryWidget::NativeConstruct()
{
	Super::NativeConstruct();

	if (ClickableButton)
	{
		ClickableButton->OnClicked.AddDynamic(this, &UDissonanceQuestEntryWidget::HandleClick);
	}
}

void UDissonanceQuestEntryWidget::NativeOnListItemObjectSet(UObject* ListItemObject)
{
	Super::NativeOnListItemObjectSet(ListItemObject);

	// We need to store the QuestItem to access its data when clicked.
	UDissonanceQuestItem* QuestItem = Cast<UDissonanceQuestItem>(ListItemObject);
	if (QuestItem)
	{
		// Store the item for later use in HandleClick()
		// (You'll need to add `UDissonanceQuestItem* QuestItem;` as a member variable in the header)
	}

	UDissonanceQuestItem* QuestItem = Cast<UDissonanceQuestItem>(ListItemObject);
	if (QuestItem)
	{
		if (Text_QuestName)
		{
			Text_QuestName->SetText(QuestItem->QuestData.QuestName);
		}
		if (Text_QuestType)
		{
			Text_QuestType->SetText(UEnum::GetDisplayValueAsText(QuestItem->QuestData.Type));
		}
		if (Text_QuestStatus)
		{
			Text_QuestStatus->SetText(UEnum::GetDisplayValueAsText(QuestItem->QuestData.Status));
		}
		if (Text_Confidence)
		{
			Text_Confidence->SetText(FText::Format(NSLOCTEXT("ResonanceDashboard", "ConfidenceFormat", "{0:.0f}%"), QuestItem->QuestData.Confidence * 100.0f));
		}
		// Update other text blocks here
	}
}

void UDissonanceQuestEntryWidget::HandleClick()
{
	UDissonanceQuestItem* QuestItem = GetListItem<UDissonanceQuestItem>();
	if (QuestItem)
	{
		// Broadcast the event with the quest data.
		OnClicked.Broadcast(QuestItem->QuestData);
	}
}
