let file = "./inputs/07.txt"

let read_file filename =
  let lines = ref [] in
  let chan = open_in filename in
  try
    while true do
      lines := input_line chan :: !lines
    done ;
    !lines
  with End_of_file -> close_in chan ; List.rev !lines

let range i j =
  let rec aux n acc = if n < i then acc else aux (n - 1) (n :: acc) in
  aux j []

let min_ = List.fold_left min max_int

let max_ = List.fold_left max min_int

let memo f =
  let h = Hashtbl.create 11 in
  fun x ->
    try Hashtbl.find h x
    with Not_found ->
      let y = f x in
      Hashtbl.add h x y ; y

let rec calc_best_alignment initial_seq f =
  min_
    (List.map
       (fun v -> List.fold_left (fun acc x -> f v x + acc) 0 initial_seq)
       (range (min_ initial_seq) (max_ initial_seq)) )

(* Run the program *)
let () =
  (* Input parsing *)
  let sequence =
    List.map int_of_string
      (String.split_on_char ',' (List.nth (read_file file) 0))
  in
  let calculator = calc_best_alignment sequence in
  (* Part 1 *)
  Printf.printf "Part 1:\n" ;
  print_int (calculator (fun x y -> abs (x - y))) ;
  print_newline () ;
  (* Part 2 *)
  Printf.printf "\n" ;
  Printf.printf "Part 2:\n" ;
  print_int
    (calculator (fun x y ->
         let d = abs (x - y) in
         d * (d + 1) / 2 ) ) ;
  print_newline ()
