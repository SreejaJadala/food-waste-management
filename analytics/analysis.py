import numpy as np
import pandas as pd
from food.models import FoodWaste

def analytics_for(user):
    records=FoodWaste.objects.all() if user.is_staff or user.role=="ADMIN" else FoodWaste.objects.filter(owner=user)
    values=list(records.values("food_type","prepared_quantity","wasted_quantity","date"))
    if not values:
        return {"total_prepared":0,"total_wasted":0,"average_waste":0,"maximum_waste":0,"minimum_waste":0,"waste_percentage":0,"most_wasted_food_type":"No records","trend":[],"food_types":[]}
    frame=pd.DataFrame(values); waste=frame["wasted_quantity"].to_numpy(dtype=float); prepared=frame["prepared_quantity"].to_numpy(dtype=float)
    by_type=frame.groupby("food_type",as_index=False)["wasted_quantity"].sum().sort_values("wasted_quantity",ascending=False)
    frame["date"]=pd.to_datetime(frame["date"]); trend=frame.groupby(frame["date"].dt.strftime("%Y-%m-%d"))["wasted_quantity"].sum().reset_index()
    total_prepared=float(np.sum(prepared)); total_wasted=float(np.sum(waste))
    return {"total_prepared":round(total_prepared,2),"total_wasted":round(total_wasted,2),"average_waste":round(float(np.mean(waste)),2),"maximum_waste":round(float(np.max(waste)),2),"minimum_waste":round(float(np.min(waste)),2),"waste_percentage":round((total_wasted/total_prepared*100) if total_prepared else 0,2),"most_wasted_food_type":by_type.iloc[0]["food_type"],"food_types":[{"label":r.food_type,"waste":round(float(r.wasted_quantity),2)} for r in by_type.itertuples()],"trend":[{"date":r.date,"waste":round(float(r.wasted_quantity),2)} for r in trend.itertuples()]}
