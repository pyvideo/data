from clive.lib import load_json_data


class TestLoadJsonFiles:
    def test_bad_paths(self):
        assert load_json_data(None) == []
        assert load_json_data('') == []
        assert load_json_data('/nonexistent/file') == []

    def test_non_json_file(self, tmpdir):
        path = tmpdir.join('foo.txt')
        path.write('test file')

        assert load_json_data(tmpdir.strpath) == []
        assert load_json_data(path.strpath) == []

    def test_json_file(self, tmpdir):
        path = tmpdir.join('foo.json')
        path.write('{}')

        assert load_json_data(tmpdir.strpath) == [(path.strpath, {})]
        assert load_json_data(path.strpath) == [(path.strpath, {})]

    def test_directory(self, tmpdir):
        cat_path = tmpdir.join('pycon').mkdir()

        path1 = cat_path.join('foo1.json')
        path1.write('{}')
        path2 = cat_path.join('foo2.json')
        path2.write('{}')

        path3 = tmpdir.join('djangocon').mkdir().join('foo3.json')
        path3.write('{}')

        assert (
            load_json_data(tmpdir.strpath) ==
            [
                # Note: djangocon comes first because it's sorted
                (path3.strpath, {}),

                (path1.strpath, {}),
                (path2.strpath, {}),
            ]
        )
