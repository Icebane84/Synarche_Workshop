// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#include "UI/UDissonanceQuestDetailWidget.h"
#include "Internationalization/Text.h"

void UDissonanceQuestDetailWidget::NativeConstruct()
{
	Super::NativeConstruct();
	// We can bind OnClicked events for the buttons here if needed.
}

void UDissonanceQuestDetailWidget::SetQuestDetails(const FDissonanceQuest& InQuest)
{
	if (Text_QuestID)
	{
		Text_QuestID->SetText(FText::FromName(InQuest.ID));
	}
	if (Text_QuestName)
	{
		Text_QuestName->SetText(InQuest.QuestName);
	}
	if (Text_QuestType)
	{
		// Using UEnum::GetDisplayValueAsText to get the user-friendly name from the enum's UMETA
		Text_QuestType->SetText(UEnum::GetDisplayValueAsText(InQuest.Type));
	}
	if (Text_Description)
	{
		Text_Description->SetText(InQuest.Description);
	}
	if (Text_Confidence)
	{
		// Formatting the float as a percentage
		FText ConfidenceText = FText::Format(
			NSLOCTEXT("ResonanceDashboard", "ConfidenceFormat", "{0}% Confidence"),
			FText::AsNumber(FMath::RoundToInt(InQuest.Confidence * 100.0f))
		);
		Text_Confidence->SetText(ConfidenceText);
	}
	if (Text_ImpactPrediction)
	{
		Text_ImpactPrediction->SetText(InQuest.ImpactPrediction);
	}
	if (Text_ProposedResolution)
	{
		Text_ProposedResolution->SetText(InQuest.ProposedResolutionSummary);
	}

	// In a real implementation, you would also populate fields for:
	// - SourceLogs
	// - RelevantPrinciples
	// - DetectedTimestamp
	// etc.
}
