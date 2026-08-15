// System Identifier: PRS-001-ENG-026
// File: MassKineticCleaveComponent.cpp (Includes Header & Implementation)

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Kismet/GameplayStatics.h"
#include "GeometryCollection/GeometryCollectionComponent.h"
#include "Engine/OverlapResult.h"
#include "Engine/World.h"
#include "MassKineticCleaveComponent.generated.h"

// ============================================================================
// HEADER DECLARATION
// ============================================================================

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class BERSERKGAME_API UMassKineticCleaveComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UMassKineticCleaveComponent();

protected:
    virtual void BeginPlay() override;

public:
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    UFUNCTION(BlueprintCallable, Category = "Mass Kinetic Cleave")
    void StartCleaveSwing();

    UFUNCTION(BlueprintCallable, Category = "Mass Kinetic Cleave")
    void StopCleaveSwing();

protected:
    void ProcessCleaveTrace(float DeltaTime);
    void InjectStrainToChaos(UGeometryCollectionComponent* TargetMesh, const FVector& ImpactPoint, const FVector& ImpactDirection, float CalculatedEnergy);
    void TriggerHitStop(float Duration);
    void ResetHitStop();

private:
    UPROPERTY(EditAnywhere, Category = "Cleave Engine | Configuration")
    float WeaponMassKG = 180.0f;

    UPROPERTY(EditAnywhere, Category = "Cleave Engine | Configuration")
    float StructuralThresholdJoules = 4500.0f;

    UPROPERTY(EditAnywhere, Category = "Cleave Engine | Sockets")
    FName WeaponBaseSocketName = FName("Socket_Base");

    UPROPERTY(EditAnywhere, Category = "Cleave Engine | Sockets")
    FName WeaponTipSocketName = FName("Socket_Tip");

    UPROPERTY(EditAnywhere, Category = "Cleave Engine | Visuals")
    float HitStopTimeDilation = 0.05f;

    bool bIsSwinging = false;
    FVector LastBaseLocation;
    FVector LastTipLocation;
    FTimerHandle HitStopTimerHandle;

    UPROPERTY()
    UMeshComponent* WeaponMeshComponent;
};

// ============================================================================
// SOURCE IMPLEMENTATION
// ============================================================================

UMassKineticCleaveComponent::UMassKineticCleaveComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
    PrimaryComponentTick.bStartWithTickEnabled = true;
}

void UMassKineticCleaveComponent::BeginPlay()
{
    Super::BeginPlay();

    AActor* Owner = GetOwner();
    if (Owner)
    {
        WeaponMeshComponent = Owner->FindComponentByClass<UMeshComponent>();
    }
}

void UMassKineticCleaveComponent::StartCleaveSwing()
{
    if (WeaponMeshComponent)
    {
        bIsSwinging = true;
        LastBaseLocation = WeaponMeshComponent->GetSocketLocation(WeaponBaseSocketName);
        LastTipLocation = WeaponMeshComponent->GetSocketLocation(WeaponTipSocketName);
    }
}

void UMassKineticCleaveComponent::StopCleaveSwing()
{
    bIsSwinging = false;
}

void UMassKineticCleaveComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    if (bIsSwinging)
    {
        ProcessCleaveTrace(DeltaTime);
    }
}

void UMassKineticCleaveComponent::ProcessCleaveTrace(float DeltaTime)
{
    if (!WeaponMeshComponent || DeltaTime <= 0.0f) return;

    FVector CurrentBase = WeaponMeshComponent->GetSocketLocation(WeaponBaseSocketName);
    FVector CurrentTip = WeaponMeshComponent->GetSocketLocation(WeaponTipSocketName);

    FVector BaseVelocity = (CurrentBase - LastBaseLocation) / DeltaTime;
    FVector TipVelocity = (CurrentTip - LastTipLocation) / DeltaTime;
    FVector MeanVelocityVector = (BaseVelocity + TipVelocity) * 0.5f;
    float SpeedMPS = MeanVelocityVector.Size() / 100.0f;

    float KineticEnergyJoules = 0.5f * WeaponMassKG * (SpeedMPS * SpeedMPS);

    FVector SwingCenter = (CurrentBase + CurrentTip + LastBaseLocation + LastTipLocation) * 0.25f;
    float HalfHeight = FVector::Dist(CurrentBase, CurrentTip) * 0.5f;
    float Radius = 30.0f;

    FCollisionShape SweepCapsule = FCollisionShape::MakeCapsule(Radius, HalfHeight);

    TArray<FOverlapResult> Overlaps;
    FCollisionQueryParams QueryParams;
    QueryParams.AddIgnoredActor(GetOwner());
    if (GetOwner() && GetOwner()->GetOwner())
    {
        QueryParams.AddIgnoredActor(GetOwner()->GetOwner());
    }

    UWorld* World = GetWorld();
    if (World && World->OverlapMultiByChannel(Overlaps, SwingCenter, FQuat::Identity, ECC_WorldDynamic, SweepCapsule, QueryParams))
    {
        for (const FOverlapResult& Overlap : Overlaps)
        {
            UGeometryCollectionComponent* GeomComp = Cast<UGeometryCollectionComponent>(Overlap.GetComponent());
            if (GeomComp)
            {
                FVector ImpactPoint = Overlap.ImpactPoint.IsZero() ? SwingCenter : Overlap.ImpactPoint;
                FVector ImpactDirection = MeanVelocityVector.GetSafeNormal();

                InjectStrainToChaos(GeomComp, ImpactPoint, ImpactDirection, KineticEnergyJoules);
            }
        }
    }

    LastBaseLocation = CurrentBase;
    LastTipLocation = CurrentTip;
}

void UMassKineticCleaveComponent::InjectStrainToChaos(UGeometryCollectionComponent* TargetMesh, const FVector& ImpactPoint, const FVector& ImpactDirection, float CalculatedEnergy)
{
    if (!TargetMesh) return;

    if (CalculatedEnergy >= StructuralThresholdJoules)
    {
        float ScaledImpulseStrength = CalculatedEnergy * 50.0f;
        TargetMesh->ApplyKineticField(ScaledImpulseStrength, ImpactPoint, ImpactDirection, 150.0f);
        TargetMesh->ApplyRadialForce(ImpactPoint, 200.0f, ScaledImpulseStrength * 0.5f, ERadialImpulseFalloff::RIF_Constant);

        TriggerHitStop(0.08f);
    }
}

void UMassKineticCleaveComponent::TriggerHitStop(float Duration)
{
    UWorld* World = GetWorld();
    if (World && !HitStopTimerHandle.IsValid())
    {
        UGameplayStatics::SetGlobalTimeDilation(World, HitStopTimeDilation);

        World->GetTimerManager().SetTimer(
            HitStopTimerHandle, 
            this, 
            &UMassKineticCleaveComponent::ResetHitStop, 
            Duration * HitStopTimeDilation, 
            false
        );
    }
}

void UMassKineticCleaveComponent::ResetHitStop()
{
    UWorld* World = GetWorld();
    if (World)
    {
        UGameplayStatics::SetGlobalTimeDilation(World, 1.0f);
        HitStopTimerHandle.Invalidate();
    }
}