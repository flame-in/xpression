from analysis.dbcode import retrieve_data



def data_retrieve_caller_sentiment(start_date, end_date, search_keyword):

    parameters = [search_keyword, start_date, end_date, "sentiment"]

    status, output = retrieve_data(*parameters)

    print(status)
    return output

def data_retrieve_caller_frontend(start_date, end_date, search_keyword):

    parameters = [search_keyword, start_date, end_date, "frontend"]

    status, output = retrieve_data(*parameters)

    print(status)
    return output



# if __name__ == "__main__":


    # sentiment values  format

    """
    v = {
        "_id": "1415038672991399937",
        "sentiment_data":
            {
                "cleaned_text": 1,
                "scores": 2,
                "ranking": 3
                "label": ['negative', 'neutral', 'positive']
            }
    }
    status = insert_sentiment_data(v)
    print(status)
    """
    


    # input to data retrieval
    """
    print("yyyy/mm/dd")
    start_date = input("start_date: ")
    end_date = input("end_date: ")
    search_keyword = input("keyword: ").strip().lower()
    
    # data_retrieve_caller_sentiment(start_date, end_date, search_keyword)
    data_retrieve_caller_frontend(start_date, end_date, search_keyword)
    """

    # 1
    # to print data that we have of a specific keyword
    # print(total_data_of_keyword(search_keyword))


