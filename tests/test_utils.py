from app.utils import safe_json_loads, flatten_tree, strip_text_for_planning


def test_safe_json_loads_extracts_json():
    assert safe_json_loads('hello {"grade":"yes"} bye')['grade'] == 'yes'


def test_flatten_tree():
    tree = [{'id': 'a', 'children': [{'id': 'b', 'children': []}]}]
    node_map = flatten_tree(tree)
    assert set(node_map.keys()) == {'a', 'b'}


def test_strip_text_removes_text():
    tree = [{'id': 'a', 'title': 'T', 'text': 'secret', 'children': []}]
    stripped = strip_text_for_planning(tree)
    assert 'text' not in stripped[0]
