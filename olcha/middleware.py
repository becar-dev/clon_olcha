import time
from django.utils.deprecation import MiddlewareMixin

class RequestTimeLoggingMiddleware(MiddlewareMixin):
    """
    Har bir so'rovni bajarishga ketgan vaqtni o'lchaydi va konsolga chiqaradi.
    """
    def process_request(self, request):
        # So'rov kelganda, hozirgi vaqtni saqlab qo'yamiz
        request.start_time = time.time()

    def process_response(self, request, response):
        # Agar so'rovda 'start_time' atributi bo'lmasa (ba'zi hollarda), hech narsa qilmaymiz
        if not hasattr(request, 'start_time'):
            return response

        # Umumiy ketgan vaqtni hisoblaymiz
        duration = time.time() - request.start_time
        
        # Natijani formatlab, konsolga chiqaramiz
        # Masalan: [INFO] GET /api/v1/products/ (took 0.05s)
        print(f"[INFO] {request.method} {request.path} (took {duration:.2f}s)")
        
        return response