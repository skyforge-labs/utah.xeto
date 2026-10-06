"""Regression checks for compiler errors that may return exit status zero."""
import importlib.util
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("utah_build", Path(__file__).parents[1] / "scripts/build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class CompilerFailures(unittest.TestCase):
    @patch.object(build.shutil, "which", return_value="java")
    @patch.object(build.subprocess, "run")
    def test_error_with_zero_exit_is_rejected(self, run, which):
        run.return_value = subprocess.CompletedProcess([], 0, "❌ ERROR: could not compile utah.ahu\n")
        with self.assertRaises(RuntimeError):
            build.run_xeto(Path("runtime"), Path("work"), "build", "utah.ahu")

    @patch.object(build.shutil, "which", return_value="java")
    @patch.object(build.subprocess, "run")
    def test_runtime_boot_failure_is_rejected(self, run, which):
        run.return_value = subprocess.CompletedProcess([], 1, "Cannot boot\n")
        with self.assertRaises(RuntimeError):
            build.run_xeto(Path("runtime"), Path("work"), "dump", "utah")
