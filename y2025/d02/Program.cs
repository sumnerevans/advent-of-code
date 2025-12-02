public static class Program
{
    readonly record struct Range(long Start, long End);

    public static void Main()
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

    static IEnumerable<long> InvalidPart1(Range range)
    {
        for (long i = range.Start; i <= range.End; i++)
        {
            string num = i.ToString();
            if (num.Length % 2 != 0)
                continue;

            if (num.Substring(0, num.Length / 2) == num.Substring(num.Length / 2))
                yield return i;
        }
    }

    static long Part2(List<Range> ranges) => ranges.SelectMany(InvalidPart2).Sum();

    static IEnumerable<long> InvalidPart2(Range range)
    {
        for (long i = range.Start; i <= range.End; i++)
        {
            string num = i.ToString();

            for (int length = 1; length <= num.Length / 2; length++)
            {
                var chunks = num.Chunk(length).Select(c => new string(c)).ToList();
                var first = chunks.First();
                if (chunks.Skip(1).All(c => c == first))
                {
                    yield return i;
                    break;
                }
            }
        }
    }
}
