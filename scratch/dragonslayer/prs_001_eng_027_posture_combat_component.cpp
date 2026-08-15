// System Identifier: PRS-001-ENG-027
// File: PostureCombatComponent.cpp (Includes Header & Implementation)

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"
#include "PostureCombatComponent.generated.h"

UENUM(BlueprintType)
enum class ECombatDefenseResult : uint8
{
    Deflect     UMETA(DisplayName = "Perfect Deflect"),
    Block       UMETA(DisplayName = "Standard Block"),
    Hit         UMETA(DisplayName = "Clean Hit"),
    StanceBroken UMETA(DisplayName = "Stance Broken")
};

// ============================================================================
// HEADER DECLARATION
// ============================================================================

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class BERSERKGAME_API UPostureCombatComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UPostureCombatComponent();

protected:
    virtual void BeginPlay() override;

public:
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    UFUNCTION(BlueprintCallable, Category = "Combat | Input")
    void TriggerDefenseInput();

    UFUNCTION(BlueprintCallable, Category = "Combat | Input")
    void ReleaseDefenseInput();

    UFUNCTION(BlueprintCallable, Category = "Combat | Solver")
    ECombatDefenseResult EvaluateIncomingStrike(float IncomingPostureDamage, float IncomingHealthDamage, float& OutMitigatedDamage);

    UFUNCTION(BlueprintCallable, Category = "Combat | Mechanics")
    void ModifyPosture(float Amount);

private:
    UPROPERTY(EditAnywhere, Category = "Combat Config | Windows")
    float MaxDeflectWindowSeconds = 0.12f;

    UPROPERTY(EditAnywhere, Category = "Combat Config | Windows")
    float MaxBlockWindowSeconds = 0.30f;

    UPROPERTY(EditAnywhere, Category = "Combat Config | Attributes")
    float MaxPosture = 100.0f;

    UPROPERTY(EditAnywhere, Category = "Combat Config | Attributes")
    float PostureRecoveryRate = 15.0f;

    double DefenseInputTimestamp = 0.0;
    bool bIsGuardButtonHeld = false;

    UPROPERTY(BlueprintReadOnly, Category = "Combat State", meta = (AllowPrivateAccess = "true"))
    float CurrentPosture = 0.0f;

    UPROPERTY(BlueprintReadOnly, Category = "Combat State", meta = (AllowPrivateAccess = "true"))
    bool bIsStanceBroken = false;
};

// ============================================================================
// SOURCE IMPLEMENTATION
// ============================================================================

UPostureCombatComponent::UPostureCombatComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
    PrimaryComponentTick.bStartWithTickEnabled = true;
}

void UPostureCombatComponent::BeginPlay()
{
    Super::BeginPlay();
    CurrentPosture = 0.0f;
    bIsStanceBroken = false;
}

void UPostureCombatComponent::TriggerDefenseInput()
{
    UWorld* World = GetWorld();
    if (!World || bIsStanceBroken) return;

    bIsGuardButtonHeld = true;
    DefenseInputTimestamp = World->GetRealTimeSeconds();
}

void UPostureCombatComponent::ReleaseDefenseInput()
{
    bIsGuardButtonHeld = false;
    DefenseInputTimestamp = 0.0;
}

void UPostureCombatComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    if (CurrentPosture > 0.0f && !bIsStanceBroken)
    {
        float RecoveryModifier = bIsGuardButtonHeld ? 0.2f : 1.0f;
        CurrentPosture -= PostureRecoveryRate * RecoveryModifier * DeltaTime;
        CurrentPosture = FMath::Max(CurrentPosture, 0.0f);
    }
}

ECombatDefenseResult UPostureCombatComponent::EvaluateIncomingStrike(float IncomingPostureDamage, float IncomingHealthDamage, float& OutMitigatedDamage)
{
    OutMitigatedDamage = IncomingHealthDamage;
    UWorld* World = GetWorld();

    if (!World || bIsStanceBroken || !bIsGuardButtonHeld)
    {
        return ECombatDefenseResult::Hit;
    }

    double CurrentTime = World->GetRealTimeSeconds();
    double ElapsedTimeSinceInput = CurrentTime - DefenseInputTimestamp;

    if (ElapsedTimeSinceInput <= MaxDeflectWindowSeconds)
    {
        OutMitigatedDamage = 0.0f;
        return ECombatDefenseResult::Deflect;
    }

    if (ElapsedTimeSinceInput <= MaxBlockWindowSeconds || bIsGuardButtonHeld)
    {
        OutMitigatedDamage = IncomingHealthDamage * 0.1f;
        ModifyPosture(IncomingPostureDamage);

        if (bIsStanceBroken)
        {
            return ECombatDefenseResult::StanceBroken;
        }

        return ECombatDefenseResult::Block;
    }

    return ECombatDefenseResult::Hit;
}

void UPostureCombatComponent::ModifyPosture(float Amount)
{
    if (bIsStanceBroken) return;

    CurrentPosture += Amount;
    
    if (CurrentPosture >= MaxPosture)
    {
        CurrentPosture = MaxPosture;
        bIsStanceBroken = true;
        bIsGuardButtonHeld = false;
        DefenseInputTimestamp = 0.0;
    }
}