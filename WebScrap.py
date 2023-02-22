import requests
from bs4 import BeautifulSoup
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="Scrapping"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS practise_scrap(id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255), link_title VARCHAR(255), image_url TEXT, paragraph TEXT , publish_date VARCHAR(255), updated_date VARCHAR(255))")


urls = 'https://www.jagran.com/news/national-news-hindi.html?itm_medium=national&itm_source=dsktp&itm_campaign=navigation'
r = requests.get(urls)
htmlContent = r.content

soup = BeautifulSoup(htmlContent,'html.parser')

link = soup.find_all('article',{'class':'topicBox'})
for anchor in link:
    anchor=soup.find_all('a')
    for a in anchor:
        if a.has_attr('href')  and 'news/national-news-hindi' in a['href']:
            pass
        elif a.has_attr('href')  and 'news/national-' in a['href']:
            url =  "https://www.jagran.com" + a['href']
            # print(url)
            # print("--------------------------------------------------------------------------------------------------")

            if url:
                print(" Page Url:  ",url)
                print("------------------------------------------------------------------------------------------------------")

                link_resp=requests.get(url)

                link_soup=BeautifulSoup(link_resp.content,'html.parser')


                link_title = link_soup.find('title')
                print("Linked Page title text: ",link_title.text)


                link_image=link_soup.find_all('img')
                image_url = []
                for img in link_image:
                    try:
                        print("Linked page image url:",image_url)
                        image_url.append(img['src'])
                    except KeyError:
                        pass


                link_parag=link_soup.find_all('p')
                paragraph =[]
                for p in link_parag:
                    print("linked Paragraph :  ", p.text)
                    paragraph.append(p.text.strip())
                print('----Full paragraph is here :', paragraph)
 
            #     # date is not working properly
                link_date=link_soup.find_all('span',{'class':'date'})
                # if link_date:
                #     if "Publish" or "Update" in link_date:
                #         print("linked page publish date: ",link_date)
                for span in link_date:
                        text = span.get_text()
                        if 'Publish Date:' in text:
                            publish_date = text.replace('Publish Date:','').strip()
                            print('Publish Date:', publish_date)
                        elif 'Updated Date:' in text:
                            updated_date = text.replace('Updated Date:','').strip()
                            print('Updated Date:', updated_date)
                print("==================================================================================================================")


                sql = "INSERT INTO practise_scrap(url, link_title, image_url, paragraph, publish_date, updated_date) VALUES (%s, %s, %s, %s, %s, %s)"
                # val = (url, link_title, image_url, paragraph, publish_date, updated_date)
                val = (url, link_title.text if link_title else None, '\n\n '.join(image_url)  , '\n\n '.join(paragraph), publish_date, updated_date)
                mycursor.execute(sql, val)
                mydb.commit()

        print('Data successfully inserted into database.')












