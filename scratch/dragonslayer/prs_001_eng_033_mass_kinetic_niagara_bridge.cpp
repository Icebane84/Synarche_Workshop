// System Identifier: PRS-001-ENG-033
// File: MassKineticNiagaraBridge.cpp (Includes Header & Implementation)

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "NiagaraFunctionLibrary.h"
#include "NiagaraComponent.h"
#include "GeometryCollection/GeometryCollectionComponent.h"
#include "Engine/World.h"
#include "MassKineticNiagaraBridge.generated.h"

class UNiagaraSystem;

// ============================================================================
// HEADER DECLARATION
// ============================================================================

UCLASS()
class BERSERKGAME_API UMassKineticNiagaraBridge : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    UMassKineticNiagaraBridge();

    UFUNCTION(BlueprintCallable, Category = "Mass Kinetic Cleave | VFX")
    static void SpawnShearedDustLine(
        const UObject* WorldContextObject,
        UNiagaraSystem* NiagaraSystemTemplate,
        UGeometryCollectionComponent* TargetMesh,
        const FVector& EntrancePoint,
        const FVector& SwingDirection,
        const FVector& PlaneNormal,
        float KineticEnergy
    );
};

// ============================================================================
// SOURCE IMPLEMENTATION
// ============================================================================

UMassKineticNiagaraBridge::UMassKineticNiagaraBridge()
{
}

void UMassKineticNiagaraBridge::SpawnShearedDustLine(
    const UObject* WorldContextObject,
    UNiagaraSystem* NiagaraSystemTemplate,
    UGeometryCollectionComponent* TargetMesh,
    const FVector& EntrancePoint,
    const FVector& SwingDirection,
    const FVector& PlaneNormal,
    float KineticEnergy)
{
    if (!NiagaraSystemTemplate || !TargetMesh) return;

    UWorld* World = GEngine->GetWorldFromContextObject(WorldContextObject, EGetWorldErrorMode::LogAndReturnNull);
    if (!World) return;

    FVector NormalizedSwing = SwingDirection.GetSafeNormal();
    FVector TraceEnd = EntrancePoint + (NormalizedSwing * 300.0f);

    FHitResult ExitHit;
    FCollisionQueryParams TraceParams(SCENE_QUERY_STAT(CleaveExitTrace), true);
    TraceParams.bTraceComplex = false;

    FVector ExitPoint = EntrancePoint + (NormalizedSwing * 120.0f);
    
    if (World->LineTraceSingleByChannel(ExitHit, EntrancePoint, TraceEnd, ECC_WorldDynamic, TraceParams))
    {
        ExitPoint = ExitHit.ImpactPoint;
    }

    FVector ExitVelocityVector = (NormalizedSwing * (KineticEnergy * 0.15f)) + (FVector::UpVector * (KineticEnergy * 0.05f));

    float MaxVelocityClamp = 4500.0f;
    if (ExitVelocityVector.Size() > MaxVelocityClamp)
    {
        ExitVelocityVector = ExitVelocityVector.GetSafeNormal() * MaxVelocityClamp;
    }

    UNiagaraComponent* NiagaraComp = UNiagaraFunctionLibrary::SpawnSystemAtLocation(
        World,
        NiagaraSystemTemplate,
        ExitPoint,
        FRotator::ZeroRotator,
        FVector(1.0f),
        true,
        true,
        ENiagaraAttachmentRule::KeepWorld,
        true
    );

    if (NiagaraComp)
    {
        NiagaraComp->SetVariableVec3(FName("User.ExitVelocity"), ExitVelocityVector);
        NiagaraComp->SetVariableVec3(FName("User.PlaneNormal"), PlaneNormal);
        NiagaraComp->SetVariableFloat(FName("User.KineticScale"), FMath::Clamp(KineticEnergy / 25000.0f, 0.1f, 2.5f));
        NiagaraComp->SetVariableVec3(FName("User.SwingDirection"), NormalizedSwing);
    }
}