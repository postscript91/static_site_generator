from textnode import TextNode, TextType

def main():
    node1 = TextNode("Hello world", TextType.TEXT)
    node2 = TextNode("Click here", TextType.LINK, "https://example.com")
    print(node1, node2)

if __name__ == "__main__":
    main()