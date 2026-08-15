// System Identifier: PRS-001-ENG-030
// File: DirectionalCleaveInterface.cpp (Includes Header & Implementation)

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "GeometryCollection/GeometryCollectionComponent.h"
#include "GeometryCollection/GeometryCollectionObject.h"
#include "Engine/World.h"
#include "DrawDebugHelpers.h"
#include "DirectionalCleaveInterface.generated.h"

// ============================================================================
// HEADER DECLARATION
// ============================================================================

UCLASS(BlueprintType, Blueprintable)
class BERSERKGAME_API UDirectionalCleaveInterface : public UObject
{
    GENERATED_BODY()

public:
    UDirectionalCleaveInterface();

    UFUNCTION(BlueprintCallable, Category = "Mass Kinetic Cleave | Physics Linker")
    static void ProjectPlanarCleaveToChaos(
        UGeometryCollectionComponent* TargetMesh, 
        const FVector& CutOrigin, 
        const FVector& SwingDirection, 
        const FVector& WeaponNormal, 
        float KineticEnergy
    );
};

// ============================================================================
// SOURCE IMPLEMENTATION
// ============================================================================

UDirectionalCleaveInterface::UDirectionalCleaveInterface()
{
}

void UDirectionalCleaveInterface::ProjectPlanarCleaveToChaos(
    UGeometryCollectionComponent* TargetMesh, 
    const FVector& CutOrigin, 
    const FVector& SwingDirection, 
    const FVector& WeaponNormal, 
    float KineticEnergy)
{
    if (!TargetMesh || !TargetMesh->GetGeometryCollection()) return;

    UWorld* World = TargetMesh->GetWorld();
    if (!World) return;

    FVector PlaneNormal = WeaponNormal.GetSafeNormal();
    float BaseForceScale = KineticEnergy * 65.0f; 
    float CleaveMaxRadius = 250.0f;

    TArray<FTransform> ComponentTransforms;
    TargetMesh->GetInstanceTransforms(ComponentTransforms);

#if !UE_BUILD_SHIPPING
    DrawDebugCircle(World, CutOrigin, CleaveMaxRadius, FQuat::FindBetweenVectors(FVector::UpVector, PlaneNormal), FColor::Cyan, false, 2.5f, 0, 2.5f);
#endif

    for (int32 TransformIdx = 0; TransformIdx < ComponentTransforms.Num(); ++TransformIdx)
    {
        FVector FragmentWorldLoc = ComponentTransforms[TransformIdx].GetLocation();
        float DistanceToOrigin = FVector::Dist(FragmentWorldLoc, CutOrigin);

        if (DistanceToOrigin <= CleaveMaxRadius)
        {
            FVector ToFragment = FragmentWorldLoc - CutOrigin;
            float PlaneDistance = FVector::DotProduct(ToFragment, PlaneNormal);

            if (FMath::Abs(PlaneDistance) <= 25.0f)
            {
                TargetMesh->ApplyKineticField(BaseForceScale, FragmentWorldLoc, SwingDirection, 50.0f);

                FVector SplittingImpulseDirection = SwingDirection + (PlaneNormal * FMath::Sign(PlaneDistance) * 0.4f);
                SplittingImpulseDirection.Normalize();

                TargetMesh->ApplyRadialForce(FragmentWorldLoc, 60.0f, BaseForceScale * 0.75f, ERadialImpulseFalloff::RIF_Linear);
            }
        }
    }
}