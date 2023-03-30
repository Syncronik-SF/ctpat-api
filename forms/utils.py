import os
import requests
from django.template.loader import get_template

class PDFConverter:
    def __init__(self):
        self.api_url = "https://api.pdfendpoint.com/v1/convert"
        self.api_key = "Bearer 2b0822dcd706d20d887a06a556a9f7e0f2de8883bf"

    def download_pdf(self, url, output_directory):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        filename = url.split('/')[-1]
        output_path = os.path.join(output_directory, filename)
        response = requests.get(url)

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f'Archivo descargado correctamente y guardado en: {output_path}')
        else:
            print(f'Error al descargar el archivo: {response.status_code}')

    def convert_html_to_pdf(self, html, filename, output_directory):
        payload = {
            "sandbox": True,
            "orientation": "vertical",
            "page_size": "Letter",
            "http_headers": "{\n\t\"cache-control\": \"max-age=0\"\n}",
            "viewport ": "970x1400",
            "use_print_media ": True,
            "wait_for_network": True,
            "margin_top": "1cm",
            "margin_bottom": "1cm",
            "margin_right": "1cm",
            "css": """.vector-menu-content{\n  display:none 
            !important;\n}\n\n.vector-toc-pinned-container{\n  display:none 
            !important;\n  height:0px;\n  
            overflow:hidden;\n}\n\n.mw-table-of-contents-container{\n  display:none 
            !important;\n\n}\n\n""",
            "margin_left": "1cm",
            "filename": filename,
            "wait_for_timeout": "5000",
            "html": str(html)
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        json_response = response.json()
        url_pdf = json_response["data"]["url"]
        self.download_pdf(url=url_pdf, output_directory=output_directory)

    def render_and_convert(self, context, filename, template_path, output_directory):
        template = get_template(template_path)
        html = template.render(context)
        self.convert_html_to_pdf(html, filename, output_directory)

def convert_boolean_to_yes_or_no(value):
    return "Si" if value else "No"

def convert_boolean_to_ok_or_no(value):
    return "OK" if value else "Indicencia presentada"