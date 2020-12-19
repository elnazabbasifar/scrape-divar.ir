from bs4 import BeautifulSoup 
import requests
import json

def __parse_html(url):

    try:
        response = requests.get(url)

    except Exception as err:
        print('Other error occurred: {}'.format(err))
    else:
        # Succeed
        soup = BeautifulSoup(response.content, "html.parser") 
        return soup

def find_categories(root, parent=0):
    """
    Method to get categories and subcategories recursively
    """
    soup = __parse_html(root)
    # Find the categories' container "ul"
    category_ul = soup.find('ul', {'class':'kt-accordion'})
    # Extract the list of categories in order to reach the lowest ul categories
    for i in range(parent):
        sub_ul = category_ul.find_all('ul')
        if sub_ul:  category_ul = sub_ul[0]
        else:   return []

    results= []
    for li in category_ul.contents:
        # Get name of category
        category_name = li.a.get_text()

        print(parent*'   ' + category_name)

        url =  '{0}{1}'.format('https://divar.ir', li.a.get('href'))
        results.append({
            "name": category_name,
            "url": url,
            "subcategories": find_categories(url, parent+1),
        })
    return results

def write_to_file(data):

    with open("output.json", 'w') as f:
        # f.write("\n")
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():

    data =find_categories('https://divar.ir/s/tehran')
    write_to_file(data)
    
if __name__ == "__main__":
    # Run script
    main()   