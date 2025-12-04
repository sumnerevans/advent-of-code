public static class Program
{
    public static void Main()
    {
        using (var reader = new StreamReader("04.txt"))
        // using (var reader = new StreamReader("04.test.01.txt"))
        {
            var map = new List<string>();
            while (!reader.EndOfStream)
            {
                map.Add(reader.ReadLine()!);
            }

            Console.WriteLine($"Part 1: {Part1(map)}");
            Console.WriteLine($"Part 2: {Part2(map)}");
        }
    }

    static IEnumerable<(int, int)> Adjs(int r, int c, int maxR, int maxC)
    {
        if (r > 0)
        {
            if (c > 0)
                yield return (r - 1, c - 1);
            yield return (r - 1, c);
            if (c < maxC - 1)
                yield return (r - 1, c + 1);
        }

        if (c > 0)
            yield return (r, c - 1);
        if (c < maxC - 1)
            yield return (r, c + 1);
        if (r < maxR - 1)
        {
            {
                if (c > 0)
                    yield return (r + 1, c - 1);
                yield return (r + 1, c);
                if (c < maxC - 1)
                    yield return (r + 1, c + 1);
            }
        }
    }

    static long Part1(List<string> map)
    {
        int ans = 0;
        int maxR = map.Count;
        int maxC = map[0].Count();
        for (int r = 0; r < map.Count; r++)
        {
            for (int c = 0; c < map[r].Count(); c++)
            {
                if (map[r][c] == '@' && Adjs(r, c, maxR, maxC).Count(coord => map[coord.Item1][coord.Item2] == '@') < 4)
                    ans++;
            }
        }
        return ans;
    }

    static long Part2(List<string> map)
    {
        bool changed = true;
        int ans = 0;
        int maxR = map.Count;
        int maxC = map[0].Count();
        while (changed)
        {
            int count = 0;

            var newMap = new List<List<char>>();

            for (int r = 0; r < map.Count; r++)
            {
                newMap.Add(new List<char>());
                for (int c = 0; c < map[r].Count(); c++)
                {
                    if (
                        map[r][c] == '@'
                        && Adjs(r, c, maxR, maxC).Count(coord => map[coord.Item1][coord.Item2] == '@') < 4
                    )
                    {
                        count++;
                        newMap[r].Add('x');
                    }
                    else
                    {
                        newMap[r].Add(map[r][c]);
                    }
                }
            }
            if (count == 0)
                return ans;
            ans += count;
            map = newMap.Select(l => new string(l.ToArray())).ToList();
        }
        throw new Exception("shouldn't be here");
    }
}
