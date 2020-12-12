from bs4 import BeautifulSoup 
import requests
import json

class DivarParser():

    def __init__(self):

       self.visited_links = []
       self.results = []
       self.parent_counter = 0

    def get_soup(self, url):

        try:
            response = requests.get(url)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
            # None
        except HTTPError as http_err:
            print('HTTP error occurred: {}'.format(http_err))

        except Exception as err:
            print('Other error occurred: {}'.format(err))
        else:
            # Succeed
            soup = BeautifulSoup(response.content, "html.parser") 
            return soup

    def find_categories(self, root):
        """
        Method to get categories and subcategories recursively
        """
        if root in self.visited_links:  return
        
        else:   self.visited_links.append(root)
        
        soup = self.get_soup(root)

        # Find the categories' container "ul"
        category_ul = soup.find('ul', {'class':'kt-accordion'})

        # if there is no subcategory, stop searching
        if category_ul is None: return 
        
        # Extract the list of categories
        categories_li = category_ul.find_all('li')
        
        # Specify the base url for the url passed into the function
        base_url = 'https://divar.ir'

        # Extract the details for each category:Persian name , url
        for item in categories_li:
            
            # generate the category link
            url = '{0}{1}'.format(base_url, item.a.get('href'))

            # if this link has been seen before, skip
            if url in self.visited_links:   continue
            
            # create a new dict to keep details of each category
            details_dict = {
                # add the category name
                'name': item.a.get_text(),                           
                'url': url
            }
            parents = self.parent_counter  
              
            # Print categories' name like a tree structure
            print(parents * '  ' + details_dict['name'])
            
            # Create a list to save the output as a json file
            self.results.append(details_dict)            

            self.parent_counter += 1

            # find the subcategories for each category recursively
            self.find_categories(details_dict['url'])

            self.parent_counter -= 1
        
        return self.results
    
    def write_to_file(self, data):

        with open("output.json", 'w') as f:
            # f.write("\n")
            json.dump(data, f, indent=4, separators=(',', ': '), ensure_ascii=False)

def main():

    divar_scrapper = DivarParser()
    #divar_scrapper()
    data =divar_scrapper.find_categories('https://divar.ir/s/tehran')
    # print(data)
    divar_scrapper.write_to_file(data)
    
if __name__ == "__main__":
    # Run script
    main()    

    
    
