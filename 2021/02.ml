let file = "./inputs/02.txt"

let read_file filename =
  let lines = ref [] in
  let chan = open_in filename in
  try
    while true do
      lines := input_line chan :: !lines
    done ;
    !lines
  with End_of_file -> close_in chan ; List.rev !lines

let part1 lines =
  let res =
    List.fold_left
      (fun (f, d) (dir, x) ->
        Printf.printf "(%d, %d) (%s, %d)\n\n" f d dir x ;
        match dir with
        | "forward" -> (f + x, d)
        | "down" -> (f, d + x)
        | "up" -> (f, d - x) )
      (0, 0) lines
  in
  match res with a, b -> a * b

let part2 lines =
  let res =
    List.fold_left
      (fun (f, d, a) (dir, x) ->
        Printf.printf "(%d, %d, %d) (%s, %d)\n\n" f d a dir x ;
        match dir with
        | "forward" -> (f + x, d + (a * x), a)
        | "down" -> (f, d, a + x)
        | "up" -> (f, d, a - x) )
      (0, 0, 0) lines
  in
  match res with a, b, _ -> a * b

(* Run the program *)
let () =
  (* Input parsing *)
  let lines =
    List.map
      (fun x ->
        ( List.nth (String.split_on_char ' ' x) 0
        , int_of_string (List.nth (String.split_on_char ' ' x) 1) ) )
      (read_file file)
  in
  let rec printer l =
    match l with
    | [] -> ()
    | (d, x) :: xs ->
        Printf.printf "(%s, %d)\n" d x ;
        printer xs
  in
  printer lines ;
  (* Part 1 *)
  Printf.printf "Part 1:\n" ;
  print_int (part1 lines) ;
  print_newline () ;
  (* Part 2 *)
  Printf.printf "Part 2:\n" ;
  print_int (part2 lines) ;
  print_newline ()
