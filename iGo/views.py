from django.shortcuts import render_to_response


def handler404(request):
    response = render_to_response('error_404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('error_500.html', {})
    response.status_code = 500
    return response
