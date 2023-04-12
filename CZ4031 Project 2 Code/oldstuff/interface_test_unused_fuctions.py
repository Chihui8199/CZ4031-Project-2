

def why_change(self,initial,new):
    if updated_clause == None:
        self.analysis_text.config(state="normal")
        self.analysis_text.delete('1.0', END) # have to clear the output from before first before inserting
        self.analysis_text.insert('1.0', "\n\n\n\n\n\n\n\n\n\n\n\n\n\nSQL Queries are the same, please ensure they are different!", ("custom",))
        self.analysis_text.tag_configure("custom", font=custom_font, justify='center')

    # Initial Query Table ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # for child in self.sql_output_container_initial.winfo_children():
    #     child.destroy() # Clean up sql output

    # actual_output_initial, column_names_initial  = preprocessor.get_query_results(self.initial_query)

    # if (actual_output_initial is None):
    #     self.analyze_btn.configure(state=ACTIVE)
    #     return
    # elif (len(actual_output_initial) == 0):
    #     ttk.Label(self.sql_output_container_initial, text = "No results matching.", font=FONT_BOLD).pack(fill=tk.X, padx=20, pady=10, anchor=CENTER)
    # else:
    #     self.createTableOutput(actual_output_initial, column_names_initial, self.sql_output_container_initial) 

    # # New Query table ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # for child in self.sql_output_container_new.winfo_children():
    #     child.destroy() # Clean up sql output

    # actual_output_new, column_names_new  = preprocessor.get_query_results(self.new_query)

    # if (actual_output_new is None):
    #     self.analyze_btn.configure(state=ACTIVE)
    #     return
    # elif (len(actual_output_new) == 0):
    #     ttk.Label(self.sql_output_container_new, text = "No results matching.", font=FONT_BOLD).pack(fill=tk.X, padx=20, pady=10, anchor=CENTER)
    # else:
    #     self.createTableOutput(actual_output_new, column_names_new, self.sql_output_container_new) 

    # added_analysis_text = self.comparePlan(initialPlan, newPlan, added_analysis_text)
    # self.analysis_text.config(state="normal")
    # self.analysis_text.delete('1.0', END) 
    #TODO we are missing LIMIT and OFFSET clauses
    def get_updated_clause(self, initial_query, new_query):
        difference = ""

        pattern = r"(WHERE .*)"
        where_match_initial = re.search(pattern, initial_query, re.IGNORECASE)
        where_match_new = re.search(pattern, new_query, re.IGNORECASE)

        # if where clauses exist for both
        if where_match_initial and where_match_new:
            # removing the first 5 characters (where)
            first_where_clause_initial = where_match_initial.group(1)[6:]
            print("\n\nInitial:\n", first_where_clause_initial)
            
            first_where_clause_new = where_match_new.group(1)[6:]
            print("\n\nNew:\n", first_where_clause_new)


            # checking all the clauses
            clauseList = [r"(GROUP BY .*)", r"(HAVING .*)", r"(ORDER BY .*)", r"(LIMIT .*)", r"(OFFSET .*)"]

            for clause in clauseList:
                where_clause_initial, where_clause_new = self.checkClause(clause, first_where_clause_initial, first_where_clause_new)
                
            if (where_clause_initial == where_clause_new):
                print("Where clause is the same")
                return None

            else:
                print("Different")
                
                initial_conditions = set(map(str.strip, where_clause_initial.split('and')))
                new_conditions = set(map(str.strip, where_clause_new.split('and')))
               
                # Getting the difference 

                # if new query is shorter than inital query
                if len(new_query) > len(initial_query):
                    diff_conditions = new_conditions - initial_conditions
                # if new query is longer than inital query
                else:
                    diff_conditions = initial_conditions - new_conditions

                print("\ninitial ", initial_conditions)
                print("\nnew ", new_conditions)
                print("\nDIFF ", diff_conditions)
                difference = difference + str(diff_conditions) + "in the WHERE clause"
            
            clauseList = [r"(GROUP BY .*)", r"(HAVING .*)", r"(ORDER BY .*)"]
            
            for clause1 in clauseList:
                clause_initial, clause_new = self.checkClause(clause1, first_where_clause_initial, first_where_clause_new)
                clause_initial, clause_new = self.checkSubClause(clause1, clauseList, clause_initial, clause_new)

                if clause1 == r"(GROUP BY .*)":
                    groupby_clause_initial = clause_initial
                    groupby_clause_new = clause_new

                if clause1 == r"(HAVING .*)":
                    having_clause_initial = clause_initial
                    having_clause_new = clause_new
                    print(having_clause_initial)
                    print(having_clause_new)

                if clause1 == r"(ORDER BY .*)":
                    orderby_clause_initial = clause_initial
                    orderby_clause_new = clause_new
                    print(orderby_clause_initial)
                    print(orderby_clause_new)

            
        else:
            print("WHERE clause not found.")

    
        return difference
def checkClause(self, clause, where_clause_initial, where_clause_new):
    match_initial = re.search(clause, where_clause_initial, re.IGNORECASE)
    match_new = re.search(clause, where_clause_new, re.IGNORECASE)

    if match_initial:
        where_clause_initial = where_clause_initial[:match_initial.start()]

    if match_new:
        where_clause_new = where_clause_new[:match_new.start()]

    print("\n\nInitial clause:\n", where_clause_initial)
    print("\n\nNew clause:\n", where_clause_new)
    return where_clause_initial, where_clause_new

# 
def checkSubClause(self, clause1, clauseList, clause_initial, clause_new):        
    # if clauses exist for both
    if clause_initial and clause_new:
        # checking all the clauses
        clauseList = [r"(GROUP BY .*)", r"(HAVING .*)", r"(ORDER BY .*)"]

        for clause2 in clauseList:
            if clause1 == clause2:
                continue
            clause_initial, clause_new = self.checkClause(clause2, clause_initial, clause_new)
            return clause_initial, clause_new
    

def printJoinRelations(self, plan, resultString):
    for i in range(len(plan)):     
        print("iteration", i)
        initialKey = list(plan.keys())[i]
        initialValue = plan[initialKey]

        if initialKey == 'Node Type':

            if "Join" in initialValue or "Nested" in initialValue:
                joinString = f"\n{initialValue} was used between "
                resultString = resultString + joinString
            
            if "Scan" in initialValue:
                scanString = f" ({initialValue})"

        elif initialKey == 'Relation Name':
            relationString = f"{initialValue}" + scanString
            print(relationString)
            resultString = resultString + relationString
            
        elif initialKey == 'Plans':
            count = 0
            for arrays in initialValue:
                print(count)
                if count == 1:
                    resultString = resultString + " and "
                resultString = self.printJoinRelations(arrays, resultString)
                count+=1

    return resultString


# Compare the execution plans and identify any differences
def comparePlan(self, initialPlan, newPlan, added_analysis_text):
    textToReturn = ""
    added_analysis_text = added_analysis_text + "\n================================================================== \n"
    
    # print('initial: ', len(initialPlan))
    # print('new: ', len(newPlan))
    
    if (len(initialPlan) <= len(newPlan)):
        added_analysis_text =  added_analysis_text + str(initialPlan['Node Type']) 
        added_analysis_text =  added_analysis_text + "\n" + str("‾‾" * len(initialPlan['Node Type']))

        for i in range(len(initialPlan)):
            
            initialKey = list(initialPlan.keys())[i]
            initialValue = initialPlan[initialKey]
            # print("-----------------------------------------------------------")
            # print("Initial key:", initialKey)
            # print("Initial value:" , initialValue)

            

            for j in range(len(newPlan)):
                newKey = list(newPlan.keys())[j]
                newValue = newPlan[newKey]
                # print("New key:", newKey)
                # print("New value:" , newValue, "\n")
                
                # if they both have same keys, compare them
                if newKey == initialKey: 

                    if isinstance(newValue, list):
                        # print("Recursively going through Plans here: \n")
                        # added_analysis_text = added_analysis_text + "\n ================================================================== \n"
                        for dicts_count in range(len(newPlan['Plans'])):
                            # print("Comparing: \n", initialPlan['Plans'][dicts_count], "\n ==WITH== \n", newPlan['Plans'][dicts_count])
                            textToReturn = self.comparePlan(initialPlan['Plans'][dicts_count], newPlan['Plans'][dicts_count], added_analysis_text)
                    
                    if newValue != initialValue and newKey == "Startup Cost":
                        startupString = self.startupCostCompare(initialValue, newValue)
                        added_analysis_text = added_analysis_text + str(startupString)
                    
                    if newValue != initialValue and newKey == "Total Cost":
                        totalString = self.totalCostCompare(initialValue, newValue)
                        added_analysis_text = added_analysis_text + str(totalString)

                    if newValue != initialValue and newKey == "Plan Rows":
                        planRowString = self.planRowsCompare(initialValue, newValue)
                        added_analysis_text = added_analysis_text + str(planRowString)
                    
                    if newValue != initialValue and newKey != "Plans":
                        # added_analysis_text = added_analysis_text + "\n\n" + newKey + " of the initial query has changed from " + str(initialValue) + " to " + str(newValue) + " in the new query." 
                        textToReturn = added_analysis_text
                    

                    break
    

        # Return text
        return textToReturn

    #TODO: when initial plan > new Plan
    # else:
    #     added_analysis_text =  added_analysis_text + str(newPlan['Node Type']) 
    #     added_analysis_text =  added_analysis_text + "\n" + str("‾‾" * len(newPlan['Node Type']))

    #     for i in range(len(initialPlan)):
            
    #         initialKey = list(initialPlan.keys())[i]
    #         initialValue = initialPlan[initialKey]
    #         print("-----------------------------------------------------------")
    #         print("Initial key:", initialKey)
    #         print("Initial value:" , initialValue)

            

    #         for j in range(len(newPlan)):
    #             newKey = list(newPlan.keys())[j]
    #             newValue = newPlan[newKey]
    #             print("New key:", newKey)
    #             print("New value:" , newValue, "\n")
                
    #             # if they both have same keys, compare them
    #             if newKey == initialKey: 

    #                 # if isinstance(newValue, list):
    #                 #     print("Recursively going through Plans here: \n")
    #                 #     # added_analysis_text = added_analysis_text + "\n ================================================================== \n"
    #                 #     for dicts_count in range(len(newPlan['Plans'])):
    #                 #         print("Comparing: \n", initialPlan['Plans'][dicts_count], "\n ==WITH== \n", newPlan['Plans'][dicts_count])
    #                 #         textToReturn = self.comparePlan(initialPlan['Plans'][dicts_count], newPlan['Plans'][dicts_count], added_analysis_text)
                    
    #                 if newValue != initialValue and newKey == "Startup Cost":
    #                     startupString = self.startupCostCompare(initialValue, newValue)
    #                     added_analysis_text = added_analysis_text + str(startupString)
                    
    #                 if newValue != initialValue and newKey == "Total Cost":
    #                     totalString = self.totalCostCompare(initialValue, newValue)
    #                     added_analysis_text = added_analysis_text + str(totalString)

    #                 if newValue != initialValue and newKey == "Plan Rows":
    #                     planRowString = self.planRowsCompare(initialValue, newValue)
    #                     added_analysis_text = added_analysis_text + str(planRowString)
                    
    #                 if newValue != initialValue and newKey != "Plans":
    #                     # added_analysis_text = added_analysis_text + "\n\n" + newKey + " of the initial query has changed from " + str(initialValue) + " to " + str(newValue) + " in the new query." 
    #                     textToReturn = added_analysis_text
                    

    #                 break
    
    #     return textToReturn