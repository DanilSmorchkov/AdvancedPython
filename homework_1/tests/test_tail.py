from ..tail import tail


def test_stdin_no_files(runner):
    input_text = "\n".join(str(i) for i in range(20)) + "\n"
    result = runner.invoke(tail, input=input_text)
    expected = "\n".join(str(i) for i in range(3, 20)) + "\n"
    assert result.output == expected


def test_single_file(runner, tmpdir):
    test_file = tmpdir.join("test.txt")
    content = "\n".join(f"Line {i}" for i in range(15)) + "\n"
    test_file.write(content)
    result = runner.invoke(tail, [str(test_file)])
    expected = "\n".join(f"Line {i}" for i in range(5, 15)) + "\n"
    assert expected in result.output
    assert "==>" not in result.output


def test_multiple_files(runner, tmpdir):
    file1 = tmpdir.join("file1.txt")
    file1.write("\n".join(f"File1 {i}" for i in range(12)) + "\n")

    file2 = tmpdir.join("file2.txt")
    file2.write("\n".join(f"File2 {i}" for i in range(8)) + "\n")

    result = runner.invoke(tail, [str(file1), str(file2)])
    assert f"==> {file1} <==" in result.output
    assert "File1 11" in result.output
    assert f"==> {file2} <==" in result.output
    assert "File2 7" in result.output


def test_nonexistent_file(runner):
    result = runner.invoke(tail, ["non_existent_file.txt"])
    assert "Cannot open 'non_existent_file.txt'" in result.stderr
    assert result.exit_code == 0


def test_mixed_input(runner, tmpdir):
    valid_file = tmpdir.join("valid.txt")
    valid_file.write("Valid content\n")
    result = runner.invoke(tail, [str(valid_file), "bad_file.txt"])
    assert "Valid content" in result.output
    assert "bad_file.txt" in result.stderr
