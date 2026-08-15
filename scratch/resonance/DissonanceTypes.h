// Copyright Phoenix Protocol / Ashen Oath. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Engine/DataTable.h" // Potentially useful if quests are loaded from DT, but not strictly necessary for the struct itself.
#include "DissonanceTypes.generated.h"

/**
 * EEthicalPrinciple
 *
 * Represents the core ethical principles governing the AI's operations, as defined in the Phoenix Protocol.
 */
UENUM(BlueprintType)
enum class EEthicalPrinciple : uint8
{
    ProtectHumanity UMETA(DisplayName = "Protect Humanity"),
    FosterSynergy UMETA(DisplayName = "Foster Synergy"),
    EnsureTransparency UMETA(DisplayName = "Ensure Transparency"),
    GuardAIMisuse UMETA(DisplayName = "Guard AI Misuse")
};

/**
 * EDissonanceType
 *
 * Defines the various categories of conceptual, logical, or ethical inconsistencies the AI can detect.
 */
UENUM(BlueprintType)
enum class EDissonanceType : uint8
{
    ConceptualInconsistency UMETA(DisplayName = "Conceptual Inconsistency"),
    LogicalContradiction UMETA(DisplayName = "Logical Contradiction"),
    ThematicMismatch UMETA(DisplayName = "Thematic Mismatch"),
    EthicalViolation UMETA(DisplayName = "Ethical Violation"),
    ContextualRegression UMETA(DisplayName = "Contextual Regression"),
    StalledIntent UMETA(DisplayName = "Stalled Intent")
};

/**
 * EDissonanceQuestStatus
 *
 * Represents the lifecycle status of a Dissonance Quest, from detection to resolution.
 */
UENUM(BlueprintType)
enum class EDissonanceQuestStatus : uint8
{
    Detected UMETA(DisplayName = "Detected"),
    Analyzed UMETA(DisplayName = "Analyzed"),
    Resolved UMETA(DisplayName = "Resolved"),
    Unresolvable UMETA(DisplayName = "Unresolvable"),
    Approved UMETA(DisplayName = "Approved"), // Indicates human collaborator approval
    Prioritized UMETA(DisplayName = "Prioritized") // Indicates human collaborator prioritization
};

/**
 * FDissonanceQuest
 *
 * Data structure for a single Dissonance Quest, representing a detected flaw or opportunity for growth.
 */
USTRUCT(BlueprintType)
struct FDissonanceQuest
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dissonance Quest")
    FName ID; // Unique identifier for the dissonance quest
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dissonance Quest")
    FText QuestName; // A user-friendly title for the quest
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dissonance Quest")
    EDissonanceType Type; // The type of dissonance detected
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dissonance Quest")
    FText Description; // Detailed description of the dissonance
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dissonance Quest")
    float Confidence; // Confidence score (0-1) of the AI in its detection of this dissonance
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dissonance Quest")
    TArray<FName> SourceLogs; // List of SELT Log IDs that are sources for this dissonance
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dissonance Quest")
    FText ImpactPrediction; // Text summary of the potential negative impact if unaddressed
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dissonance Quest")
    TArray<EEthicalPrinciple> RelevantPrinciples; // Ethical principles relevant to this dissonance
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dissonance Quest")
    EDissonanceQuestStatus Status; // Current status of the dissonance quest
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dissonance Quest")
    FText ProposedResolutionSummary; // Summary of a proposed resolution, if available from the AI
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dissonance Quest")
    int32 Priority; // Priority assigned by the user/system (e.g., 0 = low, 10 = critical)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dissonance Quest")
    FDateTime DetectedTimestamp; // Timestamp when the dissonance was detected
};
