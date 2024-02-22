(* Dan Grossman, Coursera PL, HW2 Provided Code *)

(* if you use this function to compare two strings (returns true if the same
   string), then you avoid several of the functions in problem 1 having
   polymorphic types that may be confusing *)
fun same_string(s1 : string, s2 : string) =
    s1 = s2

(* put your solutions for problem 1 here *)
(* Check if given str is already in the list *)
fun in_list (str,lst) =
    case lst of
	[] => false
	| xhd::xtl => if same_string(xhd,str) then true
		      else in_list(str,xtl)

(* Given a list of strings and a str, produce a tuple with a list including elements of the list of strings excpet the str and false if couldn't find the element *)
fun all_except (strl,str) =
    let
	fun helper(strl,acc,found)=
	    case strl of
		[] => (acc,found)
	      | x::xs' => if same_string(x,str) then helper(xs',acc,true)
			  else if in_list(x,acc) then helper(xs',acc,found)
			  else helper(xs',(x::acc),found)
    in helper(strl,[],false) end

(* Return NONE if the string is not in the list, else return SOME lst where lst is identical to the argument list except the string is not in it.  *)
fun all_except_option (str, strl) =
    let
	val ans = all_except(strl,str)			    
    in
	case ans of (list,found) => if found then SOME list else NONE
    end

(* The result has all the strings that are in some list in substitutions that also has s, but s itself should not be in the result *)
fun get_substitutions1 (strll, str) =
    let
	fun list (ans) =
	    case ans of
		(list,found) => if found then list else []		    
	fun helper (strll,acc) =
	 case strll of
	     [] => acc
	   | yhd::ytl => helper(ytl,acc @ list(all_except(yhd,str)))
    in helper(strll,[]) end
	
(* Like get_substitutions1 except it uses a tail-recursive local helper function. *)
fun get_substitutions2 (strll, str) =
    let
	fun list (ans) =
	    case ans of
		(list,found) => if found then list else []		    
	fun helper (strll,acc) =
	 case strll of
	     [] => acc
	   | yhd::ytl => helper(ytl,acc @ list(all_except(yhd,str)))
    in helper(strll,[]) end

(* The result is all the full names you can produce by substituting for the first name. The answer should begin with the original name (then have 0 or more other names) *)
fun similar_names (strll,{first=x,middle=y,last=z}) =
    let
	val name = {first=x,middle=y,last=z}
	fun to_name (strl,name) =
	    case strl of
		[] => []
	      | xhd::xtl => {first=xhd,last=z,middle=y}::
			    to_name(xtl,name)
    in
	name::(to_name(
		    (get_substitutions2(strll,x)),
		    name))
    end
	     
(* you may assume that Num is always used with values 2, 3, ..., 10
   though it will not really come up *)
datatype suit = Clubs | Diamonds | Hearts | Spades
datatype rank = Jack | Queen | King | Ace | Num of int 
type card = suit * rank

datatype color = Red | Black
datatype move = Discard of card | Draw 

exception IllegalMove

(* put your solutions for problem 2 here *)
	
(* Takes a card and returns it's color *)
fun card_color (suit,rank) =
    if suit = Spades orelse suit = Clubs
    then Black else Red

(* Takes a card and returns it's rank *)
fun card_value (suit,rank) =
    case rank of
	Ace => 11
      | Num x => x
      | _ => 10
    
(* Returns a list that has all the elements of cs except c and raises an exception if there is no c *)
fun remove_card (cs,c,e) =
    let
	fun helper (cs,acc) =
	    case cs of
		[] => raise e
	      | xhd::xtl => if xhd = c then acc@xtl
			    else helper(xtl,(xhd::acc))
    in
	helper(cs,[])
    end

(* Returns true if all the cards in the list are the same color *)
fun all_same_color (list) =
    let
	val color = case list of [] => Red
			       | x::xtl => card_color(x)
	fun helper (list) =
	    case list of
		[] => true
	      | xhd::xtl => if card_color(xhd) = color
			    then helper(xtl) else false
    in
	helper(list)
    end

(* Returns the sum of the card's values *)
fun sum_cards (list) =
    let
	fun helper (list,acc) =
	    case list of
		[] => acc
	     | xhd::xtl => helper(xtl,(card_value xhd) + acc)
    in
	helper(list,0)
    end
	
(* Returns a score: If sum is greater than goal, the preliminary score is three times (sum goal) else the preliminary score is (goal sum).*)
fun score (cards,goal) =
    let
	val sum = sum_cards(cards)
	val preliminary = if sum > goal
			  then (sum - goal) * 3
			  else goal - sum
    in
	if all_same_color(cards) then preliminary div 2 else preliminary
    end

(* Returns the score at the end of the game after processing (some or all of) the moves in the move list in order. *)
fun officiate (cards, moves, goal) =
    let
	fun game (moves,cards,held) =
	    case (moves,cards) of
	      ((Discard card)::xtl,_) => game(xtl,cards,remove_card(held,card,IllegalMove))
	     | (Draw::xtl,yhd::ytl) => if sum_cards(yhd::held) > goal then score(yhd::held,goal) else game(xtl,ytl,yhd::held)
	     | (_,_) => score(held,goal)
    in
	game(moves,cards,[])
    end





