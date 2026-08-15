// System Identifier: PRS-001-ENG-032
// File: DynamicOcclusionAudioLinker.cpp (Includes Header & Implementation)

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "CollisionQueryParams.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"
#include "GeometryCollection/GeometryCollectionComponent.h"
#include "Kismet/GameplayStatics.h"
#include "DynamicOcclusionAudioLinker.generated.h"

// ============================================================================
// HEADER DECLARATION
// ============================================================================

UCLASS()
class BERSERKGAME_API UDynamicOcclusionAudioLinker : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category = "Mass Kinetic Cleave | Audio Occlusion")
    static float CalculateDebrisOcclusionFactor(
        const UObject* WorldContextObject, 
        const FVector& SoundOrigin, 
        float& OutLowPassCutoff
    );

private:
    static const float MaxObstructingDebrisCount;
    static const float BaseUnoccludedFrequency;
    static const float MuffledFrequencyFloor;
};

// ============================================================================
// SOURCE IMPLEMENTATION
// ============================================================================

const float UDynamicOcclusionAudioLinker::MaxObstructingDebrisCount = 6.0f;
const float UDynamicOcclusionAudioLinker::BaseUnoccludedFrequency = 20000.0f;
const float UDynamicOcclusionAudioLinker::MuffledFrequencyFloor = 400.0f;

float UDynamicOcclusionAudioLinker::CalculateDebrisOcclusionFactor(
    const UObject* WorldContextObject, 
    const FVector& SoundOrigin, 
    float& OutLowPassCutoff)
{
    UWorld* World = GEngine->GetWorldFromContextObject(WorldContextObject, EGetWorldErrorMode::LogAndReturnNull);
    if (!World)
    {
        OutLowPassCutoff = BaseUnoccludedFrequency;
        return 1.0f;
    }

    APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
    if (!PC || !PC->PlayerCameraManager)
    {
        OutLowPassCutoff = BaseUnoccludedFrequency;
        return 1.0f;
    }

    FVector CameraLocation = PC->PlayerCameraManager->GetCameraLocation();

    TArray<FHitResult> OutHits;
    FCollisionQueryParams TraceParams(SCENE_QUERY_STAT(DebrisAudioOcclusion), true);
    TraceParams.bTraceComplex = false;

    bool bHit = World->LineTraceMultiByChannel(
        OutHits, 
        CameraLocation, 
        SoundOrigin, 
        ECC_WorldDynamic, 
        TraceParams
    );

    float DebrisObstructionScore = 0.0f;

    if (bHit)
    {
        for (const FHitResult& Hit : OutHits)
        {
            UGeometryCollectionComponent* ChaosComp = Cast<UGeometryCollectionComponent>(Hit.GetComponent());
            if (ChaosComp)
            {
                DebrisObstructionScore += 1.0f;
            }
        }
    }

    float OcclusionRatio = FMath::Clamp(DebrisObstructionScore / MaxObstructingDebrisCount, 0.0f, 1.0f);
    float HighFrequencyFactor = FMath::Lerp(1.0f, 0.15f, FMath::Pow(OcclusionRatio, 1.5f));
    
    OutLowPassCutoff = FMath::Lerp(BaseUnoccludedFrequency, MuffledFrequencyFloor, OcclusionRatio);

    return HighFrequencyFactor;
}