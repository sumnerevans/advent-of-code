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

    static long Part1(List<string> banks) => banks.Select(b => long.Parse(MaxJoltage(b, 2))).Sum();

    static long Part2(List<string> banks) => banks.Select(b => long.Parse(MaxJoltage(b, 12))).Sum();

    static string MaxJoltage(string bank, int pick) =>
        MaxJoltageRec(new Dictionary<(int, int), string>(), bank, 0, pick);

    static string MaxJoltageRec(IDictionary<(int, int), string> cache, string bank, int start, int pick)
    {
        if (cache.TryGetValue((start, pick), out string cached))
            return cached;
        if ((bank.Length - start) - pick < 0)
            return "";
        if (pick == 0)
            return "";

        string withCurrentChar = bank[start] + MaxJoltageRec(cache, bank, start + 1, pick - 1);
        string withoutCurrentChar = MaxJoltageRec(cache, bank, start + 1, pick);
        string selected =
            (withoutCurrentChar.Length == 0 || Convert.ToInt64(withCurrentChar) > Convert.ToInt64(withoutCurrentChar))
                ? withCurrentChar
                : withoutCurrentChar;
        cache.Add((start, pick), selected);
        return selected;
    }
}
