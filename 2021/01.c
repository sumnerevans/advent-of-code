#include <stdio.h>

#define ll long long
#define getlong(VAR) scanf("%lld", &VAR)

int main() {
  ll ans1 = 0;
  ll ans2 = 0;

  ll num = 0;
  ll threebefore;
  ll twobefore;
  ll onebefore;
  getlong(onebefore);

  int i = 0;
  while (getlong(num) >= 0) {
    if (i >= 2 && num > threebefore) {
      ans2++;
    }
    i++;
    if (num > onebefore) {
      ans1++;
    }
    threebefore = twobefore;
    twobefore = onebefore;
    onebefore = num;
  }

  printf("Answer Part 1: %lld\n", ans1);
  printf("Answer Part 2: %lld\n", ans2);
  return 0;
}
