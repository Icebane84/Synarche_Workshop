// System Identifier: PRS-001-ENG-028
// File: BerserkCharacter.cpp (Includes Header & Implementation)

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "PostureCombatComponent.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/PlayerController.h"
#include "Engine/World.h"
#include "BerserkCharacter.generated.h"

class UCameraShakeBase;

// ============================================================================
// HEADER DECLARATION
// ============================================================================

UCLASS()
class BERSERKGAME_API ABerserkCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    ABerserkCharacter();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components | Combat", meta = (AllowPrivateAccess = "true"))
    UPostureCombatComponent* PostureComponent;

public:
    UFUNCTION(BlueprintCallable, Category = "Berserk | Combat Orchestration")
    void HandleIncomingAttack(AActor* Attacker, float RawPostureDamage, float RawHealthDamage, const FVector& HitLocation);

protected:
    void ExecuteDeflectEffects(const FVector& ImpactPoint);
    void ResolveAsymmetricHitStop();

private:
    UPROPERTY(EditAnywhere, Category = "Orchestration | Hit-Stop")
    float DeflectFreezeDuration = 0.06f;

    UPROPERTY(EditAnywhere, Category = "Orchestration | Hit-Stop")
    float DeflectTimeScale = 0.01f;

    UPROPERTY(EditAnywhere, Category = "Orchestration | Camera")
    TSubclassOf<UCameraShakeBase> DeflectCameraShakeClass;

    UPROPERTY(EditAnywhere, Category = "Orchestration | Camera")
    float ShakeInnerRadius = 200.0f;

    UPROPERTY(EditAnywhere, Category = "Orchestration | Camera")
    float ShakeOuterRadius = 1500.0f;

    FTimerHandle AsymmetricHitStopTimerHandle;
};

// ============================================================================
// SOURCE IMPLEMENTATION
// ============================================================================

ABerserkCharacter::ABerserkCharacter()
{
    PrimaryActorTick.bCanEverTick = false;
    PostureComponent = CreateDefaultSubobject<UPostureCombatComponent>(TEXT("PostureComponent"));
}

void ABerserkCharacter::BeginPlay()
{
    Super::BeginPlay();
}

void ABerserkCharacter::HandleIncomingAttack(AActor* Attacker, float RawPostureDamage, float RawHealthDamage, const FVector& HitLocation)
{
    if (!PostureComponent || !Attacker) return;

    float MitigatedHealthDamage = 0.0f;
    ECombatDefenseResult DefenseResult = PostureComponent->EvaluateIncomingStrike(RawPostureDamage, RawHealthDamage, MitigatedHealthDamage);

    switch (DefenseResult)
    {
        case ECombatDefenseResult::Deflect:
        {
            ExecuteDeflectEffects(HitLocation);
            
            if (UPostureCombatComponent* AttackerPosture = Attacker->FindComponentByClass<UPostureCombatComponent>())
            {
                AttackerPosture->ModifyPosture(RawPostureDamage * 1.5f);
            }
            break;
        }

        case ECombatDefenseResult::Block:
        {
            break;
        }

        case ECombatDefenseResult::Hit:
        case ECombatDefenseResult::StanceBroken:
        {
            break;
        }
    }
}

void ABerserkCharacter::ExecuteDeflectEffects(const FVector& ImpactPoint)
{
    UWorld* World = GetWorld();
    if (!World) return;

    UGameplayStatics::SetGlobalTimeDilation(World, DeflectTimeScale);

    float DilatedDuration = DeflectFreezeDuration * DeflectTimeScale;
    
    World->GetTimerManager().SetTimer(
        AsymmetricHitStopTimerHandle,
        this,
        &ABerserkCharacter::ResolveAsymmetricHitStop,
        DilatedDuration,
        false
    );

    APlayerController* PC = Cast<APlayerController>(GetController());
    if (PC && DeflectCameraShakeClass)
    {
        PC->ClientStartCameraShakeFromSource(
            DeflectCameraShakeClass,
            ImpactPoint,
            ShakeInnerRadius,
            ShakeOuterRadius,
            1.0f
        );
    }
}

void ABerserkCharacter::ResolveAsymmetricHitStop()
{
    UWorld* World = GetWorld();
    if (World)
    {
        UGameplayStatics::SetGlobalTimeDilation(World, 1.0f);
        AsymmetricHitStopTimerHandle.Invalidate();
    }
}