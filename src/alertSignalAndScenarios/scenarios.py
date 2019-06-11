# -*- coding: utf-8 -*-
# 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
#
import ConfigParser

lengthContour = {
    'cuckoo': 0.40,  # s
    'highchirp': 0.10,  # s
    'lowchirp': 0.16  # s
}

kernels = {
    'cuckoo-org': {
        'tipoNucleo': 'armonico',
        'nArmonicas': 4
    },
    'highchirp-org': {
        'tipoNucleo': 'armonico',
        'nArmonicas': 1
    },
    'lowchirp-org': {
        'tipoNucleo': 'armonicoimpar',
        'nArmonicas': 5
    },
    'proposedNotPrime': {
        'tipoNucleo': 'propuestoNoPrimo',
        'nArmonicas': 3
    },
    'proposedPrime': {
        'tipoNucleo': 'propuestoPrimo',
        'nArmonicas': 3
    }
}

banks = {
    'cuckoo-org': {
        'fRange': [900, 1100],
        'df': 200
    },
    'highchirp-org': {
        'fRange': [2000, 3000],
        'df': 100
    },
    'lowchirp-org': {
        'fRange': [950, 1750],
        'df': 100
    },
    'proposed': {
        'fRange': [900, 3000],
        'df': 100,
    }
};

qs = {
    'cuckoo': 1,
    'highchirp': 2,
    'lowchirp': 2
}

thresholds = {
    # scenery 1
    'cuckoo-scenery1': {
        'alpha': 0.14,
        'beta': 0.45,
        'forgetFactor': 0.0
    },
    'highchirp-scenery1': {
        'alpha': 0.07,
        'beta': 0.3,
        'forgetFactor': 0.0
    },
    'lowchirp-scenery1': {
        'alpha': 0.07,
        'beta': 0.3,
        'forgetFactor': 0.0
    },
    # scenery 2
    'cuckoo-scenery2': {
        'alpha': 0.14,
        'beta': 0.45,
        'forgetFactor': 0.0
    },
    'highchirp-scenery2': {
        'alpha': 0.07,
        'beta': 0.3,
        'forgetFactor': 0.0
    },
    'lowchirp-scenery2': {
        'alpha': 0.07,
        'beta': 0.3,
        'forgetFactor': 0.0
    },
    # scenery 3, mejores valores encontrados en los barridos
    'cuckoo-scenery3': {
        'alpha': 0.03,
        'beta': 0.9,
        'forgetFactor': 0.0
    },
    'highchirp-scenery3': {
        'alpha': 0.001,
        'beta': 0.003,
        'forgetFactor': 0.0
    },
    'lowchirp-scenery3': {
        'alpha': 0.03,
        'beta': 0.3,
        'forgetFactor': 0.0
    },
    # scenery 4, mejores valores encontrados en los barridos
    'cuckoo-scenery4': {
        'alpha': 0.03,
        'beta': 0.9,
        'forgetFactor': 0.0
    },
    'highchirp-scenery4': {
        'alpha': 0.001,
        'beta': 0.003,
        'forgetFactor': 0.0
    },
    'lowchirp-scenery4': {
        'alpha': 0.003,
        'beta': 0.3,
        'forgetFactor': 0.0
    },
    # scenery 5, mejores valores encontrados en los barridos
    'cuckoo-scenery5': {
        'alpha': 0.3,
        'beta': 0.09,
        'forgetFactor': 0.0
    },
    'highchirp-scenery5': {
        'alpha': 0.003,
        'beta': 0.3,
        'forgetFactor': 0.0
    },
    'lowchirp-scenery5': {
        'alpha': 0.01,
        'beta': 0.09,
        'forgetFactor': 0.0
    },
    # scenery 6, mejores valores encontrados en los barridos
    'cuckoo-scenery6': {
        'alpha': 0.09,
        'beta': 0.09,
        'forgetFactor': 0.0
    },
    'highchirp-scenery6': {
        'alpha': 0.03,
        'beta': 0.3,
        'forgetFactor': 0.0
    },
    'lowchirp-scenery6': {
        'alpha': 0.003,
        'beta': 0.3,
        'forgetFactor': 0.0
    },
    # scenery 7, mejores valores encontrados en los barridos
    'cuckoo-scenery7': {
        'alpha': 0.0,  # NA, pero se mantiene
        'beta': 0.9,
        'forgetFactor': 0.0
    },
    'highchirp-scenery7': {
        'alpha': 0.0,  # NA, pero se mantiene
        'beta': 0.003,
        'forgetFactor': 0.0
    },
    'lowchirp-scenery7': {
        'alpha': 0.0,  # NA, pero se mantiene
        'beta': 0.03,
        'forgetFactor': 0.0
    },
    # scenery 8, mejores valores encontrados en los barridos
    'cuckoo-scenery8': {
        'alpha': 0.0,  # NA, pero se mantiene
        'beta': 0.9,
        'forgetFactor': 0.95
    },
    'highchirp-scenery8': {
        'alpha': 0.0,  # NA, pero se mantiene
        'beta': 0.03,
        'forgetFactor': 0.987
    },
    'lowchirp-scenery8': {
        'alpha': 0.0,  # NA, pero se mantiene
        'beta': 0.09,
        'forgetFactor': 0.996
    },
    # scenery 9, mejores valores encontrados en los barridos
    'cuckoo-scenery9': {
        'alpha': None,
        'beta': 0.9,
        'forgetFactor': 0.95
    },
    'highchirp-scenery9': {
        'alpha': None,
        'beta': 0.3,
        'forgetFactor': 0.975
    },
    'lowchirp-scenery9': {
        'alpha': None,
        'beta': 0.09,
        'forgetFactor': 0.993
    },
}

scenarioParameters = {
    'scenery1': {
        'kernels': {'cuckoo': 'cuckoo-org', 'highchirp': 'highchirp-org', 'lowchirp': 'lowchirp-org'},
        'banks': {'cuckoo': 'cuckoo-org', 'highchirp': 'highchirp-org', 'lowchirp': 'lowchirp-org'},
        'distances': {'cuckoo': 'proporcion', 'highchirp': 'l2mod', 'lowchirp': 'l2mod'},
        'thresholdMethod': {'cuckoo': 'fixed', 'highchirp': 'fixed', 'lowchirp': 'fixed'}
    },
    'scenery2': {  # igual a escenario 1, lo que cambia más adelante es el método de evaluación
        'kernels': {'cuckoo': 'cuckoo-org', 'highchirp': 'highchirp-org', 'lowchirp': 'lowchirp-org'},
        'banks': {'cuckoo': 'cuckoo-org', 'highchirp': 'highchirp-org', 'lowchirp': 'lowchirp-org'},
        'distances': {'cuckoo': 'proporcion', 'highchirp': 'l2mod', 'lowchirp': 'l2mod'},
        'thresholdMethod': {'cuckoo': 'fixed', 'highchirp': 'fixed', 'lowchirp': 'fixed'}
    },
    'scenery3': {
        'kernels': {'cuckoo': 'proposedPrime', 'highchirp': 'proposedPrime', 'lowchirp': 'proposedPrime'},
        'banks': {'cuckoo': 'cuckoo-org', 'highchirp': 'highchirp-org', 'lowchirp': 'lowchirp-org'},
        'distances': {'cuckoo': 'proporcion', 'highchirp': 'l2mod', 'lowchirp': 'l2mod'},
        'thresholdMethod': {'cuckoo': 'fixed', 'highchirp': 'fixed', 'lowchirp': 'fixed'}
    },
    'scenery4': {
        'kernels': {'cuckoo': 'proposedPrime', 'highchirp': 'proposedPrime', 'lowchirp': 'proposedPrime'},
        'banks': {'cuckoo': 'proposed', 'highchirp': 'proposed', 'lowchirp': 'proposed'},
        'distances': {'cuckoo': 'proporcion', 'highchirp': 'l2mod', 'lowchirp': 'l2mod'},
        'thresholdMethod': {'cuckoo': 'fixed', 'highchirp': 'fixed', 'lowchirp': 'fixed'}
    },
    'scenery5': {
        'kernels': {'cuckoo': 'cuckoo-org', 'highchirp': 'highchirp-org', 'lowchirp': 'lowchirp-org'},
        'banks': {'cuckoo': 'cuckoo-org', 'highchirp': 'highchirp-org', 'lowchirp': 'lowchirp-org'},
        'distances': {'cuckoo': 'mahalanobis-real', 'highchirp': 'mahalanobis-real', 'lowchirp': 'mahalanobis-real'},
        'thresholdMethod': {'cuckoo': 'fixed', 'highchirp': 'fixed', 'lowchirp': 'fixed'}
    },
    'scenery6': {  # igual a escenario 5, lo que cambia es la matriz de covarianza
        'kernels': {'cuckoo': 'cuckoo-org', 'highchirp': 'highchirp-org', 'lowchirp': 'lowchirp-org'},
        'banks': {'cuckoo': 'cuckoo-org', 'highchirp': 'highchirp-org', 'lowchirp': 'lowchirp-org'},
        'distances': {'cuckoo': 'mahalanobis-sin', 'highchirp': 'mahalanobis-sin', 'lowchirp': 'mahalanobis-sin'},
        'thresholdMethod': {'cuckoo': 'fixed', 'highchirp': 'fixed', 'lowchirp': 'fixed'}
    },
    'scenery7': {
        'kernels': {'cuckoo': 'cuckoo-org', 'highchirp': 'highchirp-org', 'lowchirp': 'lowchirp-org'},
        'banks': {'cuckoo': 'cuckoo-org', 'highchirp': 'highchirp-org', 'lowchirp': 'lowchirp-org'},
        'distances': {'cuckoo': 'proporcion', 'highchirp': 'l2mod', 'lowchirp': 'l2mod'},
        'thresholdMethod': {'cuckoo': 'ts2means', 'highchirp': 'ts2means', 'lowchirp': 'ts2means'}
    },
    'scenery8': {  # igual al escenario 7, lo que cambia es el uso de la integral filtrada
        'kernels': {'cuckoo': 'cuckoo-org', 'highchirp': 'highchirp-org', 'lowchirp': 'lowchirp-org'},
        'banks': {'cuckoo': 'cuckoo-org', 'highchirp': 'highchirp-org', 'lowchirp': 'lowchirp-org'},
        'distances': {'cuckoo': 'proporcion', 'highchirp': 'l2mod', 'lowchirp': 'l2mod'},
        'thresholdMethod': {'cuckoo': 'leakyInt', 'highchirp': 'leakyInt', 'lowchirp': 'leakyInt'}
    },
    'scenery9': {  # par: nucleo propuesto & distancia de Mahalanobis
        'kernels': {'cuckoo': 'cuckoo-org', 'highchirp': 'proposedPrime', 'lowchirp': 'lowchirp-org'},
        'banks': {'cuckoo': 'cuckoo-org', 'highchirp': 'highchirp-org', 'lowchirp': 'lowchirp-org'},
        'distances': {'cuckoo': 'proporcion', 'highchirp': 'mahalanobis-sin', 'lowchirp': 'mahalanobis-sin'},
        'thresholdMethod': {'cuckoo': 'leakyInt', 'highchirp': 'leakyInt', 'lowchirp': 'leakyInt'}
    }
}


def merge(dic1, dic2):
    '''
    Copy into dictionary 1 key-value pairs of dictionary 2
    '''
    for key in dic2.keys():
        dic1[key] = dic2[key]


def getScenery(sceneryID):
    configParser = ConfigParser.RawConfigParser()
    configParser.read(r'../configurations.properties')
    homeWav = configParser.get('output', 'originalWavFolderPath')

    # filepaths
    filepaths = {
        'cuckoo': '%s/cucu_slsem5o2016_10_22_15_39_10.wav' % homeWav,
        'highchirp': '%s/chirrido-alto_slsem7o2016_10_22_06_41_28.wav' % homeWav,
        'lowchirp': '%s/chirrido-bajo_slsem0s2016_09_DD_M1_SS.wav' % homeWav
    }

    homeCovMatrices = configParser.get('output', 'covarianceMatrixFolderPath')

    covRealMatrixPaths = {
        'cuckoo': '%s/cov-matrix-cuckoo.csv' % homeCovMatrices,
        'highchirp': '%s/cov-matrix-highchirp.csv' % homeCovMatrices,
        'lowchirp': '%s/cov-matrix-lowchirp.csv' % homeCovMatrices,
    }

    covSintMatrixPaths = {
        'cuckoo': '%s/cov-sintetic-cuckoo.csv' % homeCovMatrices,
        'highchirp': '%s/cov-sintetic-highchirp.csv' % homeCovMatrices,
        'lowchirp': '%s/cov-sintetic-lowchirp.csv' % homeCovMatrices
    }

    # create scenery
    cSce = {'cuckoo': {}, 'highchirp': {}, 'lowchirp': {}}
    cSceParams = scenarioParameters[sceneryID]
    for apsType in cSce.keys():
        cSce[apsType]['tipoDistancia'] = cSceParams['distances'][apsType]
        cSce[apsType]['thresholdMethod'] = cSceParams['thresholdMethod'][apsType]
        cSce[apsType]['q'] = qs[apsType]
        cSce[apsType]['filepath'] = filepaths[apsType]
        cSce[apsType]['usarEvaluacionPropuesta'] = False if sceneryID == 'scenery1' else True
        if cSce[apsType]['tipoDistancia'] == 'mahalanobis-real':
            cSce[apsType]['covMatrixPath'] = covRealMatrixPaths[apsType]
        elif cSce[apsType]['tipoDistancia'] == 'mahalanobis-sin':
            cSce[apsType]['covMatrixPath'] = covSintMatrixPaths[apsType]
        else:
            cSce[apsType]['covMatrixPath'] = None
        merge(cSce[apsType], kernels[cSceParams['kernels'][apsType]])
        merge(cSce[apsType], banks[cSceParams['banks'][apsType]])
        merge(cSce[apsType], thresholds['%s-%s' % (apsType, sceneryID)])

    return cSce
