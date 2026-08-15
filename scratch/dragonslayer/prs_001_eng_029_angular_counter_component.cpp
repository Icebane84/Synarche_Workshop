// System Identifier: PRS-001-ENG-029
// File: AngularCounterComponent.cpp (Includes Header & Implementation)

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "GameFramework/Actor.h"
#include "DrawDebugHelpers.h"
#include "Engine/World.h"
#include "AngularCounterComponent.generated.h"

UENUM(BlueprintType)
enum class ECounterAttackZone : uint8
{
    VerticalOverhead   UMETA(DisplayName = "Overhead Riposte"),
    HorizontalLeft     UMETA(DisplayName = "Left-to-Right Cleave"),
    HorizontalRight    UMETA(DisplayName = "Right-to-Left Cleave"),
    DiagonalUnderhand  UMETA(DisplayName = "Underhand Lift")
};

// ============================================================================
// HEADER DECLARATION
// ============================================================================

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class BERSERKGAME_API UAngularCounterComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UAngularCounterComponent();

protected:
    virtual void BeginPlay() override;

public:
    UFUNCTION(BlueprintCallable, Category = "Combat | Angular Counter")
    ECounterAttackZone CalculateCounterTrajectory(const FVector& AttackerLocation, const FVector& AttackDirection, float& OutTargetBlendAngle);

private:
    UPROPERTY(EditAnywhere, Category = "Combat Config | Debug")
    bool bShowDebugVectors = true;
};

// ============================================================================
// SOURCE IMPLEMENTATION
// ============================================================================

UAngularCounterComponent::UAngularCounterComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UAngularCounterComponent::BeginPlay()
{
    Super::BeginPlay();
}

ECounterAttackZone UAngularCounterComponent::CalculateCounterTrajectory(const FVector& AttackerLocation, const FVector& AttackDirection, float& OutTargetBlendAngle)
{
    AActor* Owner = GetOwner();
    if (!Owner)
    {
        OutTargetBlendAngle = 0.0f;
        return ECounterAttackZone::HorizontalLeft;
    }

    FVector OwnerForward = Owner->GetActorForwardVector();
    FVector OwnerRight = Owner->GetActorRightVector();
    FVector OwnerUp = Owner->GetActorUpVector();

    FVector RiposteVector = -AttackDirection;

    float ForwardProjection = FVector::DotProduct(RiposteVector, OwnerForward);
    float RightProjection = FVector::DotProduct(RiposteVector, OwnerRight);
    float UpProjection = FVector::DotProduct(RiposteVector, OwnerUp);

    float RadAngle = FMath::Atan2(UpProjection, RightProjection);
    float DegAngle = FMath::RadiansToDegrees(RadAngle);
    if (DegAngle < 0.0f)
    {
        DegAngle += 360.0f;
    }

    OutTargetBlendAngle = DegAngle;

    if (bShowDebugVectors && GetWorld())
    {
        FVector VisualOrigin = Owner->GetActorLocation() + (OwnerForward * 80.0f) + (OwnerUp * 50.0f);
        DrawDebugDirectionalArrow(GetWorld(), VisualOrigin, VisualOrigin + (RiposteVector * 100.0f), 20.0f, FColor::Orange, false, 2.0f, 0, 3.0f);
    }

    if (DegAngle >= 45.0f && DegAngle < 135.0f)
    {
        return ECounterAttackZone::VerticalOverhead;
    }
    else if (DegAngle >= 135.0f && DegAngle < 225.0f)
    {
        return ECounterAttackZone::HorizontalLeft;
    }
    else if (DegAngle >= 225.0f && DegAngle < 315.0f)
    {
        return ECounterAttackZone::DiagonalUnderhand;
    }
    
    return ECounterAttackZone::HorizontalRight;
}