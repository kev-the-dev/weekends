#include <iostream>

template<typename T>
void print_array(T* arr, size_t size)
{
    // Handle empty array edge case
    if (size == 0) return;

    // Print all but last
    for (size_t i = 0; i < size - 1; ++i)
    {
        std::cout << arr[i] << ',';
    }

    // Print last element
    std::cout << arr[size - 1] << std::endl;
}

template<typename T>
size_t partition(T* arr, size_t size)
{
    
}


template<typename T>
void quicksort(T* arr, size_t size)
{
    // Basecast, size 1 array is sorted
    if (size == 1) return;

    size_t i = partition(array, size);

    // Recurse w/ two subarrays, consider of by ones 
    // [0, partition]
    quicksort(arr, i);
    // [partition + 1, size]
    quicksort(arr + i, size - i);
}

int main()
{
    int x[5] = {5, 3, 1, 2, 4};
    print_array(&x[0], 5);
    quicksort(&x[0], 5);
    print_array(&x[0], 5);
}
