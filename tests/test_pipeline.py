import pymupdf

from iimrr.alias_match import match_section
from iimrr.orchestrator import extract_section
from iimrr.tier1_structural import parse_toc_positions, parse_toc_text
from iimrr.validation import validate_candidate


def test_alias_matching():
    assert match_section("MANAGEMENT DISCUSSION & ANALYSIS")[0] == "mdna"
    assert match_section("Report on Corporate Governance")[0] == "corp_governance"


def test_toc_parser():
    text = "Management Discussion & Analysis .......... 12\nDirectors' Report     30"
    assert parse_toc_text(text) == [("Management Discussion & Analysis", 12), ("Directors' Report", 30)]


def test_positioned_toc_parser_handles_no_dot_leaders():
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Management Discussion & Analysis")
    page.insert_text((500, 72), "12")
    entries = parse_toc_positions(page)
    assert ("Management Discussion & Analysis", 12) in entries
    doc.close()


def test_bookmark_extracts_original_pages(tmp_path):
    source = tmp_path / "report.pdf"
    output = tmp_path / "slice.pdf"
    doc = pymupdf.open()
    for label in ("Cover", "Management Discussion & Analysis", "MD&A detail", "Directors Report"):
        page = doc.new_page()
        page.insert_text((72, 72), label)
    doc.set_toc([[1, "Management Discussion & Analysis", 2], [1, "Directors Report", 4]])
    doc.save(source)
    doc.close()
    result = extract_section(source, "mdna", output)
    assert result["status"] == "success"
    sliced = pymupdf.open(output)
    assert sliced.page_count == 2
    assert "MD&A detail" in sliced[1].get_text()
    sliced.close()


def test_validation_requires_affirmative_boundary_evidence():
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), "A page unrelated to the requested section")
    valid, signals = validate_candidate(doc, "mdna", 0, 0)
    assert not valid
    assert "affirmative" in signals["notes"]
    doc.close()


def test_existing_output_directory_gets_a_generated_pdf_name(tmp_path):
    source = tmp_path / "report.pdf"
    destination = tmp_path / "Output"
    destination.mkdir()
    doc = pymupdf.open()
    for label in ("Management Discussion & Analysis", "Directors Report"):
        page = doc.new_page()
        page.insert_text((72, 72), label)
    doc.set_toc([[1, "Management Discussion & Analysis", 1], [1, "Directors Report", 2]])
    doc.save(source)
    doc.close()
    result = extract_section(source, "mdna", destination)
    assert result["status"] == "success"
    assert (destination / "report_mdna.pdf").is_file()


def test_progress_callback_reports_pipeline_steps(tmp_path):
    source = tmp_path / "report.pdf"
    output = tmp_path / "slice.pdf"
    doc = pymupdf.open()
    for label in ("Management Discussion & Analysis", "Directors Report"):
        page = doc.new_page()
        page.insert_text((72, 72), label)
    doc.set_toc([[1, "Management Discussion & Analysis", 1], [1, "Directors Report", 2]])
    doc.save(source)
    doc.close()
    messages = []
    result = extract_section(source, "mdna", output, progress_callback=messages.append)
    assert result["status"] == "success"
    assert any("bookmarks" in item.lower() for item in messages)
    assert any("writing" in item.lower() for item in messages)
