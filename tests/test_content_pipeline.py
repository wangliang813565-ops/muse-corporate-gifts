"""Publishing guard checks in disposable fixtures, without production writes."""
import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("gift_content", REPO / "scripts/sync_content.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ContentGuards(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        builder.ROOT = self.root
        shutil.copytree(REPO / "data", self.root / "data")
        self.data = json.loads((self.root / "data/gift_knowledge.json").read_text(encoding="utf-8"))
        for article in self.data["articles"]:
            image = self.root / "static" / article["image"].lstrip("/")
            image.parent.mkdir(parents=True, exist_ok=True)
            image.write_bytes(b"fixture")

    def tearDown(self):
        self.temp.cleanup()

    def save(self):
        (self.root / "data/gift_knowledge.json").write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")

    def test_product_and_occasion_indexes_are_rebuilt(self):
        (self.root / "static/gift-guide.json").write_text('{"products": [], "occasions": []}', encoding="utf-8")
        builder.synchronise()
        result = json.loads((self.root / "static/gift-guide.json").read_text(encoding="utf-8"))
        self.assertEqual(result["products"], json.loads((self.root / "data/corporate_gifts_v2.json").read_text(encoding="utf-8"))["products"])
        self.assertEqual(len(result["occasions"]), 9)
        self.assertEqual(len(result["articles"]), len(self.data["articles"]))

    def test_same_theme_cannot_be_published_twice(self):
        extra = copy.deepcopy(self.data["articles"][-1])
        extra.update(id="another-id", slug="another-url", date="2026-10-15")
        self.data["articles"].append(extra)
        self.save()
        with self.assertRaisesRegex(AssertionError, "Duplicate buyer question"):
            builder.synchronise()

    def test_unknown_guide_route_cannot_publish_a_dead_end(self):
        self.data['guide_hub']['locales']['en']['routes'][0]['id'] = 'missing-guide'
        self.save()
        with self.assertRaisesRegex(AssertionError, 'existing guides'):
            builder.synchronise()

    def test_second_theme_on_same_dubai_day_is_rejected(self):
        extra = copy.deepcopy(self.data["articles"][-1])
        extra.update(id="another-id", slug="another-url", topic_key="another-question")
        self.data["articles"].append(extra)
        self.save()
        with self.assertRaisesRegex(AssertionError, "one new theme"):
            builder.synchronise()

    def test_future_publication_cannot_leak_into_machine_index(self):
        self.data["articles"][-1]["published_at"] = "2099-10-16T08:00:00+04:00"
        self.data["articles"][-1]["date"] = "2099-10-16"
        self.save()
        with self.assertRaisesRegex(AssertionError, "Future publication"):
            builder.synchronise()

    def test_renamed_slug_requires_review_of_old_page(self):
        builder.synchronise()
        self.data["articles"][-1]["slug"] = "new-slug"
        self.save()
        with self.assertRaisesRegex(ValueError, "Retired/renamed"):
            builder.synchronise()


if __name__ == "__main__":
    unittest.main()
