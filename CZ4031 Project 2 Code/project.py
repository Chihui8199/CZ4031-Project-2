"""
Main Method to invoke all other necessary procedures from the 3 files
"""
import interface
import preprocessing
import annotation

if __name__ == '__main__':
    try:
        preprocessor = preprocessing.Preprocessing()
        query_plan = preprocessor.get_query_plan("select * from customer C, orders O where C.c_custkey = O.o_custkey")
        g = preprocessing.GraphGenerator(query_plan).generate_graph()
        g1 = preprocessing.QueryPlan(query_plan)
        print("MAIN: THIS IS THE QUERY PLAN", query_plan)
        annotator = annotation.Annotation()
        app = interface.QEPAnalyser(preprocessor, annotator)
    except Exception as e:
        print("PROGRAM CRASHED! EXITING NOW!")
        print("ERROR: ", e)
    finally:
        print("ENDED PROGRAM!")