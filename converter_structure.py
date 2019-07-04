import constructors 
from abc import ABCMeta, abstractmethod

class ConverterStructure():

    def __init__(self, constructor_region):
        self._constructor_region = constructor_region
    
    @abstractmethod
    def convert_structure(self, dataset):
        pass

class ConverterStructurePerImagem(ConverterStructure):
    
    def __init__(self):
        super().__init__(constructors.ConstructorRegionsPerImagem())

    def convert_structure(self, dataset):
        print('************ converting structure')
        images_converted = dict()
        refexps = []
   
        for annotation in dataset['annotations'].values():
            region = self._constructor_region.construct(dataset, annotation)
         
            if annotation['image_id'] in images_converted.keys():
                refexps[images_converted[annotation['image_id']]]['regions'].append(region)
            else:
                refexps.append({'id': annotation['image_id'],'regions': [region]})
                images_converted.update({annotation['image_id']: len(refexps) - 1})
        
        return refexps
    
class ConverterStructurePerObject(ConverterStructure):
    
    def __init__(self):
        pass
        #super().__init__(construtores.ConstructorRegionsPerObjetos())
    
    def convert_structure(self, dataset):
        refexps = []

        for annotation in dataset['annotations'].values():
            for region in self._constructor_region.construir(dataset, annotation):
                refexps.append({'id': annotation['image_id'],'regions': [region]})

        return refexps

    def _teste(self, refexps):
        for refexp in refexps:
            for i, region in enumerate(refexp['regions']):

                for i2, region2 in enumerate(refexp['regions']):
                    if ((i != i2) and (region['height']  == region2['height']
                                  and  region['width']      == region2['width']
                                  and  region['x']          == region2['x']
                                  and  region['y']          == region2['y']
                                  and  region['region_id']  != region2['region_id'])):
                        print('error')