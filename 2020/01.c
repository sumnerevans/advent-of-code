#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct long_list {
    size_t length;
    size_t data_size;
    long long *data;
};

struct long_list long_list_new_sized(size_t data_size)
{
    struct long_list list;
    list.length = 0;
    list.data_size = data_size;
    list.data = calloc(sizeof(long long), list.data_size);
    return list;
}

struct long_list long_list_new() { return long_list_new_sized(1); }

void long_list_add(struct long_list *list, long long element)
{
    if (list->length == list->data_size) {
        // Need to allocate a larger list.
        long long *newdata = calloc(sizeof(long long), list->data_size * 2);
        memcpy(newdata, list->data, sizeof(long long) * list->data_size);
        list->data_size *= 2;
        free(list->data);
        list->data = newdata;
    }

    list->data[list->length] = element;
    list->length++;
}

void print_long_list(struct long_list list)
{
    printf("[");
    for (int i = 0; i < list.length; i++) {
        if (i > 0) printf(", ");
        printf("%lld", list.data[i]);
    }
    printf("]\n");
}

int main()
{
    struct long_list numbers = long_list_new();

    long long num;
    while (scanf("%lld", &num) >= 0) {
        long_list_add(&numbers, num);
    }

    long long ans1, ans2;
    for (int i = 0; i < numbers.length; i++) {
        for (int j = 0; j < numbers.length; j++) {
            if (numbers.data[i] + numbers.data[j] == 2020) ans1 = numbers.data[i] * numbers.data[j];

            for (int k = 0; k < numbers.length; k++) {
                if (numbers.data[i] + numbers.data[j] + numbers.data[k] == 2020)
                    ans2 = numbers.data[i] * numbers.data[j] * numbers.data[k];
            }
        }
    }

    printf("Part 1:\n%lld\n", ans1);
    printf("Part 2:\n%lld\n", ans2);
    return 0;
}
