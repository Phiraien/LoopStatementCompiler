"""Safe subprocess integration for the existing C compiler."""
from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import tempfile
import time
from typing import Any, Optional


class CompilerNotFound(RuntimeError):
    """Raised when loopcc has not been built or cannot be located."""


@dataclass
class ProcessResult:
    returncode: int
    stdout: str
    stderr: str
    elapsed_ms: int
    ast: Optional[dict[str, Any]] = None


class CompilerRunner:
    def __init__(self, project_root: Optional[Path] = None) -> None:
        self.project_root = (project_root or Path(__file__).resolve().parents[1]).resolve()

    def find_compiler(self) -> Path:
        names = ("loopcc.exe", "loopcc") if os.name == "nt" else ("loopcc", "loopcc.exe")
        candidates = [self.project_root / name for name in names]
        candidates += [self.project_root / "build" / name for name in names]
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        raise CompilerNotFound(
            "Compiler executable not found. Build it first with 'make' in the "
            "project directory (MSYS2 UCRT64 or WSL on Windows)."
        )

    def compile_file(self, source_path: Path, timeout: float = 10.0) -> ProcessResult:
        compiler = self.find_compiler()
        command = [str(compiler), "-j", str(source_path)]
        started = time.perf_counter()
        try:
            completed = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            elapsed = int((time.perf_counter() - started) * 1000)
            return ProcessResult(
                returncode=124,
                stdout=exc.stdout or "",
                stderr=f"Compiler timed out after {timeout:g} seconds.\n",
                elapsed_ms=elapsed,
            )
        elapsed = int((time.perf_counter() - started) * 1000)
        ast = None
        if completed.returncode == 0:
            try:
                ast = json.loads(completed.stdout)
            except json.JSONDecodeError as exc:
                return ProcessResult(
                    returncode=125,
                    stdout=completed.stdout,
                    stderr=f"Compiler returned invalid AST JSON: {exc}\n",
                    elapsed_ms=elapsed,
                )
        return ProcessResult(
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            elapsed_ms=elapsed,
            ast=ast,
        )

    def compile_text(
        self, source: str, source_path: Optional[Path] = None, timeout: float = 10.0
    ) -> ProcessResult:
        temporary_path: Optional[Path] = None
        try:
            if source_path is None:
                handle = tempfile.NamedTemporaryFile(
                    mode="w", suffix=".c", prefix="loopcc_gui_", delete=False,
                    encoding="utf-8", newline="\n",
                )
                with handle:
                    handle.write(source)
                temporary_path = Path(handle.name)
                source_path = temporary_path
            else:
                source_path = Path(source_path)
            return self.compile_file(source_path, timeout=timeout)
        except CompilerNotFound:
            raise
        finally:
            if temporary_path is not None:
                try:
                    temporary_path.unlink()
                except OSError:
                    pass

    def run_tests(self, timeout: float = 30.0) -> ProcessResult:
        script = self.project_root / "tests" / "run_tests.sh"
        if os.name == "nt":
            # Prefer MSYS2 over WSL's bash. WSL bash cannot consume a native
            # C:\\... path directly and produces the mangled path seen by users.
            bash_candidates = [
                os.environ.get("MSYS2_BASH"),
                r"C:\msys64\usr\bin\bash.exe",
                r"C:\msys64\usr\bin\sh.exe",
                shutil.which("bash"),
            ]
        else:
            bash_candidates = [shutil.which("bash")]
        bash = next((item for item in bash_candidates if item and Path(item).exists()), None)
        if not bash:
            return ProcessResult(
                returncode=127,
                stdout="",
                stderr="Bash was not found. Run tests from MSYS2 UCRT64 or configure MSYS2_BASH.\n",
                elapsed_ms=0,
            )

        script_argument = str(script)
        if os.name == "nt" and "msys" in bash.lower():
            drive = script.drive[:1].lower()
            script_argument = f"/{drive}{script.as_posix()[2:]}"

        started = time.perf_counter()
        try:
            if os.name == "nt" and "msys" in bash.lower():
                command = [
                    bash, "-lc",
                    "export PATH=/ucrt64/bin:/usr/bin:$PATH; bash " + shlex.quote(script_argument),
                ]
            else:
                command = [bash, script_argument]
            completed = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            elapsed = int((time.perf_counter() - started) * 1000)
            return ProcessResult(124, "", f"Tests timed out after {timeout:g} seconds.\n", elapsed)
        elapsed = int((time.perf_counter() - started) * 1000)
        return ProcessResult(completed.returncode, completed.stdout, completed.stderr, elapsed)
