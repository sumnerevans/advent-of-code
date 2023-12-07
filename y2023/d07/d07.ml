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

let int_of_card card_str =
  match card_str with
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

let ints_of_hand_str hand_str =
  match String.to_seq hand_str |> List.of_seq with
  | [a; b; c; d; e] ->
      ( int_of_card a
      , int_of_card b
      , int_of_card c
      , int_of_card d
      , int_of_card e )
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

let parse_hand hand_str =
  printf "%s\n" hand_str ;
  List.iter
    (fun (count, c) -> printf "(%d, %c) " count c)
    (List.sort compare (compress hand_str)) ;
  print_newline () ;
  match List.sort compare (compress hand_str) with
  | [(5, _)] -> (FiveOfAKind, ints_of_hand_str hand_str)
  | [(1, _); (4, _)] -> (FourOfAKind, ints_of_hand_str hand_str)
  | [(2, _); (3, _)] -> (FullHouse, ints_of_hand_str hand_str)
  | [_; _; (3, _)] -> (ThreeOfAKind, ints_of_hand_str hand_str)
  | [_; (2, _); (2, _)] -> (TwoPair, ints_of_hand_str hand_str)
  | [_; _; _; (2, _)] -> (OnePair, ints_of_hand_str hand_str)
  | _ -> (HighCard, ints_of_hand_str hand_str)

let compare_hands (hand1kind, hand1str) (hand2kind, hand2str) =
  compare (int_of_hand hand1kind, hand1str) (int_of_hand hand2kind, hand2str)

let part1 hands =
  List.fold_left ( + ) 0
  @@ List.mapi
       (fun i (_, bet) ->
         printf "%d %d\n" (i + 1) bet ;
         (i + 1) * bet )
       (List.sort
          (fun (hand1, _) (hand2, _) -> compare_hands hand2 hand1)
          hands )

(* let part2 nums = *)
(*   let rec windows3 l = *)
(*     match l with *)
(*     | [] -> [] *)
(*     | [a] -> [] *)
(*     | [a; b] -> [] *)
(*     | a :: b :: c :: more -> (a, b, c) :: windows3 (b :: c :: more) *)
(*   in *)
(*   part1 (List.map (fun (a, b, c) -> a + b + c) (windows3 nums)) *)

(* Run the program *)
let () =
  let ht, (a, b, c, d, e) = parse_hand "432AA" in
  printf "%d (%d, %d, %d, %d, %d)\n" (int_of_hand ht) a b c d e ;
  print_newline () ;
  print_newline () ;
  print_newline () ;
  print_newline () ;
  (* Input parsing *)
  let hands =
    List.map
      (fun s ->
        match String.split_on_char ' ' s with
        | [hand; bet] -> (parse_hand hand, int_of_string bet)
        | _ -> failwith "Invalid input" )
      (read_file file)
  in
  (* Part 1 *)
  Printf.printf "Part 1:\n" ;
  print_int (part1 hands) ;
  print_newline () ;
  (* Part 2 *)
  Printf.printf "Part 2:\n" ;
  (* print_int (part2 lines) ; *)
  print_newline ()
