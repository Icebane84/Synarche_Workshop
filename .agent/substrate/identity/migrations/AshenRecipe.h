// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.
#pragma once

#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "AshenRecipe.generated.h"

/**
 * FAshenRecipe
 *
 * Defines the structure for a single crafting recipe in a DataTable.
 */
USTRUCT(BlueprintType)
struct FAshenRecipe : public FTableRowBase
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Recipe")
	FName RequiredIngredientID;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Recipe")
	int32 RequiredQuantity = 1;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Recipe")
	int32 TargetQuickbarSlot = -1;
};
