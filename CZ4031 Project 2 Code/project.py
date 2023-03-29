"""
Main Method to invoke all other necessary procedures from the 3 files
"""

import interface
import preprocessing
import annotation

if __name__ == '__main__':
    try:
        preprocessor = preprocessing.Preprocessing()
        annotator = annotation.Annotation()
        app = interface.QEPAnalyser(preprocessor, annotator)
    except Exception as e:
        print("PROGRAM CRASHED! EXITING NOW!")
        print("ERROR: ", e)
    finally:
        print("ENDED PROGRAM!")