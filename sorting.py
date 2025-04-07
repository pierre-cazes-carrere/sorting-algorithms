
class SortingAlgorithm:
    def sort(self, arr):
        raise NotImplementedError

class HeapSort(SortingAlgorithm):
    def sort(self, arr):
        def heapify(arr, n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n and arr[left] > arr[largest]:
                largest = left
            if right < n and arr[right] > arr[largest]:
                largest = right
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(arr, n, largest)

        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, n, i)
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            heapify(arr, i, 0)

class CombSort(SortingAlgorithm):
    def sort(self, arr):
        gap = len(arr)
        shrink = 1.3
        sorted = False
        while not sorted:
            gap = int(gap / shrink)
            if gap <= 1:
                gap = 1
                sorted = True
            i = 0
            while i + gap < len(arr):
                if arr[i] > arr[i + gap]:
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    sorted = False
                i += 1

class QuickSort(SortingAlgorithm):
    def sort(self, arr):
        def quick_sort_recursive(arr):
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]
            return quick_sort_recursive(left) + middle + quick_sort_recursive(right)
        arr[:] = quick_sort_recursive(arr)

class MergeSort(SortingAlgorithm):
    def sort(self, arr):
        def merge_sort_recursive(arr):
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left_half = merge_sort_recursive(arr[:mid])
            right_half = merge_sort_recursive(arr[mid:])
            return merge(left_half, right_half)

        def merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result

        arr[:] = merge_sort_recursive(arr)
