from ..wc import wc


def test_stdin_input(runner):
    """Test reading from stdin without files"""
    input_data = "Line 1\nLine 2\nLine 3\n"
    result = runner.invoke(wc, input=input_data)
    assert result.exit_code == 0
    assert result.output == "      3       6      21\n"


def test_single_file(runner, tmp_path):
    """Test processing single file"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Line 1\nLine 2\nLine 3\n")
    result = runner.invoke(wc, [str(test_file)])
    expected = f"      3       6      21 {test_file}\n"
    assert result.exit_code == 0
    assert result.output == expected


def test_multiple_files(runner, tmp_path):
    """Test processing multiple files with total"""
    file1 = tmp_path / "file1.txt"
    file1.write_text("A\nB\nC\n")
    file2 = tmp_path / "file2.txt"
    file2.write_text("Hello World\n")

    result = runner.invoke(wc, [str(file1), str(file2)])
    expected = (
        f"      3       3       6 {file1}\n"
        f"      1       2      12 {file2}\n"
        f"      4       5      18 total\n"
    )
    assert result.exit_code == 0
    assert result.output == expected


def test_nonexistent_file(runner):
    """Test handling non-existent file"""
    result = runner.invoke(wc, ["missing.txt"])
    assert result.exit_code == 0
    assert "wc: Cannot open 'missing.txt' for reading" in result.stderr
