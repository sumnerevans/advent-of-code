using System.Diagnostics;
using System.Text.RegularExpressions;

public static class Program
{
    enum Direction
    {
        Left,
        Right,
    };

    readonly record struct Instr(Direction Direction, int Count);

    static Regex lineRe = new Regex(@"^(L|R)(\d+)$");

    public static void Main()
    {
        var instrs = new List<Instr>();
        using (var reader = new StreamReader("01.txt"))
        // using (var reader = new StreamReader("01.test.01.txt"))
        // using (var reader = new StreamReader("01.test.02.txt"))
        // using (var reader = new StreamReader("01.test.03.txt"))
        {
            string? line = reader.ReadLine();
            while (!string.IsNullOrEmpty(line))
            {
                var match = lineRe.Match(line);
                Debug.Assert(match.Success);

                instrs.Add(
                    new Instr(
                        match.Groups[1].Value == "L" ? Direction.Left : Direction.Right,
                        int.Parse(match.Groups[2].Value)
                    )
                );
                line = reader.ReadLine();
            }
        }

        Console.WriteLine($"Part 1: {Part1(instrs)}");
        Console.WriteLine($"Part 2: {Part2(instrs)}");
    }

    static int Part1(List<Instr> instrs) => Locations(instrs).Count(loc => loc == 0);

    static int Part2(List<Instr> instrs) => Passes(instrs).Sum();

    static IEnumerable<int> Locations(List<Instr> instrs)
    {
        int location = 50;
        yield return location;
        foreach (var instr in instrs)
        {
            location += instr.Direction switch
            {
                Direction.Left => -instr.Count,
                Direction.Right => instr.Count,
            };
            location = location % 100;
            yield return location;
        }
    }

    static IEnumerable<int> Passes(List<Instr> instrs)
    {
        int location = 50;
        foreach (var instr in instrs)
        {
            int newLoc = instr.Direction switch
            {
                Direction.Left => location - instr.Count,
                Direction.Right => location + instr.Count,
            };

            if ((location < 0 && newLoc > 0) || (location > 0 && newLoc < 0))
                yield return 1;

            if (newLoc == 0)
                yield return 1;
            else
                yield return Math.Abs(newLoc / 100);

            location = newLoc % 100;
        }
    }
}
