import unittest
import os
import sys
import json
import shutil
from cpp_verifier import analyze_cpp_file, run_verifier

class TestCppVerifier(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.abspath("test_temp_cpp")
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_valid_cpp_file(self):
        content = """// System Identifier: PRS-001-ENG-999
#pragma once
#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "ValidComponent.generated.h"

UCLASS(meta=(BlueprintSpawnableComponent))
class BERSERKGAME_API UValidComponent : public UActorComponent
{
    GENERATED_BODY()
public:
    UValidComponent();
protected:
    virtual void BeginPlay() override;
    
    UPROPERTY(EditAnywhere, Category = "Test")
    UActorComponent* LinkedComponent;
};
"""
        file_path = os.path.join(self.test_dir, "ValidComponent.cpp")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        violations = analyze_cpp_file(file_path)
        self.assertEqual(len(violations), 0, f"Expected no violations, found: {violations}")

    def test_unbalanced_braces(self):
        content = """#include "ValidComponent.generated.h"
class UValidComponent : public UActorComponent {
    GENERATED_BODY()
// Missing closing brace
"""
        file_path = os.path.join(self.test_dir, "UnbalancedBraces.cpp")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        violations = analyze_cpp_file(file_path)
        rules = [v["rule"] for v in violations]
        self.assertIn("SYNTAX_UNBALANCED_BRACES", rules)

    def test_raw_delete_violation(self):
        content = """#include "ValidComponent.generated.h"
void DestroyStuff() {
    delete TargetPointer;
}
"""
        file_path = os.path.join(self.test_dir, "RawDelete.cpp")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        violations = analyze_cpp_file(file_path)
        rules = [v["rule"] for v in violations]
        self.assertIn("SAFETY_RAW_DELETE", rules)

    def test_untracked_pointer_violation(self):
        content = """#include "ValidComponent.generated.h"
class UValidComponent : public UActorComponent {
    GENERATED_BODY()
    // Raw pointer component member without UPROPERTY()
    UActorComponent* UnsafeComponent;
};
"""
        file_path = os.path.join(self.test_dir, "UntrackedPointer.cpp")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        violations = analyze_cpp_file(file_path)
        rules = [v["rule"] for v in violations]
        self.assertIn("SAFETY_UNTRACKED_POINTER", rules)

    def test_unrecognized_symbol_violation(self):
        content = """#include "ValidComponent.generated.h"
void UseUnknown() {
    UNeedlessUnsafeSymbol* BadSymbol = nullptr;
}
"""
        file_path = os.path.join(self.test_dir, "UnrecognizedSymbol.cpp")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        violations = analyze_cpp_file(file_path)
        rules = [v["rule"] for v in violations]
        self.assertIn("SYMBOL_UNRECOGNIZED", rules)

    def test_telemetry_generation(self):
        content = """#include "ValidComponent.generated.h"
class UValidComponent : public UActorComponent {
    GENERATED_BODY()
};
"""
        file_path = os.path.join(self.test_dir, "ValidComponent.cpp")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        exit_code = run_verifier([self.test_dir])
        self.assertEqual(exit_code, 0)

        # Check telemetry file
        log_path = "c:\\Users\\Chris\\Synarche_Workspace\\_governance\\50_Logs\\LOG.MECS.TELEMETRY_CPP.json"
        self.assertTrue(os.path.exists(log_path))
        with open(log_path, "r", encoding="utf-8") as lf:
            data = json.load(lf)
            self.assertIn("timestamp", data)
            self.assertIn("verified_files", data)
            self.assertEqual(data["exit_code"], 0)

if __name__ == "__main__":
    unittest.main()
