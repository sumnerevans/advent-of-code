// For more information see https://aka.ms/fsharp-console-apps
open System

let rec readlines () = [
    let line = Console.ReadLine()
    if line <> null then
        yield line
        yield! readlines ()
]

let lines = readlines()

let x = lines |> Seq.map (fun x -> (
    ((x.Split(": ")[0]).Split(' ')[1] |> int),
    ((x.Split(": ")[1]).Split("; ") |> Array.map (fun x -> (
        x.Split(", ") |> Array.map (fun x -> (
            (x.Split(' ')[0] |> int),
            (x.Split(' ')[1])
        )) |> Array.map (fun x -> (
            match (snd x) with
                |"blue" -> (fst x) <= 14
                |"green" -> (fst x) <= 13
                |"red" -> (fst x) <= 12
                |_ -> failwith "invalid color"
        )) |> Array.reduce (&&)
    )) |> Array.reduce (&&))
))
let y = x |> Seq.filter (fun x -> (snd x) = true)
let z = y |> Seq.map (fun x -> (fst x)) |> Seq.sum
printfn "Part 1: %A" z

let a = lines |> Seq.map (fun x ->
    (x.Split(": ")[1]).Split("; ") |> Array.map (fun x -> (
        x.Split(", ") |> Array.map (fun x -> (
            (x.Split(' ')[0] |> int),
            (x.Split(' ')[1])
        )) |> Array.fold (fun (blue,green,red) (count, color) -> (
            match color with
                |"blue" -> ((max count blue), green, red)
                |"green" -> (blue, (max count green), red)
                |"red" -> (blue, green, (max count red))
                |_ -> failwith "invalid color"
        )) (0, 0, 0)
    )) |> Array.fold (fun (acc_blue,acc_green,acc_red) (blue,green,red) -> (
        (max blue acc_blue, max green acc_green, max red acc_red)
    )) (0, 0, 0)
)
let b = a |> Seq.map (fun (x,y,z) -> (x*y*z)) |> Seq.sum
printfn "Part 2: %A" b
