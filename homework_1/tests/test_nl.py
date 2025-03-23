from ..nl import number_lines


def test_file_input(runner, tmp_path):
    """Test numbering lines from a file input"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Line 1\nLine 2\nLine 3\n")

    result = runner.invoke(number_lines, [str(test_file), "-b", "a"])

    assert result.exit_code == 0
    assert result.output == (
        "     1\tLine 1\n"  # noqa: E501
        "     2\tLine 2\n"  # noqa: E501
        "     3\tLine 3\n"  # noqa: E501
    )


def test_stdin_input(runner):
    """Test numbering lines from stdin input"""
    input_data = "First line\nSecond line\nThird line\n"
    result = runner.invoke(number_lines, ["-b", "a"], input=input_data)

    assert result.exit_code == 0
    assert result.output == (
        "     1\tFirst line\n"  # noqa: E501
        "     2\tSecond line\n"  # noqa: E501
        "     3\tThird line\n"  # noqa: E501
    )


def test_file_not_found(runner):
    """Test handling of non-existent file"""
    result = runner.invoke(number_lines, ["non_existent_file.txt"])

    assert result.exit_code == 1
    assert "Cannot open 'non_existent_file.txt'" in result.stderr


def test_flag_b_a(runner):
    """Test -b a option (number all lines)"""
    input_data = "Line 1\n\nLine 3\n"
    result = runner.invoke(number_lines, ["-b", "a"], input=input_data)

    assert result.exit_code == 0
    assert result.output == (
        "     1\tLine 1\n"  # noqa: E501
        "     2\t\n"  # noqa: E501
        "     3\tLine 3\n"  # noqa: E501
    )


def test_flag_b_t(runner):
    """Test -b t option (number non-empty lines only)"""
    input_data = "Line 1\n\nLine 3\n"
    result = runner.invoke(number_lines, ["-b", "t"], input=input_data)

    assert result.exit_code == 0
    assert result.output == (
        "     1\tLine 1\n"  # noqa: E501
        "      \t\n"  # noqa: E501
        "     2\tLine 3\n"  # noqa: E501
    )


def test_flag_b_n(runner):
    """Test -b n option (no numbering)"""
    input_data = "Line 1\n\nLine 3\n"
    result = runner.invoke(number_lines, ["-b", "n"], input=input_data)

    assert result.exit_code == 0
    assert result.output == (
        "      \tLine 1\n"  # noqa: E501
        "      \t\n"  # noqa: E501
        "      \tLine 3\n"  # noqa: E501
    )
