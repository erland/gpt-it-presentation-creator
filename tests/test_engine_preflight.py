from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_mandatory_engine_preflight():
    core = (ROOT / "canonical/core.md").read_text()
    for marker in ("Obligatorisk Engine-preflight", "invänta uppladdning",
                   "Ingen automatisk fallback", "uttryckligt användargodkännande",
                   "exakt runtimeversion", "filhashar", "självtest",
                   "Ren rådgivning", "releases/download/vVERSION/"):
        assert marker in core

def test_no_implicit_fallback_in_skills():
    for path in (ROOT / "canonical/skills").glob("*/behavior.md"):
        text = path.read_text()
        assert "Följ obligatorisk Engine-preflight" in text
        assert "be om paketet vid behov" not in text
        assert "eller använd värdens PPTX-funktioner" not in text


def test_single_skill_and_workflow_routing():
    import yaml
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text())
    definitions = cfg["skills"]["definitions"]
    assert [s["id"] for s in definitions] == ["it-presentation-creator"]
    assert len(list((ROOT / "canonical/skills").glob("*/behavior.md"))) == 1
    core = (ROOT / "canonical/core.md").read_text()
    for name, marker in (("presentation-design", "Välj layout efter budskap"),
                         ("powerpoint-creation", "transform_objects"),
                         ("presentation-review", "Jämför före och efter")):
        path = f"knowledge/workflows/{name}.md"
        assert path in definitions[0]["references"]
        assert marker in (ROOT / path).read_text()
        assert f"{name}.md" in core
    assert "Granskning är obligatorisk" in core
    assert "Ingen Engine." in core
