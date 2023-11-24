from django.http import JsonResponse
from loguru import logger

def test(request):
    return JsonResponse({"success": "working"})

def custom_api(func):
    """
        Used for handling error scenarios 
        and validating data keys if required
    """
    def wrapper(self, request, *args, **kwargs):
        try:
            data = func(self, request,*args, **kwargs)
            final_data = {"status": 200,
                          "data": data}
            return JsonResponse(final_data, safe=False)
        except Exception as e:
            final_data = {"status": 500,
                          "errorMsg": str(e)}
            return JsonResponse(final_data, safe=False)
    return wrapper
