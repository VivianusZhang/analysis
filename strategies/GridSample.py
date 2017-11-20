from strategies.Grid import find_grid_best_step, backtest_grid_on_one_day

if __name__ == '__main__':
    ''' maximize day end asset'''
    find_grid_best_step('002001', '2017/10/30')

    ''' minimize average '''
    find_grid_best_step('002001', '2017/10/30')

    '''backtest on step'''
    backtest_grid_on_one_day('002001', '2017/10/30', 0.03)