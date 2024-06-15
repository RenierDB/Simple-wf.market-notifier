import json
import market
import time



print('>>Market bot started!\n\n')



class jsonHandler:
    def __init__(self, path, part):
        self.config = self._read(path)
        self.part = part

    def _read(self, path):
        with open(path) as config_file:
            config = json.load(config_file)
            return(config)
        
    def getLength(self):
        return len(self.config[self.part])
    
    def getRecord(self, index):
        return self.config[self.part][index]
    
class checkMarket:
    def __init__(self, item, sellprice, buyprice):
        self.item = item
        self.sellprice = sellprice
        self.buyprice = buyprice
        self.market = market.market(item)

    def checkError(self):
        return self.market.error
    
    def checkSell(self):
        if self.market.getPrice(0) >= self.sellprice:
            return True
        else:
            return False
        
    def checkBuy(self):
        if self.market.getPrice(0) <= self.buyprice:
            return True
        else:
            return False
        
    def checkSellWarning(self):
        prices = self.market.getLowestPrices(5)
        for price in prices:
            if price < self.sellprice:
                return True
        return False
    
    def checkBuyWarning(self):
        prices = self.market.getLowestPrices(5)
        for price in prices:
            if price > self.buyprice:
                return True
        return False



stop = False

print('>>Reading config...\n\n')    
fileHandler = jsonHandler('config.json', 'items')
print('>>Config read!\n\n')

print('>>Checking market...\n\n')
for i in range(fileHandler.getLength()):
    record = fileHandler.getRecord(i)
    checker = checkMarket(record['name'], record['sellprice'], record['buyprice'])
    if not checker.checkError():
        if checker.checkSell():
            print('>>Sell ' + record['name'] + ' for ' + str(record['sellprice']) + ' platinum!\n')
            stop = True
            if checker.checkSellWarning():
                print('>>Warning!')
        elif checker.checkBuy():
            print('>>Buy ' + record['name'] + ' for ' + str(record['buyprice']) + ' platinum!\n')
            stop = True
            if checker.checkBuyWarning():
                print('>>Warning!')
    time.sleep(5)
print('\n\n>>Market checked!\n\n')

if stop:
    print(">>There are important notifications!")
    input()