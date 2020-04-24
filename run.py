from werkenntdenbesten import *
from google_scrape import *
from helper import *

head_row = ['Link', 'Wordpress', 'Invalid SSL', 'gtmetrix PageSpeed Score', 'YSlow Score', 'Fully Loaded Time']

if __name__ == "__main__":
    print("This application checks if a website has wordpress, has invalid SSL and gets stats from gtmetrix.")
    print("Enter 1 or 2 as per below: ")
    print("1) Find websites from Google: ")
    print("2) Find websites from werkenntdenbesten: ")
    ch = int(input())
    if ch == 1:
        word = input("Enter the keyword you want to search:  ")
        file_name = input("Enter the name of the file you want to save results as:  ")
        file_name = file_name + ".csv"
        tabulate_head(file_name, head_row)
        ls = search_links(word)
        print("Searching complete. Checking for conditions.")
        for l in ls:
            try:
                results = check(l)
                results_arr = []
                results_arr.append(results["link"])
                results_arr.append(results["is_wp"])
                results_arr.append(results["invalid_ssl"])
                if (results["gtmetrix"] != {}):
                    results_arr.append(results["gtmetrix"][["pagespeed_score"]])
                    results_arr.append(results["gtmetrix"][["yslow_score"]])
                    results_arr.append(results["gtmetrix"][["fully_loaded_time"]])
                print(results_arr)
                tabulate(file_name,results_arr)
            except:
                print("error in page: {}".format(l))
    elif ch == 2:
        trade = input("Enter the type of business you want to search from werkenntdenbesten: (To search all just press enter)")
        page_start = input("Enter the page number you want to start searching from: (Press enter if you don't know what to enter)")
        page_end = input("Enter the last page number you want to get information: (Press enter if you don't know what to enter)")
        file_name = input("Enter the name of the file you want to save results as:  ")
        file_name = file_name + ".csv"
        tabulate_head(file_name, head_row)
        if trade == '':
            trade = 'trade'
        if page_start == '':
            page_start = 1
        if page_end == '':
            page_end = 10
        links = search_all_trade(trade, page_start, page_end)
        print("Searching for websites...")
        business_links = []
        for link in links:
            business_links.append(get_website(link))
        print("Searching complete. Checking for conditions.")
        for business_link in business_links:
            try:
                results = check(business_link)
                results_arr = []
                results_arr.append(results["link"])
                results_arr.append(results["is_wp"])
                results_arr.append(results["invalid_ssl"])
                if (results["gtmetrix"] != {}):
                    results_arr.append(results["gtmetrix"][["pagespeed_score"]])
                    results_arr.append(results["gtmetrix"][["yslow_score"]])
                    results_arr.append(results["gtmetrix"][["fully_loaded_time"]])
                print(results_arr)
                tabulate(file_name,results_arr)
            except:
                print("error in page: {}".format(business_link))
    else:
        print("ex")