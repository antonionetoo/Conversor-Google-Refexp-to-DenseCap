
import os

class CopierImagem():
    def __init__(self, source, destiny):
        self._source  = source
        self._destiny = destiny
    
    def _copy_command(self, source, destiny):
        comando_copia = 'cp  %s %s' % (source, destiny)
        return os.system(comando_copia)

    def _download(self, url, destiny='.'):
       os.system('wget -c %s -O %s' % (url, destiny))

    def copy(self, old_name, new_name, url):
        source = '%s%s' % (self._source, old_name)
        destiny = '%s%s.jpg' % (self._destiny, new_name)

        if (self._copy_command(source, destiny)):
            self._download(url, destiny=source)

            if (self._copy_command(source, destiny)):
                print('************** There was an error copying the image. %s' %
                  (old_name))

    

  