logging = False
class Cycle(object):
    def __init__(self, marketCycle, reverseTrade):
        self.marketCycle = marketCycle
        self.reverseTrade = reverseTrade
        self.hasProblems = False

    def __str__(self):
        ret = self.leftCurrency(0)
        for i in range(len(self.marketCycle)):
            ret += '->'
            ret += self.rightCurrency(i)
        return ret

    def leftCurrency(self, i):
        return self.marketCycle[i].currencies[0 if self.reverseTrade[i] else 1]

    def rightCurrency(self, i):
        return self.marketCycle[i].currencies[1 if self.reverseTrade[i] else 0]

    def calcTakerReturn(self):
        rate = 1.0
        noFeeRate = 1.0
        startingQty = 9999999999
        qty = 9999999999
        cycleRecord = ''
        for i in range(0, len(self.marketCycle)):
            depth = self.marketCycle[i].get_depth()
            cycleRecord += self.leftCurrency(i)
            cycleRecord += '->'
            cycleRecord += self.rightCurrency(i)
            if self.reverseTrade[i]:
                currRate = depth['bids'][0]['price']  * (1 - self.marketCycle[i].takerFee)
                qty = min(qty*currRate,depth['bids'][0]['amount']/currRate)
                noFeeRate *= 1.0 / depth['bids'][0]['price']
                startingQty = min(startingQty*currRate,depth['bids'][0]['amount']*depth['bids'][0]['price'])
                cycleRecord += ' ::'
                cycleRecord += ' currRate: '
                cycleRecord += str(currRate)
                cycleRecord += ' qty: '
                cycleRecord += str(qty)
                cycleRecord += ' noFeeRate: '
                cycleRecord += str(noFeeRate)
                cycleRecord += ' startingQty: '
                cycleRecord += str(startingQty)
            else:
                currRate = 1.0 / depth['asks'][0]['price'] * (1 - self.marketCycle[i].takerFee)
                qty = min(qty*currRate,depth['asks'][0]['amount']*currRate)    
                noFeeRate *= depth['asks'][0]['price']
                startingQty = min(startingQty*currRate,depth['asks'][0]['amount']*depth['asks'][0]['price'])
                cycleRecord += ' ::'
                cycleRecord += ' currRate: '
                cycleRecord += str(currRate)
                cycleRecord += ' qty: '
                cycleRecord += str(qty)
                cycleRecord += ' noFeeRate: '
                cycleRecord += str(noFeeRate)
                cycleRecord += ' startingQty: '
                cycleRecord += str(startingQty)
            rate *= currRate
            cycleRecord += ' -- rate*=currRate: '
            cycleRecord += str(rate)
            if logging:
                print(cycleRecord)
            cycleRecord = ''
        if logging:
            print(cycleRecord)
        return [rate, qty/rate, noFeeRate, startingQty/noFeeRate]

    def calcMakerReturn(self):
        rate = 10000
        for i in range(0, len(self.marketCycle)):
            depth = self.marketCycle[i].get_depth()
            if self.reverseTrade[i]:
                rate *= 1.0 / (depth['bids'][0]['price'] + self.marketCycle[i].priceOffset)
                #*    (1 - self.marketCycle[i].makerFee)
            else:
                rate *= (depth['asks'][0]['price'] - self.marketCycle[i].priceOffset)
                #*    (1 - self.marketCycle[i].makerFee)
        return rate / 10000

    def reverse(self):
        return Cycle(list(reversed(self.marketCycle)), [not i for i in reversed(self.reverseTrade)])

    def rotate(self, pivots):
        for pivot in pivots:
            if self.marketCycle[0].currencies[0 if self.reverseTrade[0] else 1] == pivot:
                return self
            for i in range(1,len(self.marketCycle)):
                if self.marketCycle[i].currencies[0 if self.reverseTrade[i] else 1] == pivot:
                    return Cycle(self.marketCycle[i:] + self.marketCycle[:i], self.reverseTrade[i:] + self.reverseTrade[:i])
        return self

    def printCycle(c):
    #        print('match '+c.marketCycle[0].code+' '+c.marketCycle[1].code+' '+c.marketCycle[2].code+' '+str(c.reverseTrade[0])+' '+str(c.reverseTrade[1])+' '+str(c.reverseTrade[2]))
        try:
    #        ret = c.marketCycle[0].currencies[0 if c.reverseTrade[0] else 1]
    #        for i in range(len(c.marketCycle)):
    #            ret += '->'
    #            ret += c.marketCycle[i].currencies[1 if c.reverseTrade[i] else 0]
            return str(c)
        except:
            traceback.print_exc()
            return 'Problem in cycle detection'
