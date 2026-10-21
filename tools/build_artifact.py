"""Build the single-file Claude artifact version of the exam from this repo.

Usage:  python tools/build_artifact.py <output.html>

The artifact host wraps the page in its own <!doctype>/<head>/<body>, so this
drops the static-only head block, unwraps the document, and inlines both
scripts (escaping non-ASCII characters so the encoding never matters).
"""
import pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
out = pathlib.Path(sys.argv[1])

page = (root / "index.html").read_text(encoding="utf-8")
page = re.sub(r"<!-- static-only.*?<!-- /static-only -->\s*", "", page, flags=re.S)
head = re.search(r"<head>(.*)</head>", page, re.S).group(1).strip()
body = re.search(r"<body>(.*)</body>", page, re.S).group(1).strip()


def ascii_js(text):
    def esc(c):
        o = ord(c)
        if o < 128:
            return c
        if o < 0x10000:
            return "\\u%04x" % o
        o -= 0x10000
        return "\\u%04x\\u%04x" % (0xD800 + (o >> 10), 0xDC00 + (o & 0x3FF))
    return "".join(esc(c) for c in text)


for name in ("exam-key.js", "app.js"):
    js = ascii_js((root / name).read_text(encoding="utf-8"))
    assert "</script" not in js.lower()
    tag = f'<script src="{name}" charset="utf-8"></script>'
    assert tag in body, tag
    body = body.replace(tag, "<script>\n" + js + "\n</script>")

out.write_text(head + "\n" + body + "\n", encoding="utf-8")
print("artifact page written to", out)
