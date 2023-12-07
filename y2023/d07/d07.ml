open Stdlib
open Printf

(* let file = "./07.test.1.txt" *)
let file = "./07.txt"

let read_file filename =
  let lines = ref [] in
  let chan = open_in filename in
  try
    while true do
      lines := input_line chan :: !lines
    done ;
    !lines
  with End_of_file -> close_in chan ; List.rev !lines

type hand_type =
  | FiveOfAKind
  | FourOfAKind
  | FullHouse
  | ThreeOfAKind
  | TwoPair
  | OnePair
  | HighCard

type hand = hand_type * string

let int_of_hand hand =
  match hand with
  | FiveOfAKind -> 0
  | FourOfAKind -> 1
  | FullHouse -> 2
  | ThreeOfAKind -> 3
  | TwoPair -> 4
  | OnePair -> 5
  | HighCard -> 6

let int_of_card_p1 card =
  match card with
  | '2' -> 13
  | '3' -> 12
  | '4' -> 11
  | '5' -> 10
  | '6' -> 9
  | '7' -> 8
  | '8' -> 7
  | '9' -> 6
  | 'T' -> 5
  | 'J' -> 4
  | 'Q' -> 3
  | 'K' -> 2
  | 'A' -> 1
  | _ -> failwith "Invalid card"

let int_of_card_p2 card =
  match card with
  | 'J' -> 14
  | '2' -> 13
  | '3' -> 12
  | '4' -> 11
  | '5' -> 10
  | '6' -> 9
  | '7' -> 8
  | '8' -> 7
  | '9' -> 6
  | 'T' -> 5
  | 'Q' -> 3
  | 'K' -> 2
  | 'A' -> 1
  | _ -> failwith "Invalid card"

let ints_of_hand_str_p1 hand_str =
  match String.to_seq hand_str |> List.of_seq with
  | [a; b; c; d; e] ->
      ( int_of_card_p1 a
      , int_of_card_p1 b
      , int_of_card_p1 c
      , int_of_card_p1 d
      , int_of_card_p1 e )
  | _ -> failwith "Invalid hand"

let ints_of_hand_str_p2 hand_str =
  match String.to_seq hand_str |> List.of_seq with
  | [a; b; c; d; e] ->
      ( int_of_card_p2 a
      , int_of_card_p2 b
      , int_of_card_p2 c
      , int_of_card_p2 d
      , int_of_card_p2 e )
  | _ -> failwith "Invalid hand"

let sort_str s = String.to_seq s |> List.of_seq |> List.sort Char.compare

let compress s =
  let rec compress' rest prev count =
    match rest with
    | [] -> [(count, prev)]
    | x :: xs ->
        if x = prev then compress' xs prev (count + 1)
        else (count, prev) :: compress' xs x 1
  in
  match sort_str s with [] -> [] | x :: xs -> compress' xs x 1

let parse_hand_p1 hand_str =
  match List.sort compare (compress hand_str) with
  | [(5, _)] -> (FiveOfAKind, ints_of_hand_str_p1 hand_str)
  | [(1, _); (4, _)] -> (FourOfAKind, ints_of_hand_str_p1 hand_str)
  | [(2, _); (3, _)] -> (FullHouse, ints_of_hand_str_p1 hand_str)
  | [_; _; (3, _)] -> (ThreeOfAKind, ints_of_hand_str_p1 hand_str)
  | [_; (2, _); (2, _)] -> (TwoPair, ints_of_hand_str_p1 hand_str)
  | [_; _; _; (2, _)] -> (OnePair, ints_of_hand_str_p1 hand_str)
  | _ -> (HighCard, ints_of_hand_str_p1 hand_str)

let compare_hands (hand1kind, hand1str) (hand2kind, hand2str) =
  compare (int_of_hand hand1kind, hand1str) (int_of_hand hand2kind, hand2str)

let part1 =
  let hands =
    List.map
      (fun s ->
        match String.split_on_char ' ' s with
        | [hand; bet] -> (parse_hand_p1 hand, int_of_string bet)
        | _ -> failwith "Invalid input" )
      (read_file file)
  in
  List.fold_left ( + ) 0
  @@ List.mapi
       (fun i (_, bet) -> (i + 1) * bet)
       (List.sort
          (fun (hand1, _) (hand2, _) -> compare_hands hand2 hand1)
          hands )

let parse_hand_p2 hand_str =
  match List.sort compare (compress hand_str) with
  | [(5, _)] -> (FiveOfAKind, ints_of_hand_str_p2 hand_str)
  | [(1, 'J'); (4, _)] -> (FiveOfAKind, ints_of_hand_str_p2 hand_str)
  | [(1, _); (4, 'J')] -> (FiveOfAKind, ints_of_hand_str_p2 hand_str)
  | [(2, 'J'); (3, _)] -> (FiveOfAKind, ints_of_hand_str_p2 hand_str)
  | [(2, _); (3, 'J')] -> (FiveOfAKind, ints_of_hand_str_p2 hand_str)
  | [(1, _); (4, _)] -> (FourOfAKind, ints_of_hand_str_p2 hand_str)
  | [(1, 'J'); _; (3, _)] -> (FourOfAKind, ints_of_hand_str_p2 hand_str)
  | [_; (1, 'J'); (3, _)] -> (FourOfAKind, ints_of_hand_str_p2 hand_str)
  | [_; (1, _); (3, 'J')] -> (FourOfAKind, ints_of_hand_str_p2 hand_str)
  | [(1, _); (2, 'J'); (2, _)] -> (FourOfAKind, ints_of_hand_str_p2 hand_str)
  | [(1, _); (2, _); (2, 'J')] -> (FourOfAKind, ints_of_hand_str_p2 hand_str)
  | [(2, _); (3, _)] -> (FullHouse, ints_of_hand_str_p2 hand_str)
  | [(1, 'J'); (2, _); (2, _)] -> (FullHouse, ints_of_hand_str_p2 hand_str)
  | [(1, 'J'); (1, _); (1, _); (2, _)] ->
      (ThreeOfAKind, ints_of_hand_str_p2 hand_str)
  | [(1, _); (1, 'J'); (1, _); (2, _)] ->
      (ThreeOfAKind, ints_of_hand_str_p2 hand_str)
  | [(1, _); (1, _); (1, 'J'); (2, _)] ->
      (ThreeOfAKind, ints_of_hand_str_p2 hand_str)
  | [(1, _); (1, _); (1, _); (2, 'J')] ->
      (ThreeOfAKind, ints_of_hand_str_p2 hand_str)
  | [_; _; (3, _)] -> (ThreeOfAKind, ints_of_hand_str_p2 hand_str)
  | [_; (2, _); (2, _)] -> (TwoPair, ints_of_hand_str_p2 hand_str)
  | [_; _; _; (2, _)] -> (OnePair, ints_of_hand_str_p2 hand_str)
  | [(1, 'J'); (1, _); (1, _); (1, _); (1, _)] ->
      (OnePair, ints_of_hand_str_p2 hand_str)
  | [(1, _); (1, 'J'); (1, _); (1, _); (1, _)] ->
      (OnePair, ints_of_hand_str_p2 hand_str)
  | [(1, _); (1, _); (1, 'J'); (1, _); (1, _)] ->
      (OnePair, ints_of_hand_str_p2 hand_str)
  | [(1, _); (1, _); (1, _); (1, 'J'); (1, _)] ->
      (OnePair, ints_of_hand_str_p2 hand_str)
  | [(1, _); (1, _); (1, _); (1, _); (1, 'J')] ->
      (OnePair, ints_of_hand_str_p2 hand_str)
  | _ -> (HighCard, ints_of_hand_str_p2 hand_str)

let part2 =
  let hands =
    List.map
      (fun s ->
        match String.split_on_char ' ' s with
        | [hand; bet] ->
            (* let hand_type, (a, b, c, d, e) = parse_hand_p2 hand in *)
            (* printf "%s %d (%d, %d, %d, %d, %d)\n" hand *)
            (*   (int_of_hand hand_type) a b c d e ; *)
            (* flush stdout ; *)
            (* let _ = *)
            (*   match ints_of_hand_str_p2 hand with *)
            (*   | 14, _, _, _, _ -> input_line stdin *)
            (*   | _, 14, _, _, _ -> input_line stdin *)
            (*   | _, _, 14, _, _ -> input_line stdin *)
            (*   | _, _, _, 14, _ -> input_line stdin *)
            (*   | _, _, _, _, 14 -> input_line stdin *)
            (*   | _ -> "" *)
            (* in *)
            (* () ; *)
            (parse_hand_p2 hand, int_of_string bet)
        | _ -> failwith "Invalid input" )
      (read_file file)
  in
  List.fold_left ( + ) 0
  @@ List.mapi
       (fun i ((hand_type, (a, b, c, d, e)), bet) ->
         printf "%d (%d, %d, %d, %d, %d) %d %d" (int_of_hand hand_type) a b c
           d e (i + 1) bet ;
         print_newline () ;
         (i + 1) * bet )
       (List.sort
          (fun (hand1, _) (hand2, _) -> compare_hands hand2 hand1)
          hands )

(* Run the program *)
let () =
  (* Input parsing *)
  (* Part 1 *)
  Printf.printf "Part 1:\n" ;
  print_int part1 ;
  print_newline () ;
  (* Part 2 *)
  Printf.printf "Part 2:\n" ;
  print_int part2 ;
  print_newline ()
