from src.reader import PhrasesReader, ListReader


def test_reader_single_instance():
    phrases_reader = PhrasesReader()
    phrases_reader2 = PhrasesReader()

    assert id(phrases_reader) == id(phrases_reader2)

    list_reader = ListReader()
    list_reader2 = ListReader()

    assert id(list_reader) == id(list_reader2)


def test_throw_exception():
    reader = PhrasesReader()
    reader.FILE_PATH = "test/test.txt"
    reader.data = None
    try:
        reader.read_data()
        assert False
    except FileNotFoundError:
        assert True
