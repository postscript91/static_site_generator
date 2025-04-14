import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_href(self):
        # Create a node with href property
        node = HTMLNode("a", "Click me!", None, {"href": "https://www.google.com"})
        # Test that props_to_html returns the correct string
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
    
    def test_props_to_html_with_multiple_props(self):
        # Create a node with multiple properties
        node = HTMLNode("a", "Click me!", None, {"href": "https://www.google.com", "target": "_blank"})
        # Test that props_to_html returns the correct string with both properties
        # Note: You might need to check both possible orders since dictionaries don't guarantee order
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)
    
    def test_props_to_html_with_no_props(self):
        # Create a node with no properties
        node = HTMLNode("p", "Hello, world!", None, None)
        # Test that props_to_html returns an empty string
        self.assertEqual(node.props_to_html(), '')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_img_tag(self):
        node = LeafNode("img", "Image description", {"src": "image.jpg", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="An image">Image description</img>')

    def test_leaf_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_multiple_leaf_children(self):
        parent = ParentNode("ul", [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2"),
            LeafNode("li", "Item 3")
        ])
        self.assertEqual(parent.to_html(), "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>")

    def test_parent_with_props(self):
        parent = ParentNode("div", [LeafNode("span", "Hello")], {"class": "container", "id": "main"})
        self.assertEqual(parent.to_html(), '<div class="container" id="main"><span>Hello</span></div>')

    def test_missing_tag_error(self):
        node = ParentNode(None, [LeafNode("p", "text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_empty_children_error(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_complex_nesting(self):
        node = ParentNode("section", [
            ParentNode("header", [LeafNode("h1", "Title")]),
            ParentNode("article", [
                LeafNode("p", "Paragraph 1"),
                LeafNode("p", "Paragraph 2"),
                ParentNode("ul", [
                    LeafNode("li", "Bullet 1"),
                    LeafNode("li", "Bullet 2")
                ])
            ]),
            LeafNode("footer", "Copyright 2023")
        ])
        expected = "<section><header><h1>Title</h1></header><article><p>Paragraph 1</p><p>Paragraph 2</p><ul><li>Bullet 1</li><li>Bullet 2</li></ul></article><footer>Copyright 2023</footer></section>"
        self.assertEqual(node.to_html(), expected)

if __name__ == "__main__":
    unittest.main()