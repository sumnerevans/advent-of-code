public static class ExtEnumerable
{
    public static IEnumerable<long> Range(long start, long end)
    {
        for (long i = start; i <= end; i++)
        {
            yield return i;
        }
    }

    public static IEnumerable<int> Range(int start, int end)
    {
        for (int i = start; i <= end; i++)
        {
            yield return i;
        }
    }
}

public static class Program2
{
    readonly record struct Range(long Start, long End);

    public static void MainLinq()
    {
        using (var reader = new StreamReader("02.txt"))
        // using (var reader = new StreamReader("02.test.01.txt"))
        {
            var ranges = reader
                .ReadLine()!
                .Split(",")
                .Where(s => !string.IsNullOrWhiteSpace(s))
                .Select(s =>
                {
                    var parts = s.Split("-");
                    return new Range(long.Parse(parts[0]), long.Parse(parts[1]));
                })
                .ToList();

            Console.WriteLine($"Part 1: {Part1(ranges)}");
            Console.WriteLine($"Part 2: {Part2(ranges)}");
        }
    }

    static long Part1(List<Range> ranges) => ranges.SelectMany(InvalidPart1).Sum();

    static IEnumerable<long> InvalidPart1(Range range) =>
        ExtEnumerable
            .Range(range.Start, range.End)
            .Where(i =>
            {
                string num = i.ToString();
                return num.Length % 2 == 0 && num.Substring(0, num.Length / 2) == num.Substring(num.Length / 2);
            });

    static long Part2(List<Range> ranges) => ranges.SelectMany(InvalidPart2).Sum();

    static IEnumerable<long> InvalidPart2(Range range) =>
        ExtEnumerable
            .Range(range.Start, range.End)
            .Where(i =>
            {
                string num = i.ToString();
                return ExtEnumerable
                    .Range((int)1, num.Length / 2)
                    .Any(length =>
                    {
                        string first = num.Substring(0, length);
                        return num.Skip(length).Chunk(length).Select(c => new string(c)).All(c => c == first);
                    });
            });
}
