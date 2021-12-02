let file = "./inputs/01.txt"

let read_file filename =
  let lines = ref [] in
  let chan = open_in filename in
  try
    while true do
      lines := input_line chan :: !lines
    done ;
    !lines
  with End_of_file -> close_in chan ; List.rev !lines

let rec pairs l =
  match l with
  | [] -> []
  | [a] -> []
  | a :: b :: more -> (a, b) :: pairs (b :: more)

let part1 nums =
  List.fold_left (fun n (x, y) -> n + if y > x then 1 else 0) 0 (pairs nums)

let part2 nums =
  let rec windows3 l =
    match l with
    | [] -> []
    | [a] -> []
    | [a; b] -> []
    | a :: b :: c :: more -> (a, b, c) :: windows3 (b :: c :: more)
  in
  part1 (List.map (fun (a, b, c) -> a + b + c) (windows3 nums))

(* Run the program *)
let () =
  (* Input parsing *)
  let lines = List.map int_of_string (read_file file) in
  (* Part 1 *)
  Printf.printf "Part 1:\n" ;
  print_int (part1 lines) ;
  print_newline () ;
  (* Part 2 *)
  Printf.printf "Part 2:\n" ;
  print_int (part2 lines) ;
  print_newline ()
