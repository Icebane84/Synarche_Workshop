// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "DissonanceTypes.h" // Include our FDissonanceQuest struct
#include "UDissonanceQuestItem.generated.h"

/**
 * UDissonanceQuestItem
 * UObject wrapper for FDissonanceQuest, allowing it to be used as an item in a UListView.
 */
UCLASS(BlueprintType)
class ASHENOATH_API UDissonanceQuestItem : public UObject
{
	GENERATED_BODY()

public:
	// The actual Dissonance Quest data
	UPROPERTY(BlueprintReadOnly, Category = "Dissonance Quest")
	FDissonanceQuest QuestData;
	
};