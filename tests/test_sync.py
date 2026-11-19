from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class SyncTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.template = self.root / "template"
        self.template.mkdir()
        repo = Path(__file__).resolve().parents[1]
        for name in ("install.sh", "update.sh", "sync.py"):
            shutil.copy(repo / name, self.template / name)
        self.skill = Path(".pi/skills/plan-feature/SKILL.md")
        self.agent = Path(".pi/agents/builder.md")
        self.prompt = Path(".pi/prompts/implement.md")
        self.project_files = (Path("AGENTS.md"), Path("architecture.md"), Path(".pi/settings.json"))
        for relative in (self.agent, self.prompt, self.skill, *self.project_files):
            (self.template / relative).parent.mkdir(parents=True, exist_ok=True)
            (self.template / relative).write_text("original")

    def run_script(self, name, *args, status=0):
        run = subprocess.run([self.template / name, *args], cwd=self.root,
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, status, run.stdout + run.stderr)
        return run.stderr

    def project(self, name):
        path = self.root / name
        path.mkdir()
        return path

    def test_adopts_existing_copies_and_updates_all_without_losing_edits(self):
        experiment = self.project("experiment project")
        other = self.project("other")
        (experiment / self.skill).parent.mkdir(parents=True)
        (experiment / self.skill).write_text("original")
        self.run_script("install.sh", experiment.name)
        self.run_script("install.sh", other)

        (experiment / self.skill).write_text("experiment")
        shutil.copyfile(experiment / self.skill, self.template / self.skill)
        (other / self.agent).unlink()
        (other / self.skill).write_text("different experiment")
        (self.template / self.prompt).write_text("new prompt")
        report = self.run_script("update.sh", status=1)
        self.assertIn(str(other / self.agent), report)
        self.assertIn(str(other / self.skill), report)
        self.assertEqual((experiment / self.prompt).read_text(), "new prompt")
        self.assertEqual((other / self.prompt).read_text(), "new prompt")
        self.assertEqual((other / self.skill).read_text(), "different experiment")
        self.assertFalse((other / self.agent).exists())

        self.run_script("update.sh", "--overwrite", "--all")
        self.assertEqual((other / self.skill).read_text(), "experiment")
        self.assertEqual((other / self.agent).read_text(), "original")
        self.run_script("update.sh")

    def test_default_leaves_project_files_alone_and_overwrite_targets_selected_files(self):
        project = self.project("existing")
        self.run_script("install.sh", project)
        for relative in self.project_files:
            (self.template / relative).write_text("new template")
        (project / "AGENTS.md").write_text("local instructions")
        self.run_script("update.sh")
        self.assertEqual((project / "AGENTS.md").read_text(), "local instructions")
        self.assertEqual((project / "architecture.md").read_text(), "original")
        self.assertEqual((project / ".pi/settings.json").read_text(), "original")

        (self.template / self.skill).write_text("new skill")
        self.run_script("update.sh", "--overwrite", "AGENTS.md", ".pi/settings.json")
        self.assertEqual((project / "AGENTS.md").read_text(), "new template")
        self.assertEqual((project / ".pi/settings.json").read_text(), "new template")
        self.assertEqual((project / "architecture.md").read_text(), "original")
        self.assertEqual((project / self.skill).read_text(), "original")

        self.run_script("update.sh", "--overwrite", "--all")
        self.assertEqual((project / "architecture.md").read_text(), "new template")
        self.assertEqual((project / self.skill).read_text(), "new skill")

    def test_overwrite_rejects_invalid_file_scope(self):
        project = self.project("existing")
        self.run_script("install.sh", project)
        (self.template / "AGENTS.md").write_text("new template")
        for args in (("--all",), ("--overwrite", "AGENTS.md", "--all")):
            self.run_script("update.sh", *args, status=2)
        report = self.run_script("update.sh", "--overwrite", "AGENTS.md", "README.md", status=1)
        self.assertIn("README.md", report)
        self.assertEqual((project / "AGENTS.md").read_text(), "original")

    def test_named_overwrite_can_target_pi_files_one_file_or_all_files(self):
        plugins, glowkin, other = (self.project(name) for name in ("plugins", "glowkin", "other"))
        for project in (plugins, glowkin, other):
            self.run_script("install.sh", project)
            for relative in (self.skill, *self.project_files):
                (project / relative).write_text("local")

        self.run_script("update.sh", "--name", "glowkin", "--overwrite")
        self.assertEqual((glowkin / self.skill).read_text(), "original")
        self.assertEqual((glowkin / ".pi/settings.json").read_text(), "original")
        self.assertEqual((glowkin / "AGENTS.md").read_text(), "local")
        self.assertEqual((glowkin / "architecture.md").read_text(), "local")
        self.assertEqual((plugins / self.skill).read_text(), "local")

        self.run_script("update.sh", "--overwrite", "AGENTS.md", "--name", "plugins")
        self.assertEqual((plugins / "AGENTS.md").read_text(), "original")
        self.assertEqual((plugins / self.skill).read_text(), "local")

        self.run_script("update.sh", "--name", "plugins,glowkin", "--overwrite", "--all")
        for relative in (self.skill, *self.project_files):
            self.assertEqual((plugins / relative).read_text(), "original")
            self.assertEqual((glowkin / relative).read_text(), "original")
            self.assertEqual((other / relative).read_text(), "local")

    def test_rejects_unknown_or_ambiguous_names_before_syncing(self):
        glowkin = self.project("glowkin")
        first = glowkin / "plugins"
        second = self.project("plugins")
        first.mkdir()
        for project in (glowkin, first, second):
            self.run_script("install.sh", project)
        (self.template / self.skill).write_text("new skill")

        for name, message in (("unknown", "No registered project"), ("plugins", "Ambiguous project")):
            report = self.run_script("update.sh", "--name", f"glowkin,{name}", status=1)
            self.assertIn(message, report)
            self.assertEqual((glowkin / self.skill).read_text(), "original")

    def test_registers_conflicting_existing_files_without_replacing_them(self):
        project = self.project("existing")
        local = project / "AGENTS.md"
        local.write_text("custom instructions")
        (project / "unrelated.txt").write_text("keep")
        self.assertIn(str(local), self.run_script("install.sh", project, status=1))
        self.assertEqual(local.read_text(), "custom instructions")
        self.assertTrue((project / self.skill).is_file())

        (self.template / self.skill).unlink()
        self.run_script("update.sh", "--overwrite", "--all")
        self.assertEqual(local.read_text(), "original")
        self.assertTrue((project / self.skill).is_file())
        self.assertEqual((project / "unrelated.txt").read_text(), "keep")

    def test_missing_project_and_symlink_do_not_block_other_projects(self):
        moved = self.project("moved")
        linked = self.project("linked")
        clean = self.project("clean")
        for project in (moved, linked, clean):
            self.run_script("install.sh", project)
        moved.rename(self.root / "new name")
        external = self.project("external")
        (linked / ".pi").rename(linked / "saved")
        (linked / ".pi").symlink_to(external, target_is_directory=True)
        (self.template / self.skill).write_text("changed")
        report = self.run_script("update.sh", "--overwrite", "--all", status=1)
        self.assertIn(str(moved), report)
        self.assertIn(str(linked / self.skill), report)
        self.assertEqual(list(external.iterdir()), [])
        self.assertEqual((clean / self.skill).read_text(), "changed")


if __name__ == "__main__":
    unittest.main()
