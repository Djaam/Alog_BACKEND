import logging
from django.utils.deprecation import MiddlewareMixin
import os

# Configure logging
log_file_path = os.path.join(os.path.dirname(__file__), 'request_logs.log')
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
)

class LogRequestsMiddleware(MiddlewareMixin):

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

   

    def process_request(self, request):
        ip_address = self.get_client_ip(request)
        logging.info(f"IP: {ip_address} , Path: {request.path}")

