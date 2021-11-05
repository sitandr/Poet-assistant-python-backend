import yaml

coefficients = yaml.safe_load(open('config/coefficients.yaml',
                                       encoding = 'utf-8'))

k_alliteration = coefficients['check_transcription']['alliteration']
k_stresses     = coefficients['check_transcription']['stresses']
k_consonant_structure = coefficients['check_transcription']['consonant_structure']

k_meaning = coefficients['meaning']

basic_fields = {'Art': ['исскуство', 'свет', 'огонь', 'творить', 'вдохновение', 'мечтать'],
                'Battle': ['битва', 'кровь', 'безумствовать', 'храбрый', 'герой', 'зло'],
                'Love': ['страсть', 'влечение', 'красота', 'сердце', 'целовать'],
                'Epic': ['мощь', 'великий', 'просветление', 'мудрость'],
                'Fear': ['страшно', 'опасность', 'сбежать', 'ужас'],
                'Dark': ['тьма', 'смерть', 'труп', 'отчаяться', 'безумие', 'больно']}
