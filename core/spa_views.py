import os
from django.conf import settings
from django.http import HttpResponse, FileResponse, Http404
from django.views.generic import View
from django.utils._os import safe_join

class SPAView(View):
    def get(self, request, *args, **kwargs):
        # Get the requested path
        path = request.path.lstrip('/')
        
        # If empty path, serve index.html
        if not path:
            return self.serve_index()
            
        # Try to find the file in static dirs
        for static_dir in settings.STATICFILES_DIRS:
            try:
                file_path = safe_join(static_dir, path)
                if os.path.isfile(file_path):
                    # Use FileResponse to serve with correct MIME type
                    return FileResponse(open(file_path, 'rb'))
            except (ValueError, UnicodeDecodeError):
                continue
                
        # If not found, fall back to index.html (for Angular routing)
        return self.serve_index()

    def serve_index(self):
        for static_dir in settings.STATICFILES_DIRS:
            index_path = os.path.join(static_dir, 'index.html')
            if os.path.isfile(index_path):
                return FileResponse(open(index_path, 'rb'))
        return HttpResponse("index.html not found", status=404)
