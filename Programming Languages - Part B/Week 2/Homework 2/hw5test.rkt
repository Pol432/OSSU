#lang racket
;; Programming Languages Homework 5 Simple Test
;; Save this file to the same directory as your homework file
;; These are basic tests. Passing these tests does not guarantee that your code will pass the actual homework grader

;; Be sure to put your homework file in the same folder as this test file.
;; Uncomment the line below and, if necessary, change the filename
(require "hw5.rkt")

(require rackunit)

(define tests
  (test-suite
   "Sample tests for Assignment 5"
   
   ;; check racketlist to mupllist with normal list
   (check-equal? (racketlist->mupllist (list (int 3) (int 4))) (apair (int 3) (apair (int 4) (aunit))) "racketlist->mupllist test")
   (check-equal? (racketlist->mupllist (list (var "hi") (int 5))) (apair (var "hi") (apair (int 5) (aunit))))
   (check-equal? (racketlist->mupllist (list (apair (int 3) (int 4)) (int 10) (var "k") (var "sum"))) (apair (apair (int 3) (int 4)) (apair (int 10) (apair (var "k") (apair (var "sum")(aunit))))))                
   
   ;; check mupllist to racketlist with normal list
   (check-equal? (mupllist->racketlist (apair (int 3) (apair (int 4) (aunit)))) (list (int 3) (int 4)) "racketlist->mupllist test")
   (check-equal? (mupllist->racketlist (apair (var "hi") (apair (int 5) (aunit)))) (list (var "hi") (int 5)))  
   (check-equal? (mupllist->racketlist (apair (apair (int 3) (int 4)) (apair (int 10) (apair (var "k") (apair (var "sum") (aunit)))))) (list (apair (int 3) (int 4)) (int 10) (var "k") (var "sum")))

   ;; tests if ifgreater returns (int 2)
   (check-equal? (eval-exp (ifgreater (int 3) (int 4) (int 3) (int 2))) (int 2) "ifgreater test")
   (check-equal? (eval-exp (ifgreater (int 5) (int 5) (int 6) (int 1))) (int 1) "ifgreater test")
   (check-equal? (eval-exp (ifgreater (int 7) (int 6) (add (int 6) (int 3)) (var "hi"))) (int 9) "ifgreater test")
   
   ;; mlet test
   (check-equal? (eval-exp (mlet "x" (int 1) (add (int 5) (var "x")))) (int 6) "mlet test")
   (check-equal? (eval-exp (mlet "z" (int 29) (add (int 6) (int 3)))) (int 9) "mlet test")
   (check-equal? (eval-exp (mlet "y" (add (int 1) (int 3)) (add (int 4) (var "y")))) (int 8) "mlet test")
   
   ;; call test
   (check-equal? (eval-exp (call (fun #f "x" (add (var "x") (int 2))) (int 4))) (int 6))
   (check-equal? (eval-exp (call (closure '() (fun #f "x" (add (var "x") (int 7)))) (int 1))) (int 8) "call test")
   (check-equal? (eval-exp (call (closure (list (cons "x" (int 2))) (fun #f "y" (add (var "x") (var "y")))) (int 4))) (int 6) "call test")
   (check-equal? (eval-exp (call (closure (list (cons "x" (int 3))) (fun #f "y" (add (var "x") (var "y")))) (add (int 2) (int 6)))) (int 11) "call test")
   (check-equal? (eval-exp (call (fun "sum-to" "n" (ifgreater (var "n") (int 1) (add (var "n") (call (var "sum-to") (add (var "n") (int -1)))) (int 1))) (int 5))) (int 15) "call test")
   
   ;; apair test
   (check-equal? (eval-exp (apair (int 1) (int 2))) (apair (int 1) (int 2)) "apair test")
   (check-equal? (eval-exp (apair (add (int 3) (int 4)) (int 10))) (apair (int 7) (int 10)) "apair test")
   (check-equal? (eval-exp (apair (add (int 1) (int 2)) (add (int 2) (int 3)))) (apair (int 3) (int 5)) "apair test")
   
   ;; snd test
   (check-equal? (eval-exp (snd (apair (int 1) (int 2)))) (int 2) "snd test")
   (check-equal? (eval-exp (snd (apair (int 1) (int 5)))) (int 5) "snd test")
   (check-equal? (eval-exp (snd (apair (int 1) (add (int 2) (int 3))))) (int 5) "snd test")

   ;; fst test
   (check-equal? (eval-exp (fst (apair (int 1) (int 2)))) (int 1) "fst test")
   (check-equal? (eval-exp (fst (apair (int 4) (int 5)))) (int 4) "fst test")
   (check-equal? (eval-exp (fst (apair (add (int 3) (int 3)) (int 12)))) (int 6) "fst test")
   
   ;; isaunit test
   (check-equal? (eval-exp (isaunit (closure '() (fun #f "x" (aunit))))) (int 0) "isaunit test")
   (check-equal? (eval-exp (isaunit (aunit))) (int 1) "isaunit test")
   (check-equal? (eval-exp (isaunit (fst (apair (aunit) (aunit))))) (int 1))
   
   ;; ifaunit test
   (check-equal? (eval-exp (ifaunit (int 1) (int 2) (int 3))) (int 3) "ifaunit test")
   (check-equal? (eval-exp (ifaunit (add (int 1) (int 2)) (int 5) (int 12))) (int 12) "ifaunit test")
   (check-equal? (eval-exp (ifaunit (aunit) (int 2) (int 3))) (int 2) "ifaunit test")
   (check-equal? (eval-exp (ifaunit (aunit) (add (int 3) (int 1)) (int 6))) (int 4) "ifaunit test")
   (check-equal? (eval-exp (ifaunit (fst (apair (aunit) (int 0))) (int 4) (int 10))) (int 4) "ifaunit test")
   
   ;; mlet* test
   (check-equal? (eval-exp (mlet* '() (add (int 1) (int 2)))) (int 3) "mlet* test")
   (check-equal? (eval-exp (mlet* (list (cons "x" (int 10))) (var "x"))) (int 10) "mlet* test")
   (check-equal? (eval-exp (mlet* (list (cons "x" (int 10)) (cons "y" (int 12))) (add (var "x") (var "y")))) (int 22) "mlet* test")
   
   ;; ifeq test
   (check-equal? (eval-exp (ifeq (int 1) (int 2) (int 3) (int 4))) (int 4) "ifeq test")
   (check-equal? (eval-exp (ifeq (int 2) (int 2) (int 5) (int 6))) (int 5) "ifeq test")
   (check-equal? (eval-exp (ifeq (add (int 3) (int 1)) (int 2) (int 12) (int 7))) (int 7) "ifeq test")
   (check-equal? (eval-exp (ifeq (add (int 0) (int 5)) (int 5) (int 0) (int 1))) (int 0) "ifeq test")
   
   ;; mupl-map test
   (check-equal? (eval-exp (call (call mupl-map (fun #f "x" (add (var "x") (int 7)))) (apair (int 1) (aunit)))) 
                 (apair (int 8) (aunit)) "mupl-map test")
   (check-equal? (eval-exp (call (call mupl-map (fun #f "x" (add (var "x") (int 3)))) (apair (int 1) (apair (int 2) (apair (int 3) (aunit)))))) 
                 (apair (int 4) (apair (int 5) (apair (int 6) (aunit)))) "mupl-map test")
   
   ;; problems 1, 2, and 4 combined test
   (check-equal? (mupllist->racketlist
   (eval-exp (call (call mupl-mapAddN (int 7))
                   (racketlist->mupllist 
                    (list (int 3) (int 4) (int 9)))))) (list (int 10) (int 11) (int 16)) "combined test")
   
   ))

(require rackunit/text-ui)
;; runs the test
(run-tests tests)
