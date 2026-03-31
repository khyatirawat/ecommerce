def quicksort_products(products, low=0, high=None, ascending=True):
    if high is None:
        high = len(products) - 1

    def partition(arr, low, high):
        pivot = arr[high]['price']
        i = low - 1
        for j in range(low, high):
            if (arr[j]['price'] <= pivot and ascending) or (arr[j]['price'] >= pivot and not ascending):
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    if low < high:
        pi = partition(products, low, high)
        quicksort_products(products, low, pi - 1, ascending)
        quicksort_products(products, pi + 1, high, ascending)

    return products