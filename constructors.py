
from abc import ABCMeta, abstractmethod

class ConstructorRegions:

    def __init__(self):
        self._region_id = 0

    @abstractmethod
    def construct(self):
        pass
        

class ConstructorRegionsPerImagem(ConstructorRegions):

    def construct(self, dataset, annotation):  
        self._region_id += 1
        return {'region_id': self._region_id,
                'image_id' : annotation['image_id'],
                'x'        : annotation['bbox'][0],
                'y'        : annotation['bbox'][1],
                'width'    : annotation['bbox'][2],
                'height'   : annotation['bbox'][3],
                'phrase'   : [dataset['refexps'][str(i)]['raw'] for i in [a for a in annotation['refexp_ids']]],
                'tokens'   : []
                }


class ConstructorRegionsPerObjetos(ConstructorRegions):

    def construct(self, dataset, annotation):
        regions = []
        self._region_id += 1

        for phrase in self._get_phrases(dataset, annotation):
            regions.append({'region_id': self._region_id,
                            'image_id' : annotation['image_id'],
                            'x'        : annotation['bbox'][0],
                            'y'        : annotation['bbox'][1],
                            'width'    : annotation['bbox'][2],
                            'height'   : annotation['bbox'][3],
                            'phrase'   : phrase,
                            'tokens'   : []
                            })
        return regions

    def _get_phrases(self, dataset, annotation):
        return [dataset['refexps'][str(i)]['raw'] for i in [a for a in annotation['refexp_ids']]]
