let file = "./01.txt"

exception Panic of string

let read_file filename =
  let lines = ref [] in
  let chan = open_in filename in
  try
    while true do
      lines := input_line chan :: !lines
    done ;
    !lines
  with End_of_file -> close_in chan ; List.rev !lines

let part1 groups =
  List.fold_left max 0 (List.map (List.fold_left ( + ) 0) groups)

let part2 groups =
  match
    List.sort
      (fun a b -> -compare a b)
      (List.map (List.fold_left ( + ) 0) groups)
  with
  | a :: b :: c :: more -> a + b + c
  | _ -> raise (Panic "not enough groups")

(* Run the program *)
let () =
  (* Input parsing *)
  let rec group acc lines =
    match lines with
    | [] -> []
    | a :: more ->
        if a = "" then acc :: group [] more else group (a :: acc) more
  in
  let groups =
    List.map (List.map int_of_string) (group [] (read_file file))
  in
  (* Part 1 *)
  Printf.printf "Part 1:\n" ;
  print_int (part1 groups) ;
  print_newline () ;
  (* Part 2 *)
  Printf.printf "Part 2:\n" ;
  print_int (part2 groups) ;
  print_newline ()
