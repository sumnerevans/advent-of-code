open System
open System.Text.RegularExpressions

let rec readlines () =
    [ let line = Console.ReadLine()

      if line <> null then
          yield line
          yield! readlines () ]

let lines = readlines ()

let directions = lines[0]

let mapRe = Regex(@"(.*) = \((.*), (.*)\)", RegexOptions.Compiled)

let map =
    lines[2..]
    |> Seq.map (fun line -> let m = mapRe.Match(line) in (m.Groups[1].Value, (m.Groups[2].Value, m.Groups[3].Value)))
    |> Map.ofSeq

printfn "Part 1:"

let rec step_p1 current directionIdx =
    if current = "ZZZ" then
        directionIdx
    else
        let (left, right) = map[current]

        match directions[directionIdx % directions.Length] with
        | 'L' -> (step_p1 left (directionIdx + 1))
        | 'R' -> (step_p1 right (directionIdx + 1))
        | _ -> failwith "invalid direction"

printfn "%A" (step_p1 "AAA" 0)

printfn "Part 2:"

let rec step_p2_ind (current: string) (directionIdx: uint64) =
    if current[2] = 'Z' then
        directionIdx
    else
        let (left, right) = map[current]

        match directions[(int (directionIdx)) % directions.Length] with
        | 'L' -> step_p2_ind left (directionIdx + 1UL)
        | 'R' -> step_p2_ind right (directionIdx + 1UL)
        | _ -> failwith "invalid direction"

let cycleCounts =
    map.Keys
    |> Seq.filter (fun c -> c[2] = 'A')
    |> List.ofSeq
    |> List.map (fun c -> step_p2_ind c 0UL)

let rec gcd a b =
    match (a, b) with
    | (x, 0UL) -> x
    | (0UL, y) -> y
    | (a, b) -> gcd b (a % b)

let lcm a b = a * b / (gcd a b)
printfn "%d" (List.foldBack lcm cycleCounts 1UL)
