import os
import sys
from pathlib import Path
import pytest

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "..", "src")))

from hephaestus.soul import ArtificersSoul  # noqa: E402
from hephaestus.sentinel import CodeSentinel  # noqa: E402
from hephaestus.gaze import ArchitectsGaze  # noqa: E402

class TestHephaestusActivated:
    def test_soul_narrative_resonance(self):
        """Should verify that ArtificersSoul successfully computes narrative resonance."""
        soul = ArtificersSoul()
        
        # Test empty input -> default 1.0
        res_empty = soul.calculate_narrative_resonance("")
        assert res_empty == pytest.approx(1.0)
        
        # Test neutral input (no triggers) -> default 0.5
        res_neutral = soul.calculate_narrative_resonance("Just a standard test sentence with no special keywords.")
        assert res_neutral == pytest.approx(0.5)
        
        # Test emotional triggers -> should be greater than 0.5
        res_emotional = soul.calculate_narrative_resonance("We achieved victory and triumph, bringing hope to the team!")
        assert res_emotional > 0.5
        assert res_emotional <= 1.0
        
    def test_gaze_trace_semantic_web(self):
        """Should verify that ArchitectsGaze traces catalyst weaver tethers."""
        gaze = ArchitectsGaze()
        
        artifact_a = {
            "id": "GVRN.Registry.Origins",
            "content": "This is the origin of the sovereign convergence bridge.",
            "path": "_governance/10_Governance/GVRN.Registry.Origins.md"
        }
        artifact_b = {
            "id": "SYNG.Link.Forge",
            "content": "This establishes the deep structural integration and convergence of ingestion and forge.",
            "path": "_governance/09_Link/SYNG.Link.Forge.md"
        }
        
        report = gaze.trace_semantic_web(artifact_a, artifact_b)
        
        assert report["source"] == "GVRN.Registry.Origins"
        assert report["target"] == "SYNG.Link.Forge"
        assert "resonance_score" in report
        assert report["resonance_score"] >= 0.0
        assert report["status"] in ("Aligned", "Dissonant")
        assert "timestamp" in report
        
        # Assert tethers are woven in CatalystWeaver bundle
        blueprints = gaze.weaver.bundle.blueprints
        blueprint_names = [bp["name"] for bp in blueprints]
        assert "GVRN.Registry.Origins" in blueprint_names
        assert "SYNG.Link.Forge" in blueprint_names
        
        processes = gaze.weaver.bundle.processes
        assert len(processes) > 0
        assert any("TETHER" in p for p in processes)

    def test_sentinel_scan_governance(self):
        """Should verify that CodeSentinel successfully scans and writes to triage report."""
        sentinel = CodeSentinel()
        
        # Scan a subdirectory to keep the test fast
        test_scan_dir = os.path.abspath(os.path.join(current_dir, "..", "src", "hephaestus"))
        
        report = sentinel.scan_governance(test_scan_dir)
        
        assert "resonance_score" in report
        assert "dissonant_files" in report
        assert "detailed_findings" in report
        
        # Verify triage report got updated
        workspace_root = Path(test_scan_dir).resolve()
        report_path = None
        curr = workspace_root
        while curr != curr.parent:
            potential = curr / "_governance" / "5_Logs" / "GVRN.Triage.Report.md"
            if potential.parent.exists():
                report_path = potential
                break
            curr = curr.parent
            
        assert report_path is not None
        assert report_path.exists()
        
        with open(report_path, "r", encoding="utf-8") as f:
            triage_content = f.read()
            
        assert "Sentinel Scan" in triage_content
        assert "Score" in triage_content
