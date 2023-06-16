from typing import Final

from routine.model.page import Page, NotesDTO, BlockDTO

TEST_JSON_DATA: Final[dict] = {
    "created": "2023-01-01T12:12:12-00:00",
    "id": "page:xxx",
    "notes": {"blocks": [{"content": "Test Paragraph", "id": "block:xxx", "type": "paragraph"}]},
    "parent": "page:xxx",
    "title": "Test Page",
}


def test_json_parsing():
    p = Page(**TEST_JSON_DATA)

    assert p.title == "Test Page"
    assert p.id.startswith("page:")
    assert p.parent.startswith("page:")
    assert isinstance(p.notes, NotesDTO)
    assert all([isinstance(e, BlockDTO) for e in p.notes.blocks])

    test_block = p.notes.blocks[0]
    assert test_block.id.startswith("block:")
    assert test_block.type == "paragraph"
    assert test_block.content == "Test Paragraph"
