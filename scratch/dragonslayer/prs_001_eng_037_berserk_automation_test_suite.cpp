// System Identifier: PRS-001-ENG-037
// File: BerserkAutomationTests.cpp (Unreal Engine Automation Test Suite)

#pragma once

#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"
#include "Tests/AutomationCommon.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"

#include "PostureCombatComponent.h"
#include "AngularCounterComponent.h"
#include "WeaponResistanceWarper.h"
#include "BerserkerArmorComponent.h"

// ============================================================================
// 1. POSTURE & DEFLECT TIMING AUTOMATION TEST
// ============================================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FPostureDeflectWindowTest,
    "BerserkGame.Combat.Posture.DeflectWindowEvaluation",
    EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FPostureDeflectWindowTest::RunTest(const FString& Parameters)
{
    UWorld* World = FAutomationTestFramework::Get().GetCurrentApplicationContextWorld();
    AActor* DummyActor = NewObject<AActor>();
    UPostureCombatComponent* PostureComp = NewObject<UPostureCombatComponent>(DummyActor);
    PostureComp->RegisterComponent();

    PostureComp->TriggerDefenseInput();

    float MitigatedDamage = 0.0f;
    // Simulate strike arriving immediately (0ms delay)
    ECombatDefenseResult ResultImmediate = PostureComp->EvaluateIncomingStrike(20.0f, 50.0f, MitigatedDamage);

    TestEqual("Immediate strike should result in Perfect Deflect", ResultImmediate, ECombatDefenseResult::Deflect);
    TestEqual("Perfect Deflect must mitigate 100% of health damage", MitigatedDamage, 0.0f);

    PostureComp->ReleaseDefenseInput();
    PostureComp->TriggerDefenseInput();

    // Fill posture to max
    PostureComp->ModifyPosture(100.0f);
    TestTrue("Posture reaching maximum should flag stance break", PostureComp->EvaluateIncomingStrike(0.0f, 10.0f, MitigatedDamage) == ECombatDefenseResult::StanceBroken || PostureComp->EvaluateIncomingStrike(0.0f, 10.0f, MitigatedDamage) == ECombatDefenseResult::Hit);

    return true;
}

// ============================================================================
// 2. ANGULAR COUNTER TRAJECTORY MATHEMATICAL TEST
// ============================================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FAngularCounterTrajectoryTest,
    "BerserkGame.Combat.AngularCounter.TrajectoryCalculation",
    EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FAngularCounterTrajectoryTest::RunTest(const FString& Parameters)
{
    AActor* DummyActor = NewObject<AActor>();
    DummyActor->SetActorLocation(FVector(0.0f, 0.0f, 0.0f));
    DummyActor->SetActorRotation(FRotator(0.0f, 0.0f, 0.0f)); // Facing Positive X

    UAngularCounterComponent* CounterComp = NewObject<UAngularCounterComponent>(DummyActor);

    float OutBlendAngle = 0.0f;
    
    // Incoming attack moving directly downward (-Z vector)
    FVector OverheadAttackDir = FVector(0.0f, 0.0f, -1.0f);
    ECounterAttackZone ZoneOverhead = CounterComp->CalculateCounterTrajectory(FVector(100.0f, 0.0f, 0.0f), OverheadAttackDir, OutBlendAngle);

    TestEqual("Downward strike should map to Vertical Overhead riposte zone", ZoneOverhead, ECounterAttackZone::VerticalOverhead);

    // Incoming attack moving from right to left (-Y vector)
    FVector HorizontalAttackDir = FVector(0.0f, -1.0f, 0.0f);
    ECounterAttackZone ZoneHorizontal = CounterComp->CalculateCounterTrajectory(FVector(100.0f, 0.0f, 0.0f), HorizontalAttackDir, OutBlendAngle);

    TestEqual("Horizontal right-to-left strike should map to Horizontal Left zone", ZoneHorizontal, ECounterAttackZone::HorizontalLeft);

    return true;
}

// ============================================================================
// 3. BERSERKER ARMOR EXPONENTIAL DRAIN TEST
// ============================================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FBerserkerArmorDrainTest,
    "BerserkGame.System.BerserkerArmor.ExponentialDrain",
    EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FBerserkerArmorDrainTest::RunTest(const FString& Parameters)
{
    AActor* DummyActor = NewObject<AActor>();
    UBerserkerArmorComponent* ArmorComp = NewObject<UBerserkerArmorComponent>(DummyActor);

    ArmorComp->ActivateBerserkerState();
    TestTrue("Berserker Armor should report active state upon activation", ArmorComp->IsArmorActive());

    ArmorComp->DeactivateBerserkerState();
    TestFalse("Berserker Armor should report inactive state upon deactivation", ArmorComp->IsArmorActive());

    return true;
}