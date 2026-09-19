from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from django.conf import settings

def make_charts(data):
    output=Path(settings.BASE_DIR)/"static"/"charts"; output.mkdir(parents=True,exist_ok=True)
    types=data["food_types"]
    plt.figure(figsize=(7,4)); plt.bar([x["label"] for x in types],[x["waste"] for x in types],color="#16a34a"); plt.title("Food type vs waste"); plt.ylabel("Waste (kg)"); plt.xticks(rotation=25); plt.tight_layout(); plt.savefig(output/"food_type_waste.png"); plt.close()
    trend=data["trend"]
    plt.figure(figsize=(7,4)); plt.plot([x["date"] for x in trend],[x["waste"] for x in trend],marker="o",color="#f97316"); plt.title("Daily waste trend"); plt.ylabel("Waste (kg)"); plt.xticks(rotation=25); plt.tight_layout(); plt.savefig(output/"waste_trend.png"); plt.close()
    return {"food_type_chart":"/static/charts/food_type_waste.png","trend_chart":"/static/charts/waste_trend.png"}
