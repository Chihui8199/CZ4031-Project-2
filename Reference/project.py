"""
Main Method to invoke all other necessary procedures from the 3 files
"""

import interface
import preprocessing
import annotation

if __name__ == "__main__":
    preprocessor = preprocessing.Preprocessing()
    annotater = annotation.Annotation()
    app = interface.QEPAnalyzer(preprocessor, annotater)
    try:
        app.mainloop()
    except:
        print("Program crashed")
    finally:
        print("Ended programming. Cleaning up all gpio code")
