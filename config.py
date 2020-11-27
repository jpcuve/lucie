import numpy as np

A = np.array([1, 2, 3], dtype=np.float64)
# paramètres sql alchemy, avec l'URL d'accès à la db. Par défaut je mets une db in-memory sqlite, que j'initialise
# avec l'application en y injectant quelques données (init.sql). C'est assez important dans la phase de dévelopement
# d'avoir une db qui démarre automatiquement avec l'appli, et de ne pas dépendre de systèmes extérieurs.
SQLALCHEMY_DATABASE_URI = 'sqlite://'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
