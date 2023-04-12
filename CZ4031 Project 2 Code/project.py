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
            "AND l_shipdate < '11/11/2022'" \
            "GROUP BY l_orderkey, o_orderdate, o_shippriority " \
            "ORDER BY revenue DESC, o_orderdate " \
            "LIMIT 20;"
        sql_query2 = "SELECT  l_orderkey, o_orderdate, o_shippriority, sum((l_extendedprice) * (1-l_discount)) as revenue " \
            "FROM customer, orders, lineitem " \
            "WHERE customer.c_custkey = orders.o_orderkey " \
            "OR lineitem.l_orderkey = orders.o_orderkey " \
            "AND l_shipdate < '14/11/2022'" \
            "GROUP BY l_orderkey, o_orderdate, o_shippriority " \
            "ORDER BY revenue DESC, o_orderdate " \
            "LIMIT 20;"

        results = interface_test.Comparison().comparing(sql_query1, sql_query2)
        print(results)

        #app = interface.QEPAnalyser(preprocessor, annotator)
    except Exception as e:
        print("PROGRAM CRASHED! EXITING NOW!")
        print("ERROR: ", e)
    finally:
        print("ENDED PROGRAM!")

