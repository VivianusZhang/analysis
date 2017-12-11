from strategies.Grid import find_grid_best_step, backtest_grid_on_one_day

if __name__ == '__main__':
    ''' maximize day end asset'''
    find_grid_best_step('002230', '2017/11/16')

    ''' minimize average '''
    #find_grid_best_step('300458', '2017/10/30', False)

    '''backtest on step'''
    #backtest_grid_on_one_day('002230', '2017/11/16', 0.5)