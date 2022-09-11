from django.conf import settings
from django.core.exceptions import ValidationError
from pathlib import Path
from datetime import date

today = date.today()
creation_date = date.isoformat(today)


def dynamic_path( instance, filename ):
    file_extension = filename.split('.')[-1]
    standard_name = "%s-%s-%s.%s" % ( instance.first_name,instance.last_name,creation_date, file_extension)
    profile_folder = f'profile/{ standard_name }'    
    docx_folder    = f'docx/{ file_extension }/{ standard_name }'
    cases ={
        "pdf" : docx_folder,
        "docx": docx_folder,
        "jpg" : profile_folder,
        "png" : profile_folder
    }
    file_route = cases.get( file_extension )
    print(file_route)
    return file_route

def file_size( value ):
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError( 'El archivo seleccionado no debe pesar mas de 1 mb' )