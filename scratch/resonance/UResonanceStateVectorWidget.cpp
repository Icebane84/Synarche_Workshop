// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#include "UI/UResonanceStateVectorWidget.h"
#include "Internationalization/Text.h" // Required for FText::Format

void UResonanceStateVectorWidget::NativeConstruct()
{
	Super::NativeConstruct();
}

void UResonanceStateVectorWidget::UpdateKPIValues(float CoherenceIndex, float SynergyFlowRate, float CognitiveLoad)
{
    if (Text_CoherenceIndex)
    {
        Text_CoherenceIndex->SetText(FText::Format(NSLOCTEXT("ResonanceDashboard", "CoherenceIndexFormat", "Coherence Index: {0:.2f}"), CoherenceIndex));
    }
    if (Text_SynergyFlowRate)
    {
        Text_SynergyFlowRate->SetText(FText::Format(NSLOCTEXT("ResonanceDashboard", "SynergyFlowRateFormat", "Synergy Flow Rate: {0:.2f}"), SynergyFlowRate));
    }
    if (ProgressBar_CognitiveLoad)
    {
        ProgressBar_CognitiveLoad->SetPercent(CognitiveLoad);
    }
}
