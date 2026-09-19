from rest_framework.decorators import api_view
from rest_framework.response import Response
from .analysis import analytics_for
from .charts import make_charts
@api_view(["GET"])
def summary(request): return Response(analytics_for(request.user))
@api_view(["POST"])
def charts(request): return Response(make_charts(analytics_for(request.user)))
