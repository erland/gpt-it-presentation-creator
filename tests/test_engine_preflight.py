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
