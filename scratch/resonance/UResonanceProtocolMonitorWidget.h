// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "UResonanceProtocolMonitorWidget.generated.h"

/**
 * Widget for "The Active Protocol Monitor (The 'Cognitive Trace')".
 * Shows the currently executing AOP or GUCA command for transparency.
 */
UCLASS()
class ASHENOATH_API UResonanceProtocolMonitorWidget : public UUserWidget
{
	GENERATED_BODY()

protected:
	virtual void NativeConstruct() override;

};
