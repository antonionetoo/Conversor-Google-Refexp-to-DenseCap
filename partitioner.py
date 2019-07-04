import random

class Partitioner():

    def __init__(self):
        pass

    def _generate_ids(self, total_length):
        idts = [x for x in range(0, total_length)]
        random.shuffle(idts)
        return idts
    
    def _partition_size_(self, total_length, percentage):
        return int(total_length * percentage / 100)
    
    def _partition_example(self, refexps, ids, length_val, length_test):
        ids_test  = ids[0:length_test]
        ids_val   = ids[length_test : length_test + length_val]
        ids_train = ids[length_test + length_val:]

        test  = [refexps[i]['id'] for i in ids_test]
        val   = [refexps[i]['id'] for i in ids_val]
        train = [refexps[i]['id'] for i in ids_train]
        
        return (train, val, test)

    def partition(self, refexps, percentage_teste = 20, percentage_validacao = 20):
        print('************** partitioning')

        total_length = len(refexps)
        length_test  = self._partition_size_(total_length, percentage_teste)
        length_val   = self._partition_size_(total_length, percentage_validacao)
        
        ids = self._generate_ids(total_length)
        train, val, test = self._partition_example(refexps, ids, length_val, length_test)
              
        return {'train': train, 'val': val, 'test': test }
#[a for a in val if a in train or a in test]
#[a for a in test if a in train or a in val]
#[a for a in train if a in test or a in val]
#c = train + val + test
#[a for a in ids if a not in c]
"""
class ParticionadorPorObjeto(Particionador):

    def __init__(self):
        self._regions_particionadas = dict()
        super().__init__()
    
    def _region_particionada(self, region_id):
        return region_id in self._regions_particionadas.keys()
    
    def _esta_na_particao(self, region_id, particao):
        return (self._region_particionada(region_id) and 
            particao in self._regions_particionadas[region_id])
"""
    # def _partition_example(self, refexps, ids, length_val, length_test):

    #     treinamento = []
    #     teste       = []
    #     validacao   = []

    #     particao  = ''
    #     region_id = refexp['regions'][0]['region_id']

    #     if (len(teste) < length_test and 
    #         not self._esta_na_particao(region_id, 'test')):

    #         teste.append(idt)
    #         particao = 'test'
   
    #     elif (len(validacao) < length_val and 
    #         not self._esta_na_particao(region_id, 'val')):
    #         validacao.append(idt)   
    #         particao = 'val'

    #     else:
    #         treinamento.append(idt)
        
    #     if (self._region_particionada(region_id)):
    #         self._regions_particionadas[region_id].append(particao)
    #     else:
    #         self._regions_particionadas.update({region_id: [particao]})
