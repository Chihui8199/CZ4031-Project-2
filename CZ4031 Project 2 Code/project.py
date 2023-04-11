"""
Main Method to invoke all other necessary procedures from the 3 files
"""
import preprocessing
import annotation
import interface_test

if __name__ == '__main__':
    try:
        preprocessor = preprocessing.Preprocessing()
        sql_query1 = "SELECT  l_orderkey, o_orderdate, o_shippriority, sum((l_extendedprice) * (1-l_discount)) as revenue " \
            "FROM customer, orders, lineitem " \
            "WHERE customer.c_custkey = orders.o_orderkey " \
            "AND lineitem.l_orderkey = orders.o_orderkey " \
            "AND l_shipdate < '1995-03-15' " \
            "GROUP BY l_orderkey, o_orderdate, o_shippriority " \
            "ORDER BY revenue DESC, o_orderdate " \
            "LIMIT 20;"
        sql_query2 = "SELECT l_orderkey, o_orderdate, o_shippriority, sum((l_extendedprice) * (1-l_discount)) as revenue " \
            "FROM customer, orders, lineitem " \
            "WHERE customer.c_custkey = orders.o_orderkey " \
            "AND lineitem.l_orderkey = orders.o_orderkey " \
            "AND l_shipdate < '1995-03-15' " \
            "GROUP BY l_orderkey, o_orderdate, o_shippriority " \
            "ORDER BY revenue DESC, o_orderdate " \
            "LIMIT 20;"
        query_plan1 = preprocessor.get_query_plan(sql_query1)
        print("QUERY_PLAN1", query_plan1)
        query_plan2 = preprocessor.get_query_plan(sql_query2)
        print("QUERY_PLAN2", query_plan2)

        results = interface_test.Comparison().comparing(sql_query1, sql_query2)
        print(results)


        #Make this cleaner when integrate
        if query_plan1 != {}:
            # print("printing queryplan", query_plan)
            print("Annotating.........")
            annotator = annotation.Annotation(query_plan1)
            print("Generate Graph.........")
            g = annotator.generate_graph("query_plan1")
        if query_plan2!= {}:
            # print("printing queryplan", query_plan)
            print("Annotating.........")
            annotator = annotation.Annotation(query_plan2)
            print("Generate Graph.........")
            g = annotator.generate_graph("query_plan2")
        
        #app = interface.QEPAnalyser(preprocessor, annotator)
    except Exception as e:
        print("PROGRAM CRASHED! EXITING NOW!")
        print("ERROR: ", e)
    finally:
        print("ENDED PROGRAM!")

