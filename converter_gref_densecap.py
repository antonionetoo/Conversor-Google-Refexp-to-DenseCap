import help_json
import partitioner
import copy_image
import converter_structure

import argparse

class ConverterGRefToDenseCap:

   def __init__(self, path_train_json, path_val_json):
      self._refexps             = []
      self._partitioner         = partitioner.Partitioner()
      self._copier              = None
      self._conversor_structure = converter_structure.ConverterStructurePerImagem()
      self._path_train_json     = path_train_json
      self._path_val_json       = path_val_json

   def _load_dataset(self):
      print('************** loading jsons...')
      train = help_json.get_json(self._path_train_json)
      val = help_json.get_json(self._path_val_json)

      return self._merge_dict(train, val)

   def _merge_dict(self, a, b):
      c = dict(a)
      for k1 in c.keys():
         for k2, v2 in b[k1].items():
            c[k1].update({k2: v2})
      return c

   def _copy_image(self, dataset):
      print('************** copying imagens')
      for refexp in self._refexps:
         origem  = dataset['images'][str(refexp['id'])]['file_name']
         destino = str(refexp['id'])
         url     = dataset['images'][str(refexp['id'])]['flickr_url']
            
         self._copier.copy(origem, destino, url)
      
   def _generate_region_id(self):
      print('************** generate_region_id')
      region_id = 0

      for refexp in self._refexps:
         for r in refexp['regions']:
            region_id = region_id + 1
            r['region_id'] = region_id

   def convert_json(self, copy_images = False, sufixo_nome = ""):
      dataset = self._load_dataset()

      self._refexps = self._conversor_structure.convert_structure(dataset)

      if (copy_images):
         self._copy_image(dataset)

      split = self._partitioner.partition(self._refexps)

      self._generate_region_id()

      print('************** saving jsons')
      help_json.save_json('jsons/google_refexp%s.json'%(sufixo_nome), self._refexps)
      help_json.save_json('jsons/split%s.json'%(sufixo_nome), split)

   def print_info_dataset(self):
      total_regions = 0
      total_phrases = 0
      for refexp in self._refexps:
         for region in refexp['regions']:
            total_regions += 1
            total_phrases += len(region['phrase'])

      print('Total of %d images'%(len(self._refexps)))  
      print('Total of %d referring expressions'%(total_phrases))
      print('Total of %d objects'%(total_regions))

      print('Average of %f object per images'%(float(total_regions) / len(self._refexps)))
      print('Average of %f referring expressions per object'%(float(total_phrases) / total_regions))
      print('Average of %f referring expressions per imagens'%(float(total_phrases) / len(self._refexps)))

def create_arguments():
   parser = argparse.ArgumentParser()
   parser.add_argument('-divide_by', default = 'images', type = str,
         help = 'Partitioning should happen with \'images\' or \'objects\'')
   
   parser.add_argument('-path_train_json', type = str, help = 'Aligned training file path', 
         default = '../google_refexp_dataset_release/google_refexp_train_201511_coco_aligned.json')
   
   parser.add_argument('-path_val_json', type = str, help = 'Aligned validation file path',
         default = '../google_refexp_dataset_release/google_refexp_val_201511_coco_aligned.json')

   parser.add_argument('-copy_images', default = 0, type = int,
         help = 'Copy renaming images')
   
   parser.add_argument('-images_source', type = str,
         help = 'Image source folder when -image_source is 1')

   parser.add_argument('-images_destiny', type = str,
         help = 'Destination folder of images when -image_source is 1')

   return parser.parse_args()

def main():
   args = create_arguments()

   conversor = ConverterGRefToDenseCap(args.path_train_json, args.path_val_json)
   
   if args.divide_by == 'objects':
      conversor._conversor_structure = converter_structure.ConverterStructurePerObject()
      suffix_file = "_objects"
      #conversor._partitioner       = particionador.ParticionadorPorObjeto()
   elif args.divide_by == 'images':
      suffix_file = "_images"
   else:
      raise ValueError('Incorrect value for argument \'divide_by\'')
   
   copier = copy_image.CopierImagem(args.images_source, args.images_destiny)
   conversor._copier = copier
   
   conversor.convert_json(sufixo_nome = suffix_file, copy_images = args.copy_images)
   
   if args.divide_by == 'images':
      conversor.print_info_dataset()

   print('************** Done!')

if __name__ == "__main__":
   main()

        
