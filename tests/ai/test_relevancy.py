import unittest
from src.ai.relevancy import get_facts
from src.models.tweet import Tweet, TweetMetadata

class TestRelevancy(unittest.TestCase):

    def test_no_facts_for_irrelevant_tweet(self):
        tweet = Tweet(content="This is a random tweet.", metadata=TweetMetadata())
        facts = get_facts(tweet)
        self.assertEqual(facts, [])

    def test_single_fact_condition(self):
        tweet = Tweet(content="The market is bullish today!", metadata=TweetMetadata())
        facts = get_facts(tweet)
        # Expect the bullish fact
        self.assertIn("Market is strong with positive trends", facts)

    def test_multiple_facts_conditions(self):
        tweet = Tweet(content="I feel bearish and crypto markets are volatile.", metadata=TweetMetadata())
        facts = get_facts(tweet)
        # Expect both bearish and crypto facts
        self.assertIn("The cryptocurrency market has shown downward trends recently", facts)
        self.assertIn("Blockchain adoption continues to grow", facts)

if __name__ == '__main__':
    unittest.main() 