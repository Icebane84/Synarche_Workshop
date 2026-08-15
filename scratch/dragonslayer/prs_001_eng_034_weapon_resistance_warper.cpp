// System Identifier: PRS-001-ENG-034
// File: WeaponResistanceWarper.cpp (Includes Header & Implementation)

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "GameFramework/Character.h"
#include "Animation/AnimInstance.h"
#include "GeometryCollection/GeometryCollectionComponent.h"
#include "WeaponResistanceWarper.generated.h"

class UAnimMontage;

// ============================================================================
// HEADER DECLARATION
// ============================================================================

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class BERSERKGAME_API UWeaponResistanceWarper : public UActorComponent
{
    GENERATED_BODY()

public:
    UWeaponResistanceWarper();

protected:
    virtual void BeginPlay() override;

public:
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    UFUNCTION(BlueprintCallable, Category = "Mass Kinetic Cleave | Animation Warping")
    void RegisterStructuralIntersection(UGeometryCollectionComponent* GeometryComp);

    UFUNCTION(BlueprintCallable, Category = "Mass Kinetic Cleave | Animation Warping")
    void ResetResistanceMetrics();

    UFUNCTION(BlueprintPure, Category = "Mass Kinetic Cleave | Animation Warping")
    FORCEINLINE float GetCurrentPlayRateModifier() const { return CurrentPlayRateModifier; }

private:
    void ProcessAnimationWarp(float DeltaTime);

    UPROPERTY(EditAnywhere, Category = "Resistance Config")
    float BaseResistanceThresholdVolume = 50000.0f;

    UPROPERTY(EditAnywhere, Category = "Resistance Config")
    float MaxSaturationVolume = 500000.0f;

    UPROPERTY(EditAnywhere, Category = "Resistance Config")
    float MinimumPlaybackSpeedFloor = 0.08f;

    UPROPERTY(EditAnywhere, Category = "Resistance Config")
    float PlayRateRecoveryRate = 4.0f;

    float AccumulatedVolumeCurrentFrame = 0.0f;
    float TargetPlayRateModifier = 1.0f;
    float CurrentPlayRateModifier = 1.0f;

    UPROPERTY()
    ACharacter* OwnerCharacter;
};

// ============================================================================
// SOURCE IMPLEMENTATION
// ============================================================================

UWeaponResistanceWarper::UWeaponResistanceWarper()
{
    PrimaryComponentTick.bCanEverTick = true;
    PrimaryComponentTick.bStartWithTickEnabled = true;
}

void UWeaponResistanceWarper::BeginPlay()
{
    Super::BeginPlay();
    OwnerCharacter = Cast<ACharacter>(GetOwner());
}

void UWeaponResistanceWarper::RegisterStructuralIntersection(UGeometryCollectionComponent* GeometryComp)
{
    if (!GeometryComp) return;

    FBoxSphereBounds ComponentBounds = GeometryComp->GetBounds();
    FVector BoxSize = ComponentBounds.BoxExtent * 2.0f;
    
    float CalculatedVolume = BoxSize.X * BoxSize.Y * BoxSize.Z;
    AccumulatedVolumeCurrentFrame += CalculatedVolume;
}

void UWeaponResistanceWarper::ResetResistanceMetrics()
{
    AccumulatedVolumeCurrentFrame = 0.0f;
    TargetPlayRateModifier = 1.0f;
}

void UWeaponResistanceWarper::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    if (!OwnerCharacter) return;

    ProcessAnimationWarp(DeltaTime);
    AccumulatedVolumeCurrentFrame = 0.0f;
}

void UWeaponResistanceWarper::ProcessAnimationWarp(float DeltaTime)
{
    UAnimInstance* AnimInstance = OwnerCharacter->GetMesh() ? OwnerCharacter->GetMesh()->GetAnimInstance() : nullptr;
    if (!AnimInstance || !AnimInstance->IsAnyMontagePlaying()) return;

    if (AccumulatedVolumeCurrentFrame > BaseResistanceThresholdVolume)
    {
        float ExcessVolume = AccumulatedVolumeCurrentFrame - BaseResistanceThresholdVolume;
        float SaturationRatio = FMath::Clamp(ExcessVolume / (MaxSaturationVolume - BaseResistanceThresholdVolume), 0.0f, 1.0f);

        TargetPlayRateModifier = FMath::Lerp(1.0f, MinimumPlaybackSpeedFloor, FMath::Sqrt(SaturationRatio));
    }
    else
    {
        TargetPlayRateModifier = 1.0f;
    }

    float InterpSpeed = (TargetPlayRateModifier > CurrentPlayRateModifier) ? PlayRateRecoveryRate * 2.0f : PlayRateRecoveryRate;
    CurrentPlayRateModifier = FMath::FInterpTo(CurrentPlayRateModifier, TargetPlayRateModifier, DeltaTime, InterpSpeed);

    UAnimMontage* ActiveMontage = AnimInstance->GetCurrentActiveMontage();
    if (ActiveMontage)
    {
        AnimInstance->Montage_SetPlayRate(ActiveMontage, CurrentPlayRateModifier);
    }
}