import json
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Pipeline, PipelineStep, ProcessingHistory
from .forms import PipelineForm
from datasets.models import Dataset
from datasets.utils import read_uploaded_file
from processing.pipeline_executor import execute_pipeline


@login_required
def pipeline_list(request):
    pipelines = Pipeline.objects.filter(user=request.user)
    return render(request, 'pipelines/list.html', {'pipelines': pipelines})


@login_required
def create_pipeline(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user)

    if request.method == 'POST':
        form = PipelineForm(request.POST)
        if form.is_valid():
            pipeline = form.save(commit=False)
            pipeline.user = request.user
            pipeline.save()
            messages.success(request, 'Pipeline created. Add steps to configure it.')
            return redirect('pipelines:edit', pipeline_id=pipeline.id)
    else:
        initial_data = {
            'name': f'Process {dataset.original_name}',
            'output_format': dataset.file_format,
        }
        form = PipelineForm(initial=initial_data)

    return render(request, 'pipelines/create.html', {'form': form, 'dataset': dataset})


@login_required
def edit_pipeline(request, pipeline_id):
    pipeline = get_object_or_404(Pipeline, id=pipeline_id, user=request.user)
    steps = pipeline.steps.all()

    if request.method == 'POST':
        form = PipelineForm(request.POST, instance=pipeline)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pipeline updated.')
            return redirect('pipelines:edit', pipeline_id=pipeline.id)

        step_order = 0
        operations = request.POST.getlist('operation')
        configs = request.POST.getlist('config')
        step_ids_to_keep = []

        for op, cfg in zip(operations, configs):
            if op:
                step_order += 1
                step_data = {'operation': op}
                try:
                    step_data['config'] = json.loads(cfg) if cfg.strip() else {}
                except json.JSONDecodeError:
                    step_data['config'] = {}

                step, created = PipelineStep.objects.get_or_create(
                    pipeline=pipeline,
                    step_order=step_order,
                    defaults=step_data,
                )
                if not created:
                    PipelineStep.objects.filter(pk=step.pk).update(**step_data)
                step_ids_to_keep.append(step.pk)

        pipeline.steps.exclude(pk__in=step_ids_to_keep).delete()

        return redirect('pipelines:edit', pipeline_id=pipeline.id)
    else:
        form = PipelineForm(instance=pipeline)

    operation_choices = PipelineStep.OPERATION_CHOICES

    return render(request, 'pipelines/edit.html', {
        'form': form,
        'pipeline': pipeline,
        'steps': steps,
        'operation_choices': operation_choices,
    })


@login_required
def delete_pipeline(request, pipeline_id):
    pipeline = get_object_or_404(Pipeline, id=pipeline_id, user=request.user)
    pipeline.delete()
    messages.success(request, 'Pipeline deleted.')
    return redirect('pipelines:list')


@login_required
def execute_pipeline_view(request, pipeline_id):
    pipeline = get_object_or_404(Pipeline, id=pipeline_id, user=request.user)
    dataset_id = request.GET.get('dataset_id')

    if not dataset_id:
        messages.error(request, 'Please select a dataset to process.')
        return redirect('pipelines:edit', pipeline_id=pipeline.id)

    dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user)

    if request.method == 'POST':
        df = read_uploaded_file(dataset.file)
        steps_data = list(pipeline.steps.values('operation', 'config'))

        result = execute_pipeline(df, steps_data)

        history = ProcessingHistory.objects.create(
            pipeline=pipeline,
            runtime=result['runtime'],
            output_format=pipeline.output_format,
            summary=result['summary'],
        )

        if 'output' in result:
            from django.http import HttpResponse
            response = HttpResponse(result['output'], content_type=result['output_content_type'])
            response['Content-Disposition'] = f'attachment; filename="processed_{dataset.original_name}"'
            return response

        original_stats = {
            'rows': len(df),
            'columns': len(df.columns),
            'missing': int(df.isnull().sum().sum()),
            'duplicates': int(df.duplicated().sum()),
        }
        processed_df = result['dataframe']
        processed_stats = {
            'rows': len(processed_df),
            'columns': len(processed_df.columns),
            'missing': int(processed_df.isnull().sum().sum()),
            'duplicates': int(processed_df.duplicated().sum()),
        }
        processed_rows = processed_df.values.tolist()
        processed_columns = list(processed_df.columns)

        context = {
            'pipeline': pipeline,
            'dataset': dataset,
            'result': result,
            'history': history,
            'original_stats': original_stats,
            'processed_stats': processed_stats,
            'processed_rows': processed_rows,
            'processed_columns': processed_columns,
        }
        return render(request, 'pipelines/results.html', context)

    return render(request, 'pipelines/execute.html', {
        'pipeline': pipeline,
        'dataset': dataset,
    })


@login_required
def download_processed(request, history_id):
    history = get_object_or_404(ProcessingHistory, id=history_id)
    if history.pipeline and history.pipeline.user != request.user:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()

    from processing.conversion import convert_dataframe
    output_format = request.GET.get('format', 'csv')

    dataset_id = request.GET.get('dataset_id')
    if not dataset_id:
        from django.http import HttpResponseBadRequest
        return HttpResponseBadRequest('Missing dataset_id')

    dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user)
    df = read_uploaded_file(dataset.file)
    steps_data = list(history.pipeline.steps.values('operation', 'config'))
    result = execute_pipeline(df, steps_data)

    if 'output' in result:
        content = result['output']
        content_type = result['output_content_type']
        ext = result['output_extension']
    else:
        processed_df = result['dataframe']
        content, content_type, ext = convert_dataframe(processed_df, output_format)

    response = HttpResponse(content, content_type=content_type)
    filename = f'processed_{dataset.original_name}'
    if ext:
        base = os.path.splitext(filename)[0]
        filename = base + ext
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required
def pipeline_results(request, pipeline_id, history_id):
    pipeline = get_object_or_404(Pipeline, id=pipeline_id, user=request.user)
    history = get_object_or_404(ProcessingHistory, id=history_id, pipeline=pipeline)
    return render(request, 'pipelines/results.html', {
        'pipeline': pipeline,
        'history': history,
        'result': {'summary': history.summary, 'runtime': history.runtime, 'success': True},
    })


@login_required
def processing_history(request):
    history = ProcessingHistory.objects.filter(pipeline__user=request.user)
    return render(request, 'pipelines/history.html', {'history': history})
