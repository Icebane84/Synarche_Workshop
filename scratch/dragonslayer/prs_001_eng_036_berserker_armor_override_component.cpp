// System Identifier: PRS-001-ENG-036
// File: BerserkerArmorComponent.cpp (Includes Header & Implementation)

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "GameFramework/Character.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Kismet/KismetMathLibrary.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"
#include "BerserkerArmorComponent.generated.h"

// ============================================================================
// HEADER DECLARATION
// ============================================================================

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class BERSERKGAME_API UBerserkerArmorComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UBerserkerArmorComponent();

protected:
    virtual void BeginPlay() override;

public:
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    UFUNCTION(BlueprintCallable, Category = "Berserker Armor | Controls")
    void ActivateBerserkerState();

    UFUNCTION(BlueprintCallable, Category = "Berserker Armor | Controls")
    void DeactivateBerserkerState();

    UFUNCTION(BlueprintPure, Category = "Berserker Armor | State")
    FORCEINLINE bool IsArmorActive() const { return bIsArmorActive; }

    UFUNCTION(BlueprintPure, Category = "Berserker Armor | State")
    FORCEINLINE float GetStateDuration() const { return ActiveStateTime; }

private:
    void ProcessHealthDrain(float DeltaTime);
    void ProcessAutomatedTargetTracking(float DeltaTime);
    AActor* FindOptimalRageTarget();

    UPROPERTY(EditAnywhere, Category = "Berserker Config | Health")
    float BaseHealthDrainPerSecond = 2.0f;

    UPROPERTY(EditAnywhere, Category = "Berserker Config | Health")
    float ExponentialDrainFactor = 0.15f;

    UPROPERTY(EditAnywhere, Category = "Berserker Config | Tracking")
    float TargetAcquisitionRadius = 1200.0f;

    UPROPERTY(EditAnywhere, Category = "Berserker Config | Tracking")
    float CameraTrackingInterpSpeed = 15.0f;

    bool bIsArmorActive = false;
    float ActiveStateTime = 0.0f;
    
    UPROPERTY()
    AActor* CurrentRageTarget;

    UPROPERTY()
    ACharacter* OwnerCharacter;

    UPROPERTY()
    APlayerController* OwnerPlayerController;
};

// ============================================================================
// SOURCE IMPLEMENTATION
// ============================================================================

UBerserkerArmorComponent::UBerserkerArmorComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
    PrimaryComponentTick.bStartWithTickEnabled = true;
}

void UBerserkerArmorComponent::BeginPlay()
{
    Super::BeginPlay();

    OwnerCharacter = Cast<ACharacter>(GetOwner());
    if (OwnerCharacter)
    {
        OwnerPlayerController = Cast<APlayerController>(OwnerCharacter->GetController());
    }
}

void UBerserkerArmorComponent::ActivateBerserkerState()
{
    if (bIsArmorActive || !OwnerCharacter) return;

    bIsArmorActive = true;
    ActiveStateTime = 0.0f;
    CurrentRageTarget = nullptr;

    UCharacterMovementComponent* MoveComp = OwnerCharacter->GetCharacterMovement();
    if (MoveComp)
    {
        MoveComp->MaxWalkSpeed = 1200.0f;
        MoveComp->RotationRate = FRotator(0.0f, 1080.0f, 0.0f);
    }
}

void UBerserkerArmorComponent::DeactivateBerserkerState()
{
    if (!bIsArmorActive || !OwnerCharacter) return;

    bIsArmorActive = false;
    ActiveStateTime = 0.0f;
    CurrentRageTarget = nullptr;

    UCharacterMovementComponent* MoveComp = OwnerCharacter->GetCharacterMovement();
    if (MoveComp)
    {
        MoveComp->MaxWalkSpeed = 450.0f; 
        MoveComp->RotationRate = FRotator(0.0f, 360.0f, 0.0f);
    }
}

void UBerserkerArmorComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    if (!bIsArmorActive || !OwnerCharacter) return;

    ActiveStateTime += DeltaTime;

    ProcessHealthDrain(DeltaTime);
    ProcessAutomatedTargetTracking(DeltaTime);
}

void UBerserkerArmorComponent::ProcessHealthDrain(float DeltaTime)
{
    float AccelDrainValue = BaseHealthDrainPerSecond + FMath::Pow(ActiveStateTime * ExponentialDrainFactor, 2.0f);
    float DamageToApply = AccelDrainValue * DeltaTime;

    UGameplayStatics::ApplyDamage(OwnerCharacter, DamageToApply, OwnerPlayerController, GetOwner(), UDamageType::StaticClass());
}

void UBerserkerArmorComponent::ProcessAutomatedTargetTracking(float DeltaTime)
{
    if (!OwnerPlayerController) return;

    if (CurrentRageTarget)
    {
        float SpatialDistance = FVector::Dist(OwnerCharacter->GetActorLocation(), CurrentRageTarget->GetActorLocation());
        if (SpatialDistance > TargetAcquisitionRadius)
        {
            CurrentRageTarget = nullptr;
        }
    }

    if (!CurrentRageTarget)
    {
        CurrentRageTarget = FindOptimalRageTarget();
    }

    if (CurrentRageTarget)
    {
        FVector LookAtOrigin = CurrentRageTarget->GetActorLocation();
        FVector CameraOrigin = OwnerPlayerController->PlayerCameraManager ? OwnerPlayerController->PlayerCameraManager->GetCameraLocation() : OwnerCharacter->GetActorLocation();
        
        FRotator TargetRotation = UKismetMathLibrary::FindLookAtRotation(CameraOrigin, LookAtOrigin);
        FRotator CurrentRotation = OwnerPlayerController->GetControlRotation();

        FRotator BlendedRotation = FMath::RInterpTo(CurrentRotation, TargetRotation, DeltaTime, CameraTrackingInterpSpeed);
        OwnerPlayerController->SetControlRotation(BlendedRotation);
    }
}

AActor* UBerserkerArmorComponent::FindOptimalRageTarget()
{
    UWorld* World = GetWorld();
    if (!World) return nullptr;

    TArray<TEnumAsByte<EObjectTypeQuery>> ObjectTypes;
    ObjectTypes.Add(UEngineTypes::ConvertToObjectType(ECC_Pawn));

    TArray<AActor*> ActorsToIgnore;
    ActorsToIgnore.Add(OwnerCharacter);

    TArray<AActor*> OutActors;
    
    bool bFound = UKismetSystemLibrary::SphereOverlapActors(
        World,
        OwnerCharacter->GetActorLocation(),
        TargetAcquisitionRadius,
        ObjectTypes,
        nullptr,
        ActorsToIgnore,
        OutActors
    );

    AActor* ClosestActor = nullptr;
    float MinDistance = TargetAcquisitionRadius;

    if (bFound)
    {
        for (AActor* Actor : OutActors)
        {
            float CurrentDist = FVector::Dist(OwnerCharacter->GetActorLocation(), Actor->GetActorLocation());
            if (CurrentDist < MinDistance)
            {
                MinDistance = CurrentDist;
                ClosestActor = Actor;
            }
        }
    }

    return ClosestActor;
}