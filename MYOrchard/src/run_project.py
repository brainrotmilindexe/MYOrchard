from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"data"/"raw"; OUT=ROOT/"data"/"processed"
SEED=20261024

def save(df,path):
    path.parent.mkdir(parents=True,exist_ok=True); df.to_csv(path,index=False)

def main():
    rng=np.random.default_rng(SEED); RAW.mkdir(parents=True,exist_ok=True); OUT.mkdir(parents=True,exist_ok=True)
    seasons=pd.DataFrame([{"season_id":f"S{y}","season":f"{y}-{str(y+1)[-2:]}","start_year":y,
      "pandemic_scenario":y in (2019,2020),"market_pressure_scenario":y in (2022,2023),
      "scenario_note":"Synthetic pandemic scenario" if y in (2019,2020) else "Synthetic cost/market scenario" if y in (2022,2023) else "Baseline synthetic season"} for y in range(2011,2026)])
    varieties=pd.DataFrame([["V01","Alphonso",.20,78],["V02","Banganapalli",.28,48],["V03","Kesar",.18,62],["V04","Totapuri",.22,32],["V05","Dasheri",.12,42]],columns=["variety_id","variety","acre_share","base_price_per_kg"])
    blocks=pd.DataFrame([["B01","North Block",5],["B02","South Block",5],["B03","East Block",4],["B04","West Block",5],["B05","Central Block",5]],columns=["block_id","block_name","acres"])
    buyers=pd.DataFrame([["C001","Deccan Fresh Traders","Distributor","Hyderabad"],["C002","Green Basket Wholesale","Wholesaler","Secunderabad"],["C003","Metro Fruit Supply","Distributor","Bengaluru"],["C004","Sunrise Produce Market","Market Agent","Pune"],["C005","Harvest Lane Foods","Retail Supplier","Hyderabad"],["C006","Crown Agro Links","Wholesaler","Chennai"],["C007","FreshRoute Commerce","Distributor","Mumbai"],["C008","Village-to-City Foods","Retail Supplier","Warangal"]],columns=["buyer_id","buyer_name","buyer_type","market"])
    for name,df in [("seasons",seasons),("varieties",varieties),("orchard_blocks",blocks),("buyers",buyers)]: save(df,RAW/f"{name}.csv")
    hr=[]
    for s in seasons.itertuples():
      factor=rng.normal(1,.10)*(0.96 if s.pandemic_scenario else 1)*(0.88 if s.start_year in (2015,2018,2023) else 1)
      for b in blocks.itertuples():
       for v in varieties.itertuples():
        acres=b.acres*v.acre_share; kg=max(250,int(acres*rng.normal(3200,280)*factor)); rej=int(kg*np.clip(rng.normal(.055,.018),.015,.13))
        hr.append([f"H-{s.start_year}-{b.block_id}-{v.variety_id}",s.season_id,b.block_id,v.variety_id,round(acres,2),kg,rej,kg-rej])
    harvest=pd.DataFrame(hr,columns=["harvest_id","season_id","block_id","variety_id","acres_allocated","harvested_kg","rejected_kg","saleable_kg"]); save(harvest,RAW/"harvest.csv")
    weights=np.array([.19,.16,.15,.13,.12,.10,.09,.06]); weights/=weights.sum(); sr=[]; counter=1
    for s in seasons.itertuples():
     for v in varieties.itertuples():
      available=int(harvest[(harvest.season_id==s.season_id)&(harvest.variety_id==v.variety_id)].saleable_kg.sum())
      remaining=int(available*np.clip(rng.normal(.80,.055),.65,.92)); n=0
      while remaining>0 and n<8:
       qty=min(remaining,int(rng.integers(350,1500))); remaining-=qty; n+=1
       buyer=buyers.iloc[int(rng.choice(len(buyers),p=weights))]; month=int(rng.choice([4,5,6],p=[.25,.5,.25])); day=int(rng.integers(1,29))
       price=round(max(15,v.base_price_per_kg*(1+.035*(s.start_year-2011))*rng.normal(1,.075)*(0.97 if s.market_pressure_scenario else 1)*(0.96 if s.pandemic_scenario else 1)),2)
       gross=qty*price; disc=round(gross*rng.choice([0,.01,.02,.03],p=[.68,.16,.11,.05]),2); rev=round(gross-disc,2)
       status=rng.choice(["Paid","Part-paid","Outstanding"],p=[.76,.14,.10]); collected=rev if status=="Paid" else round(rev*rng.uniform(.25,.75),2) if status=="Part-paid" else 0
       sr.append([f"INV{counter:06d}",f"{s.start_year}-{month:02d}-{day:02d}",s.season_id,buyer.buyer_id,v.variety_id,qty,price,disc,rev,collected,status]); counter+=1
    sales=pd.DataFrame(sr,columns=["invoice_line_id","invoice_date","season_id","buyer_id","variety_id","quantity_kg","price_per_kg","discount_amount","revenue","amount_collected","payment_status"]); save(sales,RAW/"sales.csv")
    er=[]; eid=1
    for s in seasons.itertuples():
      total=int(harvest[harvest.season_id==s.season_id].harvested_kg.sum()); infl=1+.045*(s.start_year-2011)
      for cat,rate in zip(["Harvest Labour","Packing","Transport","Irrigation & Care","Other Operations"],[2.4,1.15,1.35,.95,.55]):
       mult=rng.normal(1,.07)*(1.18 if s.market_pressure_scenario else 1)*(1.12 if s.pandemic_scenario and cat in ("Harvest Labour","Transport") else 1)
       er.append([f"E{eid:04d}",s.season_id,f"{s.start_year}-06-30",cat,round(total*rate*infl*mult,2),"Synthetic modeled cost"]);eid+=1
    expenses=pd.DataFrame(er,columns=["expense_id","season_id","expense_date","category","amount","assumption_note"]);save(expenses,RAW/"expenses.csv")
    sh=harvest.groupby("season_id",as_index=False).agg(harvested_kg=("harvested_kg","sum"),rejected_kg=("rejected_kg","sum"),saleable_kg=("saleable_kg","sum"))
    ss=sales.groupby("season_id",as_index=False).agg(quantity_sold_kg=("quantity_kg","sum"),revenue=("revenue","sum"),amount_collected=("amount_collected","sum"),invoice_lines=("invoice_line_id","count"))
    se=expenses.groupby("season_id",as_index=False).agg(operating_expenses=("amount","sum"))
    k=seasons.merge(sh,on="season_id").merge(ss,on="season_id").merge(se,on="season_id")
    k["operating_contribution"]=(k.revenue-k.operating_expenses).round(2); k["wastage_rate_pct"]=(k.rejected_kg/k.harvested_kg*100).round(2)
    k["sale_through_rate_pct"]=(k.quantity_sold_kg/k.saleable_kg*100).round(2); k["collection_rate_pct"]=(k.amount_collected/k.revenue*100).round(2)
    k["revenue_per_kg"]=(k.revenue/k.quantity_sold_kg).round(2); k["revenue_yoy_pct"]=k.revenue.pct_change().mul(100).round(2); save(k,OUT/"seasonal_kpis.csv")
    bp=sales.groupby("buyer_id",as_index=False).agg(invoice_lines=("invoice_line_id","count"),quantity_sold_kg=("quantity_kg","sum"),revenue=("revenue","sum"),amount_collected=("amount_collected","sum")).merge(buyers,on="buyer_id")
    bp["revenue_share_pct"]=(bp.revenue/bp.revenue.sum()*100).round(2);bp["collection_rate_pct"]=(bp.amount_collected/bp.revenue*100).round(2);save(bp.sort_values("revenue",ascending=False),OUT/"buyer_performance.csv")
    vp=sales.groupby("variety_id",as_index=False).agg(invoice_lines=("invoice_line_id","count"),quantity_sold_kg=("quantity_kg","sum"),revenue=("revenue","sum"),avg_selling_price_per_kg=("price_per_kg","mean")).merge(varieties,on="variety_id")
    vp["revenue_share_pct"]=(vp.revenue/vp.revenue.sum()*100).round(2);vp["avg_selling_price_per_kg"]=vp.avg_selling_price_per_kg.round(2);save(vp.sort_values("revenue",ascending=False),OUT/"variety_performance.csv")
    m=sales.copy();m["month"]=pd.to_datetime(m.invoice_date).dt.to_period("M").astype(str);m=m.groupby("month",as_index=False).agg(quantity_sold_kg=("quantity_kg","sum"),revenue=("revenue","sum"),invoice_lines=("invoice_line_id","count"));save(m,OUT/"monthly_sales.csv")
    quality=pd.DataFrame([["seasons",len(seasons),"PASS"],["buyers",len(buyers),"PASS"],["varieties",len(varieties),"PASS"],["harvest rows",len(harvest),"PASS" if (harvest.harvested_kg>=harvest.saleable_kg).all() else "FAIL"],["sales rows",len(sales),"PASS" if (sales.revenue>=0).all() else "FAIL"],["expense rows",len(expenses),"PASS" if (expenses.amount>=0).all() else "FAIL"]],columns=["check","row_count","status"]);save(quality,OUT/"data_quality_report.csv")
    print(f"Generated {len(seasons)} seasons, {len(harvest)} harvest rows, {len(sales)} sales lines and {len(expenses)} expense rows.")
    print("Analysis outputs written to data/processed/.")

if __name__=="__main__": main()
