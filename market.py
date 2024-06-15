import requests
import json

class market:
    url = 'https://api.warframe.market/v1/items/'
    error = False

    def __init__(self, item, test=False):
        self.item = item
        response = None
        if test:
            with open('test/high_voltage_response1.json') as f:
                response = json.load(f)
        else:
            response = self.getOrders()
        if 'error' in response:
            print('Error trying to fetch ' + self.item)
            self.error = True
        else:
            self.orders = self.sortResponse(response)
    
    def getOrders(self):
        response = requests.get(self.url + self.item.lower() + '/orders')
        return response.json()

    def sortResponse(self, response):
        sellOrders = []
        for order in response['payload']['orders']:
            if (order['order_type'] == 'sell') and (order['user']['status'] == 'ingame') and (order['platform'] == 'pc'):
                sellOrders.append(order)
        sellOrders.sort(key=lambda x: x['platinum'])
        return sellOrders
    
    def getLowestPrices(self, quantity):
        prices = []
        for i in range(quantity):
            prices.append(self.getPrice(i))
        return prices
    
    def getPrice(self, index):
        return self.orders[index]['platinum']
    
    def getQuantity(self):
        return len(self.orders)