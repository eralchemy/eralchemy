"""Forum like example.

Code credits go to NewsMeme (https://github.com/danjac/newsmeme)
"""

from forum import Base

if __name__ == "__main__":
    from eralchemy import render_er

    render_er(Base, "forum_mermaid.md", mode="mermaid")
    render_er(Base, "forum_mermaid_er.md", mode="mermaid_er")
    render_er(Base, "forum_mermaid_plain.md", mode="mermaid_plain")
    render_er(
        Base, "forum_mermaid_plain_with_title.md", mode="mermaid_plain", title="Forum ER Diagram"
    )
