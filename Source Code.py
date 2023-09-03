from requests_html import HTMLSession
import csv

session = HTMLSession()
home = session.get('https://egypt.yallamotor.com/used-cars')


#get all brands
all_brands = home.html.find('#makesListing > div > div.brandsContainer.m32t.make-list.p8b')
all_brand_extend = home.html.find('#makesListing > div > div.brandsContainer.make-list.expandbtn')
brands = []
for brand in all_brands :
    brands.append(brand.text)

for brand in all_brand_extend :
    brands.append(brand.text)

brands = [b.split('\n') for b in brands]
brands_list = []
for b in brands :
    brands_list.extend(b)

brands_list = [b.lower() for b in brands_list]

# max pages
max_pages = []
for brand in brands_list:
    brand_page = session.get(f'https://egypt.yallamotor.com/used-cars/{brand}')
    try:
        num_cars = brand_page.html.find('#mainContent > div:nth-child(17) > div > div.col.is-8.p0.p4r > div.m20t.m12b.color-gray.text-center > b:nth-child(2)',first = True).text
        max_pages.append (int(float(num_cars)/12)+1)
        
    except:
        max_pages.append(1)
print(len(brands_list) , len(max_pages))


# combine brand with its max page to complete all cars in site 

combine = {}
car_id=1
for i in range(len(brands_list)):
    combine[brands_list[i]] = max_pages[i]

# write data in csv file
with open('cars data.csv' , 'w',encoding="utf-8",newline='') as file : 
    writer = csv.writer(file)
    writer.writerow(['id', 'car_name' , 'brand' , 'model' , 'kilometers_driven' , 'transmision' , 'fuel' , 'color','engine_capacity','price'])
    for brand , max_page in combine.items():
        for i in range(1,max_page+1):
            site = session.get(f'https://egypt.yallamotor.com/used-cars/{brand}?page={i}&sort=updated_desc')
            

            cars_dev = site.html.find('#mainContent > div:nth-child(17) > div > div.col.is-8.p0.p4r > div:nth-child(2) > div')
            
            for cars in cars_dev :
                try :

                    car_url = list(cars.absolute_links)

                    # because of absolute_links has dinamic sort with every request i handled it with this piece of code
                    splited  = [l.split('/') for l in car_url]
                    link = [l for l in splited if l[2] == 'egypt.yallamotor.com' and len(l)>7][0]
                    
                    url = "/".join(link)
                    # --------------------------------------------------------------------

                    car = session.get(url)
                    try :
                        car_name = car.html.xpath('//*[@id="overviewnav"]/div[1]/h1',first = True).text
                    except:
                        car_name = ''

                    try :
                        car_model = car.html.xpath('//*[@id="highlightsnav"]/div[1]/div[2]/div[1]/div[3]',first = True).text
                    except:
                        car_model = ''

                    try:
                        car_kilometers = car.html.xpath('//*[@id="highlightsnav"]/div[1]/div[2]/div[2]/div[3]',first = True).text
                    except:
                        car_kilometers = ''

                    try:
                        car_transmission = car.html.xpath('//*[@id="highlightsnav"]/div[1]/div[2]/div[4]/div[3]',first = True).text
                    except:
                        car_transmission = ''

                    try :
                        fuel = car.html.xpath('//*[@id="highlightsnav"]/div[1]/div[3]/div[1]/div[3]',first = True).text
                    except :
                        fuel = ''

                    try :
                        color = car.html.xpath('//*[@id="highlightsnav"]/div[1]/div[3]/div[2]/div[3]',first = True).text
                    except:
                        color = ''

                    try :
                        engine_capacity = car.html.xpath('//*[@id="highlightsnav"]/div[3]/div/div[1]/div[4]/div[2]',first = True).text
                    except:
                        engine_capacity = ''

                    try:
                        price = car.html.xpath('//*[@id="mainContent"]/div[3]/div/div[2]/div[1]/div[1]/div/span',first = True).text
                    except:
                        price = ''

                    car_brand = brand

                    id = car_id

                    writer.writerow([id, car_name , car_brand , car_model , car_kilometers , car_transmission , fuel , color , engine_capacity , price])
                    
                    print (id , "\n---------------------------------------------")
                    car_id+=1
                except:
                    print("ads")



