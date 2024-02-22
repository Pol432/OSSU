(* Coursera Programming Languages, Homework 3, Provided Code *)

exception NoAnswer

datatype pattern = Wildcard
		 | Variable of string
		 | UnitP
		 | ConstP of int
		 | TupleP of pattern list
		 | ConstructorP of string * pattern

datatype valu = Const of int
	      | Unit
	      | Tuple of valu list
	      | Constructor of string * valu

fun g f1 f2 p =
    let 
	val r = g f1 f2 
    in
	case p of
	    Wildcard          => f1 ()
	  | Variable x        => f2 x
	  | TupleP ps         => List.foldl (fn (p,i) => (r p) + i) 0 ps
	  | ConstructorP(_,p) => r p
	  | _                 => 0
    end

(**** for the challenge problem only ****)

datatype typ = Anything
	     | UnitT
	     | IntT
	     | TupleT of typ list
	     | Datatype of string

(**** you can put all your code here ****)
			 
fun only_capitals sl = List.filter(fn str => (Char.isUpper(String.sub (str,0)))) sl

fun longest_string1 sl = List.foldl(fn (acc,cur) =>
				       if (String.size acc) > (String.size cur)
				       then acc else cur) "" sl

fun longest_string2 sl = List.foldl(fn (acc,cur) =>
				       if (String.size acc) >= (String.size cur)
				       then acc else cur) "" sl

fun longest_string_helper f sl = List.foldl (fn (acc,cur) =>
				     (if f (String.size acc, String.size cur)
				      then acc else cur)) "" sl

val longest_string3 = fn sl => longest_string_helper (fn (x,y) => x > y) sl
    
val longest_string4 = fn sl => longest_string_helper (fn (x,y) => x >= y) sl
    
val longest_capitalized = fn sl => List.foldl(fn (acc,cur) =>
					if (String.size acc) > (String.size cur)
					then acc else cur) "" (only_capitals sl)

fun rev_string s = (String.implode o rev o String.explode) s
 
fun first_answer f l =
    case l of
	[] => raise NoAnswer
      | xhd::xtl => case f xhd of
			NONE => first_answer f xtl
		     | SOME xhd => xhd

fun all_answers f lst =
    let
	fun helper lst acc =
	    case lst of
		[] => SOME acc
	      | xhd::xtl  => case f xhd of
				 NONE => NONE
			      | SOME x => helper xtl (x @ acc)
    in
	helper lst []
    end

fun count_wildcards p = g (fn x => 1) (fn x => 0) p

fun count_wild_and_variable_lengths p = (count_wildcards p) + g (fn x => 0) (fn x => String.size x) p

fun count_some_var (str,p) = g (fn x => 0) (fn x => if x = str then 1 else 0) p

fun check_pat p =
    let
	fun str_list p =
	    case p of
		Variable x => [x]
	     | TupleP x => List.foldl(fn (cur,acc) => str_list cur @ acc) [] x
	     | ConstructorP (_,y) => str_list y
	     | _ => []
	fun check list =
	    case list of
		[] => true
	      | xhd::xtl => (not (List.exists(fn x => x=xhd) xtl))
			    andalso check xtl			   
    in check (str_list p) end
	

fun match (v,p) =
    case (v,p) of
	(_,Wildcard) => SOME []
      | (_,Variable x) => SOME [(x,v)]
      | (Unit,UnitP) => SOME []
      | (Const x, ConstP y) => if x = y then SOME [] else NONE
      | (Constructor (xx,xy),ConstructorP (yy,yx)) => if xx = yy
						      then match(xy,yx) else NONE
      | (Tuple x, TupleP y) => if List.length x = List.length y
			       then all_answers match(ListPair.zip(x,y))
			       else NONE
      | _ => NONE

fun first_match v lp =
   SOME (first_answer (fn p => match (v,p)) lp) handle NoAnswer => NONE
