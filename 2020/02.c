#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int str_count(char *str, char look)
{
    int i = 0;
    int count = 0;
    while (str[i] != '\0') {
        if (str[i] == look) count++;
        i++;
    }
    return count;
}

int main()
{
    int low, high;
    char c;
    char password[100];

    long long ans1 = 0;
    long long ans2 = 0;

    while (scanf("%d-%d %c: %s", &low, &high, &c, password) >= 0) {
        int count = str_count(password, c);
        if (low <= count && count <= high) ans1++;
        if ((password[low - 1] == c) ^ (password[high - 1] == c)) ans2++;
    }

    printf("Part 1:\n%lld\n", ans1);
    printf("Part 2:\n%lld\n", ans2);
    return 0;
}
