// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "UResonanceSynergyMapWidget.generated.h"

/**
 * Widget for "The Synergy Map (The 'Short-Term Memory')".
 * A dynamic visualization of concepts active in the CSE's context window.
 */
UCLASS()
class ASHENOATH_API UResonanceSynergyMapWidget : public UUserWidget
{
	GENERATED_BODY()

protected:
	virtual void NativeConstruct() override;

};
