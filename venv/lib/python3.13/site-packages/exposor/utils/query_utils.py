
def query_parser(technology_files_content):
    #print(aa)
    #if isinstance(technology_files_content, dict):
    #    data = [technology_files_content]
    for index, item_list in enumerate(technology_files_content):
        #Logging could happen
        #print(f"Entry {index+1}:")
        if isinstance(item_list, list):
            for entry in item_list:
                info = entry.get('info',{})
                print(info['cpe'])
                queries = entry.get('queries',{})
                # logging maybe that all is okay
                print(queries)
        else:
            info = item_list.get('info',{})
            queries = item_list.get('queries',{})
            # logging maybe that all is okay
            print(info['cpe'])
            print(queries)