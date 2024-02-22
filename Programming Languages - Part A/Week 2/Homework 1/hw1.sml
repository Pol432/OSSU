(* Homework1 *)
open  Int;
open List;

(* It evaluates to true if the first argument is a date that comes before the 
second argument *)
fun is_older (date1 : int*int*int, date2 : int*int*int) =
    let
	val year = (#1 date1) < (#1 date2)
	val month = ((#2 date1) < (#2 date2)) andalso ((#1 date1) = (#1 date2))
	val day = ((#3 date1) < (#3 date2))
		  andalso ((#2 date1) = (#2 date2))
		  andalso ((#1 date1) = (#1 date2))
    in
	if year
	   orelse month
	   orelse day
	then true else false
    end

(* Returns how many dates in the list are in the given month. *)
fun number_in_month (dates : (int*int*int) list, month : int) =
    if null dates
    then 0
    else
	let val next_date = (number_in_month(tl dates, month))
	in
	    if month = #2 (hd dates)
	    then 1 + next_date
	    else next_date end
	   

(* Returns the number of dates in the list of dates that are in any of the months in the list of months *)
fun number_in_months (dates : (int*int*int) list, months : int list) =
    if null months
    then
	0
    else
	 number_in_month(dates, hd months) +
	 number_in_months (dates, tl months)

			  
(* Returns a list holding the dates from the argument list of dates that are in
the month. *)
fun dates_in_month (dates : (int*int*int) list, month) =
    if null dates
    then []
    else
	let
	    val next_dates = (dates_in_month(tl dates, month))
	in
	    if month = #2 (hd dates)
	    then
		hd dates :: next_dates
	    else
		next_dates
	end
		   

(* Returns a list holding the dates from the argument list of dates that are in 
any of the months in the list of months. *)
fun dates_in_months (dates : (int*int*int) list, months : int list) =
    if null months
    then []
    else dates_in_month(dates, hd months) @ (dates_in_months(dates, tl months))

						
(* Returns the nth element of the list where the head of the list is 1st*)
fun get_nth (strings : string list, n : int) =
    List.nth (strings, n - 1)

	
(* Returns a string of the form January 20, 2013 (for example).*)
fun date_to_string (date : int*int*int) =
    let
	val months = ["January", "February", "March", "April", "May", "June",
		      "July","August", "September", "October", "November", "December"]
	val day = Int.toString (#3 date)
	val year = Int.toString (#1 date)
    in
	get_nth(months, #2 date) ^ " " ^ day ^ ", " ^ year
    end
	
				 
(* Return an int n such that the first n elements of the list add to less than
 sum, but the first n + 1 elements of the list add to sum or more. *)
fun number_before_reaching_sum (sum : int, ints : int list) =
    if null (tl ints) orelse null ints
    then 0
    else
	let
	    fun sum_list (current_sum : int, ints : int list, position : int) =
		let val hd_tl_ints = if null (tl ints)
				     then 0 else hd(tl ints)
		in
		    if (current_sum + hd_tl_ints) >=  sum orelse null ints
		    then position
		    else
			sum_list (
			    (current_sum + hd_tl_ints),
			    tl ints,
			    position + 1) end
	in
	   sum_list(hd ints, ints, 1)
	end


val days = [0, 31, 28, 31, 30, 31, 30 , 31, 31, 30, 31, 30, 31]
(* Returns what month that day is in (1 for January, 2 for February, etc.) *)
fun what_month (day : int) =
    number_before_reaching_sum(day, days)
	

(* Returns an int list [m1,m2,...,mn] where m1 is the month of day1, m2 is the
 month of day1+1, ..., and mn is the month of day day2. *)
fun month_range (day1 : int, day2 : int) =
    let
	fun slice(current : int) =
	    if current <= day2	      
	    then (what_month current) :: slice(current + 1)
	    else []
    in	
	slice(day1)
    end


(* It evaluates to NONE if the list has no dates and SOME d if the date d is the oldest date in the list.*)
fun oldest (dates : (int*int*int) list) =
    if null dates
    then NONE
    else
	let
	    fun oldest_helper (current : int*int*int, dates: (int*int*int) list)=
		if null dates then current
				     
		else if is_older (hd dates, current)
		then oldest_helper(hd dates, tl dates)
				  
		else oldest_helper(current, tl dates)
	in
	    SOME (oldest_helper(hd dates, dates))
	end
	    

fun no_duplicates (list: int list) =
    if null list
    then []
    else
	let val tl_list = no_duplicates(tl list)
	in if List.exists (fn x => x = (hd list)) (tl list)		  
	   then tl_list
	   else (hd list) :: tl_list
	end

fun number_in_months_challenge (dates: (int*int*int) list, months: int list) =
    number_in_months(dates, no_duplicates(months))

fun dates_in_months_challenge (dates: (int*int*int) list, months: int list) =
    dates_in_months(dates, no_duplicates(months))


fun reasonable_date (date: int*int*int) =
    let
	val year = #1 date
	val month = #2 date
	val day = #3 date
	val days_in_month = List.nth(days, month)
    in
	year > 0 andalso month > 0 andalso month <= 12
	andalso day > 0 andalso day <= days_in_month
    end
