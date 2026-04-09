"""src/examples/ 내 모든 예제 파일이 에러 없이 실행되는지 검증하는 테스트."""

import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLES_DIR = Path(__file__).parent.parent / "src" / "examples"


def get_example_files():
    """examples 디렉터리에서 *_example.py 파일 목록을 동적으로 수집."""
    return sorted(EXAMPLES_DIR.glob("*_example.py"))


@pytest.mark.parametrize("example_file", get_example_files(), ids=lambda p: p.stem)
def test_example_runs_without_error(example_file: Path):
    """각 예제 파일을 서브프로세스로 실행하여 exit code 0인지 확인."""
    result = subprocess.run(
        [sys.executable, str(example_file)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"{example_file.name} 실행 실패\n"
        f"stderr:\n{result.stderr}"
    )
