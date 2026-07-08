from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pipelines.models import Pipeline
from pipelines.models import ProcessingHistory


@login_required
def home(request):
    recent_pipelines = Pipeline.objects.filter(
        user=request.user
    ).order_by('-updated_at')[:5]

    recent_history = ProcessingHistory.objects.filter(
        pipeline__user=request.user
    ).order_by('-executed_at')[:5]

    saved_pipelines = Pipeline.objects.filter(
        user=request.user
    ).count()

    context = {
        'recent_pipelines': recent_pipelines,
        'recent_history': recent_history,
        'saved_pipelines_count': saved_pipelines,
    }
    return render(request, 'dashboard/home.html', context)
