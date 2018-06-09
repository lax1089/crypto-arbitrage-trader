from cycle import Cycle
from bittrex import Bittrex

import traceback
import time

try:
    from credentials import Credentials
except:
    print('You do not have a credentials.py file set up properly! Cannot load credentials.')

my_bittrex = Bittrex(Credentials.get_key(), Credentials.get_secret(), api_version='v2.0')

def get_curr_balance(currency):
    try:
        return float(my_bittrex.get_balance(currency)['result']['Available'])
    except:
        return 0.0

def execute_order(cycle, i, qty):
    market = cycle.marketCycle[i].get_code()
    #print(my_bittrex.get_order_history('BTC-NEO'))

    depth = cycle.marketCycle[i].get_depth_no_update()
    print ('reverse trade: '+str(cycle.reverseTrade[i]))

    if cycle.reverseTrade[i]:
        currRate = depth['bids'][0]['price']
        if qty != None:
            print('I was passed a qty, so I will only place an order for that qty of %f' % qty)
        else:
            qty = depth['bids'][0]['amount']
        print('Placing sell order on market %s for qty %f @ %f' % (market, qty* (1 - cycle.marketCycle[i].takerFee), currRate))
        #order_result = my_bittrex.trade_sell(market, 'LIMIT', qty * (1 - cycle.marketCycle[i].takerFee), currRate, 'GOOD_TIL_CANCELLED', None, 0.0)
        order_result = my_bittrex.trade_sell(market, 'LIMIT', qty , currRate, 'GOOD_TIL_CANCELLED', None, 0.0)
        new_qty = qty * currRate  * (1 - cycle.marketCycle[i].takerFee)
        #print(my_bittrex.trade_sell(market, 'MARKET', qty, 'GOOD_TIL_CANCELLED'))
    else:
        currRate = depth['asks'][0]['price']
        if qty != None:
            print('I was passed a qty, so I will only place an order for that qty of %f' % qty)
        else:
            qty = depth['asks'][0]['amount']
        print('Placing buy order on market %s for qty %f @ %f' % (market, qty/currRate* (1 - cycle.marketCycle[i].takerFee), currRate))
        order_result = my_bittrex.trade_buy(market, 'LIMIT', qty / currRate * (1 - cycle.marketCycle[i].takerFee), currRate, 'GOOD_TIL_CANCELLED', None, 0.0)
        #order_result = my_bittrex.trade_buy(market, 'LIMIT', qty / currRate, currRate, 'GOOD_TIL_CANCELLED', None, 0.0)
        new_qty = qty /  currRate * (1 - cycle.marketCycle[i].takerFee)
        #print(my_bittrex.trade_buy(market, 'MARKET', qty, 'GOOD_TIL_CANCELLED'))
    
    print(order_result)
    if order_result['success'] == True:
        print('Order was placed successfully')
        # Instead of returning True I should return the order identifier (UUID) so 
        # I can check when it was filled in the calling method
        return [new_qty+1, order_result['result']['OrderId']]
        #return 'e606d53c-8d70-11e3-94b5-425861b86ab6' example of what a UUID will look like
    else:
        print('Order was NOT placed successfully')
        # Instead of returning False I should return a string like 'ORDER_NOT_PLACED' 
        # that the calling method will recognize and know to abandon this chain
        return [-1,'ORDER_NOT_PLACED']

class CycleTrader(object):

    def executeCycle(cycle, new_qty):
        try:
            print('')
            print('## Executing cycle ##')
            print ('Starting with %f %s' % (get_curr_balance(cycle.leftCurrency(0)), cycle.leftCurrency(0)))
            
            for i in range(len(cycle.marketCycle)):
                #print('')
                print('Now want to utilize %s market to get %s' % (cycle.marketCycle[i].get_code(), cycle.rightCurrency(i)))
                
                myBalance = get_curr_balance(cycle.leftCurrency(i))
                print('My balance for %s is %f' % (cycle.leftCurrency(i), float(myBalance)))
                
                qty = min(new_qty, myBalance)
                print('new qty of %s is %f, balance is %f, using %f' % (cycle.leftCurrency(i), new_qty, myBalance, qty))
                
                # TODO: Should probably just pass the cycle to the below wrapper function call (execute_order) 
                # and then within that method extract the information I need (ie: reverseTrade, code, etc.)
                #get_curr_balance(cycle.marketCycle[i].currencies[1 if cycle.reverseTrade[i] else 0])
                [new_qty, order_uuid] = execute_order(cycle, i, qty)
                #print('I currently have %.8f of %s' % (get_curr_balance(cycle.marketCycle[i].currencies[1 if cycle.reverseTrade[i] else 0]), cycle.marketCycle[i].currencies[1 if cycle.reverseTrade[i] else 0]))
                if order_uuid != 'ORDER_NOT_PLACED':
                    print('Now need to keep checking order status on uuid %s and when it is filled, move to next part of cycle' % order_uuid)
                    # Loop 10 times sleeping for .5 seconds between each check on the order status.
                    # As soon as it is not open, we can assume it was filled and break out of this 
                    # loop, moving on to next part in the chain
                    isFilled = False
                    for i in range(1, 30):
                        print('iteration %d' % i)
                        order_check_result = my_bittrex.get_order(order_uuid)
                        print(order_check_result)
                        try: 
                            if order_check_result['result']['IsOpen'] == True:
                                print('Order still open, neet to keep waiting')
                            else:
                                print('Order filled! Move on to next part of the chain')
                                isFilled = True
                                break
                            time.sleep(.5)
                        except:
                            # If we encounter an exception here it is likely that the order check
                            # returned JSON which implied the order was not properly retrieved/found.
                            # Unless the return format of this API call changed, it would be very odd
                            # to have an exception here..
                            traceback.print_exc()
                            print('Problem getting order status, so exiting this chain :(')
                            return None
                    if isFilled == False:
                        print('I have finished waiting and order is still not filled :( ..aborting chain')
                        break
                else:
                    print('Order was not placed successfully so exiting this chain')
                    break
            print ('Ending with %f %s' % (get_curr_balance(cycle.leftCurrency(0)), cycle.leftCurrency(0)))
        except:
            traceback.print_exc()
            print('Encountered exception during the execution of cycle')
            

    
