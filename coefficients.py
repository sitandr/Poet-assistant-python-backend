import yaml

coefficients = yaml.safe_load(open('coefficients.yaml',
                                       encoding = 'utf-8'))

k_alliteration = coefficients['check_transcription']['alliteration']
k_stresses     = coefficients['check_transcription']['stresses']
k_consonant_structure = coefficients['check_transcription']['consonant_structure']

k_meaning = coefficients['meaning']
