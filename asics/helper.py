def operate_list(test_list):
    formatted_output = ""
    for i, element in enumerate(test_list):
        formatted_output += element
        if i != len(test_list) - 1:
            formatted_output += ", "
    return formatted_output

def generate_query(data, schema, table, offset):

    col_list = data['data']
    clist = []
    for c in col_list:
        clist.append(c['colname'])
    
    cols = operate_list(clist)
    query = f"select {cols} from {schema}.{table} limit 50 OFFSET {offset}"
    return query 
    
def config_str_to_list(input_string):
    input_string = input_string[1:-1]
    output_list1 = input_string.split(",")
    output_list2 = []
    for i in output_list1:
        i=i.strip()
        i=i.strip("'")
        output_list2.append(i)
    del output_list1
    del input_string
    return output_list2