from pathlib import Path
import unittest
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"data"/"raw"; OUT=ROOT/"data"/"processed"
class TestMYOrchard(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=pd.read_csv(RAW/"seasons.csv"); cls.h=pd.read_csv(RAW/"harvest.csv")
  cls.x=pd.read_csv(RAW/"sales.csv"); cls.e=pd.read_csv(RAW/"expenses.csv")
  cls.k=pd.read_csv(OUT/"seasonal_kpis.csv")
 def test_15_seasons(self): self.assertEqual(len(self.s),15)
 def test_harvest_math(self): self.assertTrue((self.h.harvested_kg-self.h.rejected_kg==self.h.saleable_kg).all())
 def test_nonnegative_amounts(self): self.assertTrue((self.x.revenue>=0).all() and (self.e.amount>=0).all())
 def test_collection_bound(self): self.assertTrue((self.x.amount_collected<=self.x.revenue+.01).all())
 def test_kpi_season_count(self): self.assertEqual(len(self.k),15)
if __name__=="__main__": unittest.main()
