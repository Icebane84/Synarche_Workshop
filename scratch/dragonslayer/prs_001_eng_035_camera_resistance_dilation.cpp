// System Identifier: PRS-001-ENG-035
// File: CameraResistanceDilationComponent.cpp (Includes Header & Implementation)

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "GameFramework/Character.h"
#include "Camera/CameraComponent.h"
#include "WeaponResistanceWarper.h"
#include "CameraResistanceDilationComponent.generated.h"

// ============================================================================
// HEADER DECLARATION
// ============================================================================

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class BERSERKGAME_API UCameraResistanceDilationComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UCameraResistanceDilationComponent();

protected:
    virtual void BeginPlay() override;

public:
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

private:
    void ExecuteFovModulation(float DeltaTime);

    UPROPERTY(EditAnywhere, Category = "FOV Config | Limits")
    float BaselineFov = 90.0f;

    UPROPERTY(EditAnywhere, Category = "FOV Config | Limits")
    float MaximumCompressionFov = 76.0f;

    UPROPERTY(EditAnywhere, Category = "FOV Config | Limits")
    float ElasticExpansionOvershoot = 6.0f;

    UPROPERTY(EditAnywhere, Category = "FOV Config | Dynamics")
    float CompressionInterpSpeed = 18.0f;

    UPROPERTY(EditAnywhere, Category = "FOV Config | Dynamics")
    float RecoveryInterpSpeed = 8.0f;

    float TargetFov = 90.0f;
    float CurrentFov = 90.0f;
    bool bWasResistingLastFrame = false;

    UPROPERTY()
    ACharacter* OwnerCharacter;

    UPROPERTY()
    UCameraComponent* ActiveCameraComponent;

    UPROPERTY()
    UWeaponResistanceWarper* ResistanceWarper;
};

// ============================================================================
// SOURCE IMPLEMENTATION
// ============================================================================

UCameraResistanceDilationComponent::UCameraResistanceDilationComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
    PrimaryComponentTick.bStartWithTickEnabled = true;
}

void UCameraResistanceDilationComponent::BeginPlay()
{
    Super::BeginPlay();

    OwnerCharacter = Cast<ACharacter>(GetOwner());
    if (OwnerCharacter)
    {
        ActiveCameraComponent = OwnerCharacter->FindComponentByClass<UCameraComponent>();
        ResistanceWarper = OwnerCharacter->FindComponentByClass<UWeaponResistanceWarper>();
    }

    CurrentFov = BaselineFov;
    TargetFov = BaselineFov;
}

void UCameraResistanceDilationComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    if (!ActiveCameraComponent || !ResistanceWarper) return;

    ExecuteFovModulation(DeltaTime);
}

void UCameraResistanceDilationComponent::ExecuteFovModulation(float DeltaTime)
{
    float DirectModifier = ResistanceWarper->GetCurrentPlayRateModifier();
    bool bIsResisting = (DirectModifier < 0.95f);

    if (bIsResisting)
    {
        float CompressionRatio = 1.0f - DirectModifier; 
        TargetFov = FMath::Lerp(BaselineFov, MaximumCompressionFov, FMath::Sqrt(CompressionRatio));
        bWasResistingLastFrame = true;
    }
    else
    {
        if (bWasResistingLastFrame)
        {
            CurrentFov = BaselineFov + ElasticExpansionOvershoot;
            TargetFov = BaselineFov;
            bWasResistingLastFrame = false;
        }
        else
        {
            TargetFov = BaselineFov;
        }
    }

    float ActiveInterpSpeed = bIsResisting ? CompressionInterpSpeed : RecoveryInterpSpeed;
    CurrentFov = FMath::FInterpTo(CurrentFov, TargetFov, DeltaTime, ActiveInterpSpeed);

    ActiveCameraComponent->SetFieldOfView(CurrentFov);
}