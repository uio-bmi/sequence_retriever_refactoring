import unittest
from sequence_retriever import fetch_sequence_from_web_service

class SequenceRetrieverTester(unittest.TestCase):

    def setUp(self):
        self.valid_sources = ["UCSC", "TOGOWS"]

    def test_fetching_from_invalid_source_raises_exception(self):
        self.assertRaises(
            NotImplementedError,
            fetch_sequence_from_web_service,
            "invalid_test_source", "chr1", 1, 10
        )

    def test_fetching_from_invalid_start_raises_exception(self):
        for source in self.valid_sources:
            self.assertRaises(
                Exception,
                fetch_sequence_from_web_service,
                source, "chr1", -1, 10
            )

    def test_fetching_from_invalid_end_raises_excecption(self):
        for source in self.valid_sources:
            self.assertRaises(
                Exception,
                fetch_sequence_from_web_service,
                source, "chr1", 1, -1
            )

    def test_fetched_sequence_is_correct(self):

        for source in self.valid_sources:
            sequence = fetch_sequence_from_web_service(source, "chr2", 10000000, 10000005)
            self.assertEqual(sequence, "ttaga",
                             "Fetched sequence from %s does not match"
                             "correct sequence" % source)

            sequence = fetch_sequence_from_web_service(source, "chr5", 2895722, 2895728)
            self.assertEqual(sequence, "atggat",
                             "Fetched sequence from %s does not match"
                             "correct sequence" % source)



if __name__ == "__main__":
    unittest.main()