import RawMethods as rw
from moto import mock_dynamodb2
import unittest


@mock_dynamodb2
class TestUnit(unittest.TestCase):

    def test0_create_table(self):
        assert (rw.create_table() is not None)

    def test1_create_todo(self):
        todo = rw.create_todo()
        assert (todo.get('id') == rw.TODO_ID)
        assert (todo.get('text') == rw.TODO_TEXT)

    def test2_get_todo(self):
        todo = rw.get_todo()
        assert (todo.get('id') == rw.TODO_ID)
        assert (todo.get('text') == rw.TODO_TEXT)

    def test3_list_todo(self):
        todos = rw.list_todo()
        assert (len(todos) == 1)
        assert (todos[0].get('id') == rw.TODO_ID)
        assert (todos[0].get('text') == rw.TODO_TEXT)

    def test4_update_todo(self):
        todo = rw.update_todo()
        assert (todo.get('id') == rw.TODO_ID)
        assert (todo.get('text') == rw.TODO_NEW_TEXT)
        assert (todo.get('checked'))

    def test5_delete_todo(self):
        is_deleted = rw.delete_todo()
        assert is_deleted
        todos = rw.list_todo()
        assert (len(todos) == 0)

    def test6_delete_table(self):
        is_deleted = rw.delete_table()
        assert is_deleted


if __name__ == '__main__':
    unittest.main()
