from markets._kraken_market_generator import KrakenMarketGenerator
from markets._bittrex_market_generator import BittrexMarketGenerator

from cycle import Cycle
from cyclegenerator import CycleGenerator
from cycletrader import CycleTrader

import time
import sys
import traceback

currency_filter = None;
return_threshold = 1.0
doPerformExecuteTrade = False

try:
    print ('Argument passed in for source currency filter: %s' % str(sys.argv[3]))
    currency_filter = str(sys.argv[3])
except:
    print ('No argument passed, defaulting to no filter on source currency')

try:
    print ('Argument passed in for return threshold: %s' % str(sys.argv[2]))
    return_threshold = float(sys.argv[2])
except:
    print ('No argument passed, defaulting to 1.0 return threshold')
        
#print('Only printing chains with a return greater than %f' % return_threshold)    

try: 
	print ('Argument passed in for doPerformExecuteTrade: %s' % str(sys.argv[1]))
	doPerformExecuteTrade = bool(sys.argv[1])
except:
	print ('No argument passed, defaulting to false for doPerformExecuteTrade (will not execute trades)')

#kraken = KrakenMarketGenerator()
#kraken_markets = kraken.get_markets(kraken.get_market_json())

def doIt():

    bittrex = BittrexMarketGenerator()
    bittrex_markets = bittrex.get_markets(bittrex.get_market_json())

#print('### KRAKEN MARKETS ###')
#kraken_markets.update_markets()
#for market in kraken_markets:
    #market.print_market()
    #print('bid %.12f' % market.get_bid())
    #print('ask %.12f' % market.get_ask())
    
#print('### BITTREX MARKETS ###')
#bittrex.update_markets(bittrex_markets)
#for market in bittrex_markets:
    #market.print_market()
    #print('bid %f' % market.get_bid())
    #print('ask %f' % market.get_ask())

    print('### BITTREX MARKETS ###')
    bittrex.update_markets(bittrex_markets)
    if (currency_filter != None):
        cycles = CycleGenerator.generateCycles(bittrex_markets, currency_filter)
    else:
        cycles = CycleGenerator.generateCyclesNoFilter(bittrex_markets)
     
    for c in cycles:
        print(Cycle.printCycle(c))
    cycleExecutionCount = 0
    for i in range(1,99999999999):
        time.sleep(1)
        sys.stdout.flush()
        if cycleExecutionCount > 5:
            return
        print(i, '==========')
        for c in cycles:
            if c.hasProblems:
                continue
            try:
                print(c)
                [taker, limit, noFeeRate, startingAmt] = c.calcTakerReturn()
                if taker > return_threshold:
                #if taker > 1.015 and limit > 0.5 and c.leftCurrency(0) == 'ETH':
    #            if taker > 1.015 and limit > 0.5:
                    print('')
                    print('Found a profitable cycle!')
                    print(Cycle.printCycle(c))
                    print('taker conversion factor: %f' % float(taker))
                    print('taker percentage %f%%' % float((taker-1)*100))
                    print('taker profit on 5k: %f' % float(taker*5000-5000))
                    print('taker limiting factor %f' % float(limit))
                    print('taker limited return %f' % float((taker*limit-limit)))
                    print('noFeeRate %f' % float(noFeeRate))
                    print('startingAmt %f' % float(startingAmt))
                    if doPerformExecuteTrade == True:
                        try: 
                            # below while condition needs to change, and may even need to be moved to the trade executer class
                            #while (taker > 1.015):
                            while (taker > return_threshold):
                                print('still profitable, executing cycle')
                                CycleTrader.executeCycle(c, startingAmt)
                                [taker, limit, noFeeRate, startingAmt] = c.calcTakerReturn()
                            print('no longer profitable, moving on to find another opportunity')
                        except:
                            traceback.print_exc()
                            print('Encountered exception when calling trade executor!')
                        cycleExecutionCount+=1
#                        return
                    else:
                        print('Not executing trades')
    #            else:
    #                print('taker not profitable')
    #            maker = c.calcMakerReturn()
    #            if maker > return_threshold:
    #                print('maker conversion factor %f' % float(maker))
    #                print('maker percentage %f%%' % float((maker-1)*100))
    #                print('maker profit on $5k: $%f' % float(maker*5000-5000))
    #            else:
    #                print('maker not profitable')
            except KeyboardInterrupt:
                return
            except:
                #traceback.print_exc()
                print(Cycle.printCycle(c))
                c.hasProblems = True
                print('Something went wrong in calculating/printing returns!')
                
doIt()
