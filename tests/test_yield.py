import unittest
import json
from app import app

class TestYieldPrediction(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_predict_yield(self):
        response = self.app.post('/yield-prediction', json={
            "crop": "Wheat",
            "state": "Punjab",
            "season": "Kharif",
            "area": 5,
            "rainfall": 800,
            "fertilizer": 50,
            "pesticide": 10
        })

        data = json.loads(response.data)
        self.assertIn("predicted_yield", data)

if __name__ == '__main__':
    unittest.main()
