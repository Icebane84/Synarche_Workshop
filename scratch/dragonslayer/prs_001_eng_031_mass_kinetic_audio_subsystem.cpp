// System Identifier: PRS-001-ENG-031
// File: MassKineticAudioSubsystem.cpp (Includes Header & Implementation)

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "Kismet/GameplayStatics.h"
#include "Components/AudioComponent.h"
#include "AudioParameter.h"
#include "MassKineticAudioSubsystem.generated.h"

class USoundBase;

// ============================================================================
// HEADER DECLARATION
// ============================================================================

UCLASS()
class BERSERKGAME_API UMassKineticAudioSubsystem : public UWorldSubsystem
{
    GENERATED_BODY()

public:
    UMassKineticAudioSubsystem();

    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    UFUNCTION(BlueprintCallable, Category = "Mass Kinetic Cleave | Audio")
    void PlayProceduralCleaveAudio(const FVector& ImpactLocation, float KineticEnergyJoules, float MaterialHardnessScale = 1.0f);

private:
    UPROPERTY()
    USoundBase* MasterCleaveMetaSoundAsset;

    const float ReferenceMaxEnergy = 25000.0f;
    const float BaseMinPitch = 0.65f;
    const float BaseMaxPitch = 1.15f;
};

// ============================================================================
// SOURCE IMPLEMENTATION
// ============================================================================

UMassKineticAudioSubsystem::UMassKineticAudioSubsystem()
{
    static ConstructorHelpers::FObjectFinder<USoundBase> MetaSoundAssetObj(TEXT("/Game/Audio/MetaSounds/MS_MassKinetic_Impact.MS_MassKinetic_Impact"));
    if (MetaSoundAssetObj.Succeeded())
    {
        MasterCleaveMetaSoundAsset = MetaSoundAssetObj.Object;
    }
}

void UMassKineticAudioSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
}

void UMassKineticAudioSubsystem::Deinitialize()
{
    Super::Deinitialize();
}

void UMassKineticAudioSubsystem::PlayProceduralCleaveAudio(const FVector& ImpactLocation, float KineticEnergyJoules, float MaterialHardnessScale)
{
    UWorld* World = GetWorld();
    if (!World || !MasterCleaveMetaSoundAsset) return;

    float EnergyRatio = FMath::Clamp(KineticEnergyJoules / ReferenceMaxEnergy, 0.0f, 1.0f);
    float TargetPitch = FMath::Lerp(BaseMaxPitch, BaseMinPitch, FMath::Sqrt(EnergyRatio));

    float TransientCrunchVolume = FMath::Pow(EnergyRatio, 2.0f); 
    float SubBassIntensity = FMath::Clamp((KineticEnergyJoules - 5000.0f) / (ReferenceMaxEnergy - 5000.0f), 0.0f, 1.0f);
    float SpatialRadiusOverride = FMath::Lerp(1200.0f, 5000.0f, EnergyRatio * (MaterialHardnessScale / 5.0f));

    UAudioComponent* AudioComp = UGameplayStatics::SpawnSoundAtLocation(
        World, 
        MasterCleaveMetaSoundAsset, 
        ImpactLocation, 
        FRotator::ZeroRotator, 
        1.0f,
        TargetPitch, 
        0.0f,
        nullptr,
        nullptr,
        false
    );

    if (AudioComp)
    {
        TArray<FAudioParameter> MetaSoundParameters;
        
        MetaSoundParameters.Add(FAudioParameter(FName("KineticEnergy"), KineticEnergyJoules));
        MetaSoundParameters.Add(FAudioParameter(FName("EnergyRatio"), EnergyRatio));
        MetaSoundParameters.Add(FAudioParameter(FName("TransientCrunchMix"), TransientCrunchVolume));
        MetaSoundParameters.Add(FAudioParameter(FName("SubBassIntensity"), SubBassIntensity));
        MetaSoundParameters.Add(FAudioParameter(FName("MaterialHardness"), MaterialHardnessScale));
        MetaSoundParameters.Add(FAudioParameter(FName("DynamicAttenuationRadius"), SpatialRadiusOverride));

        AudioComp->SetParameters(MetaSoundParameters);
        AudioComp->Play();
    }
}