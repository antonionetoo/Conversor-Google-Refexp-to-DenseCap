
import os

class CopierImagem():
    def __init__(self):
        pass
    
    def _copy_command(self, source, destiny):
        comando_copia = 'cp  %s %s' % (source, destiny)
        return os.system(comando_copia)

    def _download(self, url, destiny='.'):
       os.system('wget -c %s -O %s' % (url, destiny))

    def copy(self, old_name, new_name, url, path_base='../external/coco/images/'):
        source = '%strain2014/train2014/%s' % (path_base, old_name)
        destiny = '%strain2014/images_id/%s.jpg' % (path_base, new_name)

        if (self._copy_command(source, destiny)):
            self._download(url, destiny=source)

            if (self._copy_command(source, destiny)):
                print('********* Ocorreu um erro ao realizar a copia da imagem %s' %
                  (old_name))

    

  