"""
Tests for macos_photo_exporter module
"""
import os
import sys
from testing_constants import SRC_DIR
from testing_constants import TEST_DIR
from testing_constants import TEST_LIBRARY_NAME

sys.path.append(SRC_DIR)
import macos_photo_exporter  # pylint: disable=C0413 # noqa: E402


def test_export(tmp_path) -> None:
    """
    Tests that the export function can export a photo from a known photo library to a temp
    directory. The test will pass if the expected file is found in the temp directory.
    """
    # Test photo library location
    test_photo_library = os.path.join(TEST_DIR, TEST_LIBRARY_NAME)

    # Create a temporary test directory to contain the exported files
    temp_export_path = tmp_path / "photo_export_test"

    # Call export funtion
    macos_photo_exporter.export(temp_export_path, "2020-02-14", "2020-02-16", test_photo_library)

    # Expected test photo name and path
    test_photo = os.path.join(temp_export_path, "2020", "2020-02-14", "IMG_0051.jpeg")

    assert os.path.exists(test_photo)
