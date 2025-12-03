public static class Program
{
    public static void Main()
    {
        using (var reader = new StreamReader("03.txt"))
        // using (var reader = new StreamReader("03.test.01.txt"))
        {
            var banks = new List<string>();
            while (!reader.EndOfStream)
            {
                banks.Add(reader.ReadLine()!);
            }

            Console.WriteLine($"Part 1: {Part1(banks)}");
            Console.WriteLine($"Part 2: {Part2(banks)}");
        }
    }

    static long Part1(List<string> banks) => banks.Select(b => MaxJoltage1(b).Max()).Sum();

    static IEnumerable<long> MaxJoltage1(string bank)
    {
        for (int i = 0; i < bank.Length; i++)
        {
            for (int j = i + 1; j < bank.Length; j++)
            {
                yield return Convert.ToInt32(new string(new char[] { bank[i], bank[j] }));
            }
        }
    }

    static long Part2(List<string> banks) => banks.Select(b => long.Parse(MaxJoltage(b, 12))).Sum();

    static string MaxJoltage(string bank, int pick)
    {
        var cache = new Dictionary<(int, int), string>();
        return MaxJoltageRec(cache, bank, 0, pick);
    }

    static string MaxJoltageRec(Dictionary<(int, int), string> cache, string bank, int start, int pick)
    {
        if (cache.TryGetValue((start, pick), out string val))
            return val;
        if ((bank.Length - start) - pick < 0)
            return "";
        if (pick == 0)
            return "";

        var opt1 = bank[start] + MaxJoltageRec(cache, bank, start + 1, pick - 1);
        var opt2 = MaxJoltageRec(cache, bank, start + 1, pick);
        if (opt2.Length == 0)
        {
            cache.Add((start, pick), opt1);
            return opt1;
        }
        if (Convert.ToInt64(opt1) > Convert.ToInt64(opt2))
        {
            cache.Add((start, pick), opt1);
            return opt1;
        }
        else
        {
            cache.Add((start, pick), opt2);
            return opt2;
        }
    }
}
