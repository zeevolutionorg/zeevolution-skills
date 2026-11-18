"""Tests for scripts/check_leaks.py"""

import zipfile

import pytest
from helpers import load_script

cl = load_script("scripts/check_leaks.py")

pytestmark = pytest.mark.unit


def run(monkeypatch, *argv):
    monkeypatch.setattr("sys.argv", ["check_leaks.py", *map(str, argv)])
    cl.main()


# built at runtime so this file itself never contains a flagged domain or address
BAD_URL = "https:" + "//intranet.acme.io/x"
BAD_EMAIL = "me@" + "acme.io"


@pytest.fixture
def deny(tmp_path_factory):
    p = tmp_path_factory.mktemp("denylist") / "deny.txt"
    p.write_text("# comment\nacme corp\nzorblax\n", encoding="utf-8")
    return p


class TestDenylistLoading:
    def test_file_argument(self, deny):
        assert cl.load_denylist(str(deny)) == ["acme corp", "zorblax"]

    def test_env_file(self, deny, monkeypatch):
        monkeypatch.setenv("LEAK_DENYLIST_FILE", str(deny))
        assert cl.load_denylist(None) == ["acme corp", "zorblax"]

    def test_env_inline_secret(self, monkeypatch):
        monkeypatch.delenv("LEAK_DENYLIST_FILE", raising=False)
        monkeypatch.setenv("LEAK_DENYLIST", "Foo\n\nBar")
        assert cl.load_denylist(None) == ["foo", "bar"]

    def test_home_file(self, tmp_path, monkeypatch):
        monkeypatch.delenv("LEAK_DENYLIST_FILE", raising=False)
        monkeypatch.delenv("LEAK_DENYLIST", raising=False)
        monkeypatch.setattr(cl.Path, "home", lambda: tmp_path)
        assert cl.load_denylist(None) is None
        (tmp_path / ".config" / "zeevolution").mkdir(parents=True)
        (tmp_path / ".config" / "zeevolution" / "denylist.txt").write_text("x\n", encoding="utf-8")
        assert cl.load_denylist(None) == ["x"]


class TestCheckText:
    def check(self, text, deny=("zorblax",)):
        problems = []
        cl.check_text("f", text, list(deny), problems)
        return problems

    def test_whole_word_only(self):
        assert self.check("zorblaxing review") == []
        assert self.check("the Zorblax cycle")

    def test_unknown_domains_flagged(self):
        assert self.check("see " + BAD_URL)
        assert self.check("see https://github.com/x") == []

    def test_emails(self):
        assert self.check(BAD_EMAIL)
        assert self.check("zeevolution@users.noreply.github.com") == []


class TestMain:
    def test_clean_tree_passes(self, tmp_path, deny, monkeypatch, capsys):
        (tmp_path / "a.md").write_text("hello", encoding="utf-8")
        run(monkeypatch, "--denylist", deny, tmp_path)
        assert "leak check ok" in capsys.readouterr().out

    def test_denylisted_term_fails(self, tmp_path, deny, monkeypatch):
        (tmp_path / "a.md").write_text("Welcome to ACME Corp", encoding="utf-8")
        with pytest.raises(SystemExit):
            run(monkeypatch, "--denylist", deny, tmp_path)

    def test_office_metadata_fails(self, tmp_path, deny, monkeypatch):
        with zipfile.ZipFile(tmp_path / "d.docx", "w") as z:
            z.writestr("docProps/core.xml", "<cp:coreProperties><dc:creator>Jane Doe</dc:creator></cp:coreProperties>")
            z.writestr("docProps/app.xml", "<Properties><Company>Acme</Company></Properties>")
        with pytest.raises(SystemExit):
            run(monkeypatch, "--denylist", deny, tmp_path)

    def test_office_neutral_metadata_passes(self, tmp_path, deny, monkeypatch):
        with zipfile.ZipFile(tmp_path / "d.xlsx", "w") as z:
            z.writestr("docProps/core.xml", "<x><dc:creator>zeevolution-skills</dc:creator></x>")
        run(monkeypatch, "--denylist", deny, tmp_path)

    def test_pdf_author_fails(self, tmp_path, deny, monkeypatch):
        (tmp_path / "a.pdf").write_bytes(b"%PDF-1.4 /Author (Jane Doe) ")
        with pytest.raises(SystemExit):
            run(monkeypatch, "--denylist", deny, tmp_path)

    def test_image_exif_fails(self, tmp_path, deny, monkeypatch):
        from PIL import Image

        img = Image.new("RGB", (4, 4))
        exif = Image.Exif()
        exif[0x013B] = "Jane Doe"  # Artist
        img.save(tmp_path / "s.jpg", exif=exif)
        with pytest.raises(SystemExit):
            run(monkeypatch, "--denylist", deny, tmp_path)

    def test_repository_is_clean(self, root, monkeypatch, capsys):
        """The real repo must pass the URL / email / metadata checks (denylist runs in CI)."""
        monkeypatch.delenv("LEAK_DENYLIST", raising=False)
        monkeypatch.delenv("LEAK_DENYLIST_FILE", raising=False)
        run(monkeypatch, root)
        assert "leak check ok" in capsys.readouterr().out
