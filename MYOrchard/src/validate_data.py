from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parents[1]/"data"/"raw"
def main():
 s=pd.read_csv(R/"seasons.csv"); b=pd.read_csv(R/"buyers.csv"); v=pd.read_csv(R/"varieties.csv")
 h=pd.read_csv(R/"harvest.csv"); x=pd.read_csv(R/"sales.csv"); e=pd.read_csv(R/"expenses.csv")
 assert len(s)==15 and s.season_id.is_unique
 assert b.buyer_id.is_unique and v.variety_id.is_unique
 assert h.harvest_id.is_unique and x.invoice_line_id.is_unique and e.expense_id.is_unique
 assert (h.harvested_kg-h.rejected_kg==h.saleable_kg).all()
 assert (x.quantity_kg>0).all() and (x.revenue>=0).all()
 assert (x.amount_collected<=x.revenue+.01).all() and (e.amount>=0).all()
 assert set(x.season_id)<=set(s.season_id) and set(x.buyer_id)<=set(b.buyer_id) and set(x.variety_id)<=set(v.variety_id)
 # Each variety's sold amount must not exceed its season's saleable harvest.
 sold=x.groupby(["season_id","variety_id"]).quantity_kg.sum()
 avail=h.groupby(["season_id","variety_id"]).saleable_kg.sum()
 assert (sold<=avail).all()
 print("PASS: all MYOrchard integrity checks completed.")
if __name__=="__main__": main()
