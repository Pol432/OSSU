
(* This is a comment. This is our first program. *)

val x = 34;
(* dynamic envyronment x --> 34 *)

val y = 17;
(* dynamic environment x --> 34, y --> 17 *)

val z = (x + y) + (y + 2);
(* dynamic environment x --> 34, y --> 17, z --> 70 *)

val abs_of_z = if z < 0 then 0 - z else z;
