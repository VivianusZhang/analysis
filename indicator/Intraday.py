def vwap(data):
    total_volume = 0
    total_amount = 0
    for _ in data:
        total_volume = total_volume + _['volume'] * 100
        total_amount = total_amount + _['amount']

    return total_amount / total_volume
