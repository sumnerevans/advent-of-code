let file = "./inputs/06.txt"

let read_file filename =
  let lines = ref [] in
  let chan = open_in filename in
  try
    while true do
      lines := input_line chan :: !lines
    done ;
    !lines
  with End_of_file -> close_in chan ; List.rev !lines

module IntMap = Map.Make (struct
  type t = int

  let compare = compare
end)

let rec calculate_lanternfish initial_seq =
  let step m =
    IntMap.fold
      (fun k v acc ->
        IntMap.merge
          (fun k v1 v2 ->
            match (v1, v2) with
            | Some x, Some y -> Some (x + y)
            | Some x, None -> Some x
            | None, Some x -> Some x
            | _ -> None )
          acc
          ( match k with
          | 0 -> IntMap.add 8 v (IntMap.add 6 v IntMap.empty)
          | _ -> IntMap.add (k - 1) v IntMap.empty ) )
      m IntMap.empty
  in
  let rec do_calc current_count days =
    match days with
    | 0 -> IntMap.fold (fun _ v acc -> v + acc) current_count 0
    | _ -> do_calc (step current_count) (days - 1)
  in
  let initial_counts =
    List.fold_left
      (fun m x ->
        match IntMap.find_opt x m with
        | None -> IntMap.add x 1 m
        | Some v -> IntMap.add x (v + 1) m )
      IntMap.empty initial_seq
  in
  do_calc initial_counts

(* Run the program *)
let () =
  (* Input parsing *)
  let sequence =
    List.map int_of_string
      (String.split_on_char ',' (List.nth (read_file file) 0))
  in
  let calculator = calculate_lanternfish sequence in
  (* Part 1 *)
  Printf.printf "Part 1:\n" ;
  print_int (calculator 80) ;
  print_newline () ;
  (* Part 2 *)
  Printf.printf "\n" ;
  Printf.printf "Part 2:\n" ;
  print_int (calculator 256) ;
  print_newline ()
