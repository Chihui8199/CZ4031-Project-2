

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