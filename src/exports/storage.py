from django.core.files.storage import default_storage

def save(fpath, file_obj, overwirte = False):
    '''Export a file to the default django storage with the option of overwritting the current item'''

    if overwirte is True and default_storage.exists(fpath):
        default_storage.delete(fpath)
    
    default_storage.save(fpath, file_obj)