from bs4 import BeautifulSoup


with open('test.xml','r') as f:
    data = f.read()

#print(data)

dmarc_data = BeautifulSoup(data,"xml")
#print(dmarc_data)py