"""打包离线教材，检查本地链接并核对 ZIP 内容；不包含运行输出和 QA 文件。"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import json
import os
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT.parent / "Python-Zero-to-Practice.zip"
EXCLUDED = {"qa", "__pycache__", ".git", ".venv", "venv", "node_modules", "outputs", "personal", ".idea", ".vscode"}


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get("id"):
            self.ids.add(data["id"])
        for key in ("href", "src"):
            if data.get(key):
                self.links.append(data[key])


def distribution_files(root=ROOT):
    """供离线打包与原网站打包共用的分发文件规则。"""
    return sorted(
        p for p in root.rglob("*")
        if p.is_file() and not set(p.relative_to(root).parts) & EXCLUDED
        and p.name != ".DS_Store" and p.suffix not in {".pyc", ".zip", ".pem", ".key"}
        and p.name != ".env" and not p.name.startswith(".env.")
        and not ("progress" in p.name and p.suffix == ".json")
    )


def main():
    parser = Links()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    files = distribution_files()
    relative = {p.relative_to(ROOT).as_posix() for p in files}
    for href in parser.links:
        url = urlsplit(href)
        if url.scheme or url.netloc:
            continue
        if not url.path:
            if url.fragment:
                assert unquote(url.fragment) in parser.ids, f"无效章节链接：{href}"
        else:
            assert unquote(url.path) in relative, f"链接目标未打包：{href}"
    temporary = ARCHIVE.with_suffix(".tmp.zip")
    try:
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                archive.write(path, ROOT.name + "/" + path.relative_to(ROOT).as_posix())
        with zipfile.ZipFile(temporary) as archive:
            assert archive.testzip() is None
            assert len(archive.namelist()) == len(files)
            for path in files:
                assert archive.read(ROOT.name + "/" + path.relative_to(ROOT).as_posix()) == path.read_bytes()
        os.replace(temporary, ARCHIVE)
    finally:
        if temporary.exists():
            temporary.unlink()
    report = {
        "archive": str(ARCHIVE), "files": len(files),
        "bytes": ARCHIVE.stat().st_size,
        "sha256": hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
        "all_links_valid": True, "all_members_byte_matched": True,
    }
    (ROOT / "qa").mkdir(exist_ok=True)
    (ROOT / "qa/package-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
