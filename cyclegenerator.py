from cycle import Cycle

class CycleGenerator(object):

    def generateCyclesNoFilter(markets):

        cycles = []
        counter = 0

        for index1 in range(len(markets)):
            markets[index1].print_market()
            for index2 in range(index1+1, len(markets)):
                for i in range(2):
                    for j in range(2):
                        if markets[index1].currencies[1-i] == markets[index2].currencies[j]:
                            for index3 in range(index2+1, len(markets)):
                                for k in range(2):
                                    if markets[index2].currencies[1-j] == markets[index3].currencies[k] and markets[index1].currencies[i] == markets[index3].currencies[1-k]:
                                        print('match '+markets[index1].code+' '+markets[index2].code+' '+markets[index3].code+' '+str(i==0)+' '+str(j==0)+' '+str(k==0))
                                        currCycle = Cycle([markets[index1], markets[index2], markets[index3]], [(i==0), (j==0), (k==0)]).rotate(['ETH','BTC','USDT'])
                                        # if currCycle.leftCurrency(0) == 'ETH' and (currCycle.leftCurrency(1) == 'USDT' or currCycle.leftCurrency(2) == 'USDT'):
                                        if 1 == 1: 
                                            cycles+=[currCycle, currCycle.reverse()]
                                        counter+=1
        print('counter %d' %counter)
        return cycles

    def generateCycles(markets, currencyFilter):

        cycles = []
        counter = 0

        for index1 in range(len(markets)):
            markets[index1].print_market()
            if (markets[index1].get_sourceCurrency() == currencyFilter):
                for index2 in range(index1+1, len(markets)):
                    for i in range(2):
                        for j in range(2):
                            if markets[index1].currencies[1-i] == markets[index2].currencies[j]:
                                for index3 in range(index2+1, len(markets)):
                                    for k in range(2):
                                        if markets[index2].currencies[1-j] == markets[index3].currencies[k] and markets[index1].currencies[i] == markets[index3].currencies[1-k]:
                                            print('match '+markets[index1].code+' '+markets[index2].code+' '+markets[index3].code+' '+str(i==0)+' '+str(j==0)+' '+str(k==0))
                                            currCycle = Cycle([markets[index1], markets[index2], markets[index3]], [(i==0), (j==0), (k==0)]).rotate(['ETH','BTC','USDT'])
                                            # if currCycle.leftCurrency(0) == 'ETH' and (currCycle.leftCurrency(1) == 'USDT' or currCycle.leftCurrency(2) == 'USDT'):
                                            if 1 == 1: 
                                                cycles+=[currCycle, currCycle.reverse()]
                                            counter+=1
        print('counter %d' %counter)
        return cycles

