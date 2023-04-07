"""
Main Method to invoke all other necessary procedures from the 3 files
"""
import preprocessing
import annotation

if __name__ == '__main__':
    try:
        preprocessor = preprocessing.Preprocessing()
        sql_query = "SELECT l_orderkey, o_orderdate, o_shippriority, sum((l_extendedprice) * (1-l_discount)) as revenue " \
            "FROM customer, orders, lineitem " \
            "WHERE customer.c_custkey = orders.o_orderkey " \
            "AND lineitem.l_orderkey = orders.o_orderkey " \
            "AND orders.o_orderdate < '1995-03-15' " \
            "AND l_shipdate < '1995-03-15' " \
            "AND c_mktsegment = 'BUILDING' " \
            "GROUP BY l_orderkey, o_orderdate, o_shippriority " \
            "ORDER BY revenue DESC, o_orderdate " \
            "LIMIT 20;"
        query_plan = preprocessor.get_query_plan(sql_query)
        #TODO: INTEGRATE: 
        # fetch query_plan result (valid or invalid + the error"
        # for the app
        
        if query_plan != {}:
            # print("printing queryplan", query_plan)
            print("Annotating.........")
            annotator = annotation.Annotation(query_plan)
            print("Generate Graph.........")
            g = annotator.generate_graph()
        
        #app = interface.QEPAnalyser(preprocessor, annotator)
    except Exception as e:
        print("PROGRAM CRASHED! EXITING NOW!")
        print("ERROR: ", e)
    finally:
        print("ENDED PROGRAM!")

