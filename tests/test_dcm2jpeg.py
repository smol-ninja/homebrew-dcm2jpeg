from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from dcm2jpeg import apply_windowing, convert_dcm_to_jpeg, main


class TestApplyWindowing:
    def test_normalizes_to_uint8_range(self) -> None:
        arr = np.array([[0, 50], [100, 200]], dtype=np.float64)
        ds = MagicMock(spec=[])
        result = apply_windowing(arr, ds)
        assert result.dtype == np.uint8
        assert result.min() == 0
        assert result.max() == 255

    def test_constant_image_returns_zeros(self) -> None:
        arr = np.full((10, 10), 42.0)
        ds = MagicMock(spec=[])
        result = apply_windowing(arr, ds)
        assert result.dtype == np.uint8
        assert np.all(result == 0)

    def test_applies_window_center_width(self) -> None:
        arr = np.array(
            [[0, 500], [1000, 2000]],
            dtype=np.float64,
        )
        ds = MagicMock()
        ds.WindowCenter = 500.0
        ds.WindowWidth = 1000.0
        result = apply_windowing(arr, ds)
        assert result.dtype == np.uint8
        assert result[0, 0] == 0
        assert result[0, 1] == 127
        assert result[1, 0] == 255
        assert result[1, 1] == 255

    def test_multivalue_window(self) -> None:
        arr = np.array(
            [[0, 100], [200, 300]],
            dtype=np.float64,
        )
        ds = MagicMock()
        ds.WindowCenter = [150.0, 200.0]
        ds.WindowWidth = [300.0, 100.0]
        result = apply_windowing(arr, ds)
        assert result.dtype == np.uint8


class TestConvertDcmToJpeg:
    def test_creates_jpeg_file(self, tmp_path: Path) -> None:
        ds = MagicMock()
        ds.pixel_array = np.random.randint(
            0,
            4096,
            (64, 64),
            dtype=np.int16,
        )
        ds.WindowCenter = 2048.0
        ds.WindowWidth = 4096.0

        dcm_path = tmp_path / "test.dcm"
        output_path = tmp_path / "test.jpeg"

        with patch("dcm2jpeg.pydicom.dcmread", return_value=ds):
            convert_dcm_to_jpeg(dcm_path, output_path)

        assert output_path.exists()
        assert output_path.stat().st_size > 0


class TestMain:
    def test_no_dcm_files(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        import sys

        sys.argv = ["dcm2jpeg", str(tmp_path)]
        main()
        captured = capsys.readouterr()
        assert "No .dcm files found" in captured.out

    def test_nonexistent_directory(self, tmp_path: Path) -> None:
        import sys

        sys.argv = ["dcm2jpeg", str(tmp_path / "nonexistent")]
        with pytest.raises(SystemExit):
            main()
