import unittest
import naive_search
import boyer_moore

class TestStringSearch(unittest.TestCase):
    def test_naive_search(self):
        self.assertEqual(naive_search.naive_search('abc', 'abc'), [0])
        self.assertEqual(naive_search.naive_search('abcabc', 'abc'), [0,3])
        self.assertEqual(naive_search.naive_search('abc', 'bc'), [1])
        self.assertEqual(naive_search.naive_search('abc', 'c'), [2])
        self.assertEqual(naive_search.naive_search('abc', 'x'), [])
    def test_boyer_moore(self):
        self.assertEqual(boyer_moore.boyer_moore_search('abc', 'abc'), [0])
        self.assertEqual(boyer_moore.boyer_moore_search('abcabc', 'abc'), [0,3])
        self.assertEqual(boyer_moore.boyer_moore_search('abc', 'bc'), [1])
        self.assertEqual(boyer_moore.boyer_moore_search('abc', 'c'), [2])
        self.assertEqual(boyer_moore.boyer_moore_search('abc', 'x'), [])
        self.assertEqual(boyer_moore.boyer_moore_search('abcabcbcbc', 'bc'), [1, 4, 6, 8])
        self.assertEqual(boyer_moore.boyer_moore_search('abcabcbbbbc', 'bbb'), [6, 7])
        self.assertEqual(boyer_moore.boyer_moore_search('abc', 'abcabc'), [])

if __name__ == '__main__':
    unittest.main()
